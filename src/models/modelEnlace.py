class Enlace:
    def __init__(self, enlaceOriginal: str, enlaceAcortado: str, descripcion: str = ""):
        self.enlaceOriginal = enlaceOriginal
        self.enlaceAcortado = enlaceAcortado
        self.descripcion    = descripcion

    def getEnlaceOriginal(self)  -> str: return self.enlaceOriginal
    def getEnlaceAcortado(self)  -> str: return self.enlaceAcortado
    def getDescripcion(self)     -> str: return self.descripcion

    def setEnlaceOriginal(self, v: str): self.enlaceOriginal = v
    def setEnlaceAcortado(self, v: str): self.enlaceAcortado = v
    def setDescripcion(self, v: str):    self.descripcion    = v

    def __str__(self) -> str:
        return f"Enlace(original='{self.enlaceOriginal}', acortado='{self.enlaceAcortado}', descripcion='{self.descripcion}')"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "enlaceOriginal": self.enlaceOriginal,
            "enlaceAcortado": self.enlaceAcortado,
            "descripcion":    self.descripcion
        }