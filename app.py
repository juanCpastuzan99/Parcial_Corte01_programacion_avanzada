from flask import Flask, render_template
from src.controller.controllerEnlace import (
    acortar_enlace,
    redirigir_enlace,
    listar_enlaces,
    eliminar_enlace
)

app = Flask(__name__, template_folder='src/templates')

@app.route('/')
def index():
    return render_template('index.html')

app.add_url_rule('/enlaces/crear',    'acortar',   acortar_enlace,   methods=['POST'])
app.add_url_rule('/enlaces',          'listar',    listar_enlaces,   methods=['GET'])
app.add_url_rule('/enlaces/<codigo>', 'eliminar',  eliminar_enlace,  methods=['DELETE'])
app.add_url_rule('/<codigo>',         'redirigir', redirigir_enlace, methods=['GET'])  # ← debe ir al final

if __name__ == '__main__':
    app.run(debug=True, port=3000)