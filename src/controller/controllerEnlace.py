from flask import request, jsonify, redirect, render_template
from src.config.connectionMysql import get_connection_mysql
from src.config.connectionMongo import imagenUrl
from src.models.modelEnlace import Enlace
import random, string

def generar_codigo(longitud=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))

# --- CREAR ---
def acortar_enlace():
    try:
        enlace_original = request.form.get('enlace_original')
        url_imagen      = request.form.get('url_imagen')
        descripcion     = request.form.get('descripcion')

        if not enlace_original:
            return jsonify({"error": "El enlace original es obligatorio"}), 400

        # ✅ Verificar si el enlace original ya existe
        db = get_connection_mysql()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id FROM enlaces WHERE enlaceOriginal = %s", (enlace_original,)
        )
        existente = cursor.fetchone()

        if existente:
            db.close()
            return redirect('/?error=Este enlace ya fue acortado anteriormente')

        # Generar código único (que no esté repetido en BD)
        while True:
            codigo = generar_codigo()
            cursor.execute(
                "SELECT id FROM enlaces WHERE enlaceAcortado = %s", (codigo,)
            )
            if not cursor.fetchone():
                break  # El código no existe, se puede usar

        enlace = Enlace(enlace_original, codigo, descripcion)
        cursor.execute(
            "INSERT INTO enlaces (enlaceOriginal, enlaceAcortado, descripcion) VALUES (%s, %s, %s)",
            (enlace.getEnlaceOriginal(), enlace.getEnlaceAcortado(), enlace.getDescripcion())
        )
        db.commit()
        db.close()

        if url_imagen:
            imagenUrl.insert_one({"url": url_imagen, "enlaceAcortado": codigo})

        return redirect('/enlaces')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- LISTAR ---
def listar_enlaces():
    try:
        db = get_connection_mysql()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM enlaces")
        rows = cursor.fetchall()
        db.close()

        # Traer imágenes de MongoDB
        imagenes = {
            doc["enlaceAcortado"]: doc["url"]
            for doc in imagenUrl.find({}, {"_id": 0})
            if "enlaceAcortado" in doc
        }

        for row in rows:
            row["imagen"] = imagenes.get(row["enlaceAcortado"], None)

        return render_template('enlaces.html', enlaces=rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- REDIRIGIR ---
def redirigir_enlace(codigo):
    try:
        db = get_connection_mysql()
        cursor = db.cursor()  # ← fix: sin dictionary ni buffered
        cursor.execute("SELECT * FROM enlaces WHERE enlaceAcortado = %s", (codigo,))
        row = cursor.fetchone()
        db.close()
        if row:
            return redirect(row["enlaceOriginal"])
        return jsonify({"error": "Enlace no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ELIMINAR ---
def eliminar_enlace(codigo):
    try:
        db = get_connection_mysql()
        cursor = db.cursor()
        cursor.execute("DELETE FROM enlaces WHERE enlaceAcortado = %s", (codigo,))
        db.commit()
        db.close()
        imagenUrl.delete_one({"enlaceAcortado": codigo})
        return jsonify({"mensaje": f"Enlace '{codigo}' eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500