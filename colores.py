# clases de colores
class Colores_class:
    def __init__(self):
        self.__BOTONES_1 = "#1995AD"
        self.__BOTONES_2 = "#A1D6E2"
        self.__CAJAS_TERCIARIAS = "#A3A3A4"
        self.__CAJAS_SECUNDARIAS = "#B6B5B7"
        self.__CAJAS_PRINCIPALES = "#D7D6D7"
        self.__CAJAS_PRINCIPALES_TRANS = "#B9E8FF60"
        self.__FONDO_GENERAL = "#F1F1F2"

    def get_botones_1(self):
        return self.__BOTONES_1 
    
    def get_botones_2(self):
        return self.__BOTONES_2
    
    def get_cajas_principales(self):
        return self.__CAJAS_PRINCIPALES
    
    def get_cajas_principales_trans(self):
        return self.__CAJAS_PRINCIPALES_TRANS
    
    def get_cajas_secundarias(self):
        return self.__CAJAS_SECUNDARIAS
    
    def get_cajas_terciarias(self):
        return self.__CAJAS_TERCIARIAS
    
    def get_fondo_general(self):
        return self.__FONDO_GENERAL
    
