from datetime import date
from random import randint

# Requisito 7
NIVEL_CRITICA = "crítica"
NIVEL_BAJA = "baja"
NIVEL_MEDIA = "media"
NIVEL_ALTA = "alta"

# Requisito 7
PORCENTAJE_MINIMO_BAJA = 40
PORCENTAJE_MINIMO_MEDIA = 60
PORCENTAJE_MINIMO_ALTA = 80

# Requisitos 1 y 2
MESES_POR_ANIO = 12
ANIO_MINIMO = 1
ANIO_MAXIMO = 9999

# Requisitos 2, 3, 9 y 13
FECHA_MAXIMA = date(ANIO_MAXIMO, MESES_POR_ANIO, 31)

# Requisitos 12 y 13
CAMPOS_LINEA_HOTEL = 5
CAMPOS_LINEA_OCUPACION = 2


class Hotel:
    # Requisito 1
    def __init__(self,
                 nombre: str,
                 habitaciones_habilitadas: int,
                 fecha_inicio: date):
        self.nombre = nombre
        self.habitaciones_habilitadas = habitaciones_habilitadas
        self.fecha_inicio = fecha_inicio
        self.habitaciones_ocupadas = []

    # Requisitos 2, 6, 8 y 9
    def calcular_fecha_del_dia(self, posicion: int) -> date:
        fecha = self.fecha_inicio
        for _ in range(posicion):
            fecha = calcular_dia_siguiente(fecha)
        return fecha

    # Requisitos 2 y 9
    def calcular_fecha_dia_siguiente(self) -> date | None:
        fecha_ultimo_dia = self.calcular_fecha_ultimo_dia()
        if fecha_ultimo_dia is None:
            fecha_dia_siguiente = self.fecha_inicio
        elif fecha_ultimo_dia == FECHA_MAXIMA:
            fecha_dia_siguiente = None
        else:
            fecha_dia_siguiente = calcular_dia_siguiente(fecha_ultimo_dia)
        return fecha_dia_siguiente

    # Requisitos 2, 3 y 13
    def calcular_dias_disponibles(self) -> int:
        fecha_dia_siguiente = self.calcular_fecha_dia_siguiente()
        if fecha_dia_siguiente is None:
            dias_disponibles = 0
        else:
            tiempo_disponible = FECHA_MAXIMA - fecha_dia_siguiente
            dias_disponibles = tiempo_disponible.days + 1
        return dias_disponibles

    # Requisitos 2, 3 y 13
    def revisar_dias_disponibles(self, numero_de_dias: int):
        dias_disponibles = self.calcular_dias_disponibles()
        if dias_disponibles == 0:
            raise ValueError(f"El registro del hotel ya llegó a la fecha máxima, {FECHA_MAXIMA}")
        if numero_de_dias > dias_disponibles and dias_disponibles == 1:
            raise ValueError(f"Solo queda 1 día por registrar hasta el {FECHA_MAXIMA}")
        if numero_de_dias > dias_disponibles:
            raise ValueError(f"Solo quedan {dias_disponibles} días por registrar hasta el {FECHA_MAXIMA}")

    # Requisitos 2, 3 y 13
    def revisar_rango_ocupadas(self, ocupadas: int):
        if ocupadas < 0 or ocupadas > self.habitaciones_habilitadas:
            raise ValueError(f"Las habitaciones ocupadas van de 0 a {self.habitaciones_habilitadas}")

    # Requisitos 2, 3 y 13
    def convertir_habitaciones_ocupadas(self, ocupadas_texto: str) -> int:
        if not es_entero(ocupadas_texto):
            raise ValueError("Las habitaciones ocupadas deben ser un número entero")
        ocupadas = int(ocupadas_texto)
        self.revisar_rango_ocupadas(ocupadas)
        return ocupadas

    # Requisitos 2, 3 y 13
    def registrar_dia(self, ocupadas: int):
        self.revisar_dias_disponibles(1)
        self.revisar_rango_ocupadas(ocupadas)
        self.habitaciones_ocupadas.append(ocupadas)

    # Requisito 3
    def convertir_numero_de_dias(self, dias_texto: str) -> int:
        if not es_entero(dias_texto):
            raise ValueError("El número de días debe ser un número entero")
        numero_de_dias = int(dias_texto)
        if numero_de_dias < 1:
            raise ValueError("Se debe simular al menos un día")
        self.revisar_dias_disponibles(numero_de_dias)
        return numero_de_dias

    # Requisito 3
    def simular_dias(self, numero_de_dias: int, minimo: int, maximo: int):
        self.revisar_dias_disponibles(numero_de_dias)
        self.revisar_rango_ocupadas(minimo)
        self.revisar_rango_ocupadas(maximo)
        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo")
        for _ in range(numero_de_dias):
            self.habitaciones_ocupadas.append(randint(minimo, maximo))

    # Requisito 4
    def calcular_dias_registrados(self) -> int:
        dias_registrados = len(self.habitaciones_ocupadas)
        return dias_registrados

    # Requisito 4
    def calcular_noches_vendidas(self) -> int:
        noches_vendidas = 0
        for ocupadas in self.habitaciones_ocupadas:
            noches_vendidas = noches_vendidas + ocupadas
        return noches_vendidas

    # Requisito 4
    def calcular_promedio_ocupadas(self) -> float | None:
        dias_registrados = self.calcular_dias_registrados()
        if dias_registrados == 0:
            promedio = None
        else:
            promedio = self.calcular_noches_vendidas() / dias_registrados
        return promedio

    # Requisitos 4 y 11
    def calcular_porcentaje_ocupacion(self) -> float | None:
        promedio = self.calcular_promedio_ocupadas()
        if promedio is None:
            porcentaje = None
        else:
            porcentaje = promedio / self.habitaciones_habilitadas * 100
        return porcentaje

    # Requisito 5
    def calcular_desviacion_estandar(self) -> float | None:
        promedio = self.calcular_promedio_ocupadas()
        if promedio is None:
            desviacion = None
        else:
            suma_de_cuadrados = 0
            for ocupadas in self.habitaciones_ocupadas:
                suma_de_cuadrados = suma_de_cuadrados + (ocupadas - promedio) ** 2
            desviacion = (suma_de_cuadrados / self.calcular_dias_registrados()) ** 0.5
        return desviacion

    # Requisito 6
    def buscar_posicion_mas_ocupada(self) -> int | None:
        posicion_mas_ocupada = None
        for posicion in range(len(self.habitaciones_ocupadas)):
            if posicion_mas_ocupada is None:
                posicion_mas_ocupada = posicion
            elif self.habitaciones_ocupadas[posicion] > self.habitaciones_ocupadas[posicion_mas_ocupada]:
                posicion_mas_ocupada = posicion
        return posicion_mas_ocupada

    # Requisito 6
    def buscar_posicion_menos_ocupada(self) -> int | None:
        posicion_menos_ocupada = None
        for posicion in range(len(self.habitaciones_ocupadas)):
            if posicion_menos_ocupada is None:
                posicion_menos_ocupada = posicion
            elif self.habitaciones_ocupadas[posicion] < self.habitaciones_ocupadas[posicion_menos_ocupada]:
                posicion_menos_ocupada = posicion
        return posicion_menos_ocupada

    # Requisito 7
    def clasificar_ocupacion(self, ocupadas: int) -> str:
        porcentaje_del_dia = ocupadas / self.habitaciones_habilitadas * 100
        if porcentaje_del_dia < PORCENTAJE_MINIMO_BAJA:
            nivel = NIVEL_CRITICA
        elif porcentaje_del_dia < PORCENTAJE_MINIMO_MEDIA:
            nivel = NIVEL_BAJA
        elif porcentaje_del_dia < PORCENTAJE_MINIMO_ALTA:
            nivel = NIVEL_MEDIA
        else:
            nivel = NIVEL_ALTA
        return nivel

    # Requisito 7
    def contar_dias_en_nivel(self, nivel: str) -> int:
        dias_en_nivel = 0
        for ocupadas in self.habitaciones_ocupadas:
            if self.clasificar_ocupacion(ocupadas) == nivel:
                dias_en_nivel = dias_en_nivel + 1
        return dias_en_nivel

    # Requisito 8
    def es_dia_critico(self, posicion: int) -> bool:
        critico = self.clasificar_ocupacion(self.habitaciones_ocupadas[posicion]) == NIVEL_CRITICA
        return critico

    # Requisito 8
    def contar_racha_critica_desde(self, posicion_inicio: int) -> int:
        dias_de_racha = 0
        posicion = posicion_inicio
        while posicion < len(self.habitaciones_ocupadas) and self.es_dia_critico(posicion):
            dias_de_racha = dias_de_racha + 1
            posicion = posicion + 1
        return dias_de_racha

    # Requisito 8
    def buscar_inicio_racha_critica_mas_larga(self) -> int | None:
        mejor_inicio = None
        mejor_largo = 0
        for posicion in range(len(self.habitaciones_ocupadas)):
            empieza_racha = self.es_dia_critico(posicion) and (posicion == 0 or not self.es_dia_critico(posicion - 1))
            if empieza_racha:
                largo = self.contar_racha_critica_desde(posicion)
                if largo > mejor_largo:
                    mejor_largo = largo
                    mejor_inicio = posicion
        return mejor_inicio

    # Requisito 9
    def calcular_fecha_ultimo_dia(self) -> date | None:
        dias_registrados = self.calcular_dias_registrados()
        if dias_registrados == 0:
            fecha_ultimo_dia = None
        else:
            fecha_ultimo_dia = self.calcular_fecha_del_dia(dias_registrados - 1)
        return fecha_ultimo_dia

    # Requisito 9
    def calcular_dias_sin_registrar(self, fecha_actual: date) -> int:
        fecha_dia_siguiente = self.calcular_fecha_dia_siguiente()
        if fecha_dia_siguiente is None:
            dias_sin_registrar = 0
        else:
            tiempo_sin_registrar = fecha_actual - fecha_dia_siguiente
            dias_sin_registrar = tiempo_sin_registrar.days
            if dias_sin_registrar < 0:
                dias_sin_registrar = 0
        return dias_sin_registrar


class CadenaHotelera:
    # Requisito 10
    def __init__(self):
        self.hoteles = []

    # Requisito 12
    def tiene_hoteles(self) -> bool:
        hay_hoteles = len(self.hoteles) > 0
        return hay_hoteles

    # Requisito 10
    def buscar_hotel(self, nombre: str) -> Hotel | None:
        nombre = nombre.strip()
        hotel_encontrado = None
        for hotel in self.hoteles:
            if hotel_encontrado is None and hotel.nombre == nombre:
                hotel_encontrado = hotel
        return hotel_encontrado

    # Requisitos 1 y 10
    def existe_hotel(self, nombre: str) -> bool:
        existe = False
        for hotel in self.hoteles:
            if hotel.nombre == nombre:
                existe = True
        return existe

    # Requisito 1
    def crear_hotel(self,
                    nombre: str,
                    habitaciones_texto: str,
                    anio_texto: str,
                    mes_texto: str,
                    dia_texto: str) -> Hotel:
        nombre = nombre.strip()
        if nombre == "":
            raise ValueError("El nombre del hotel no puede estar vacío")
        if self.existe_hotel(nombre):
            raise ValueError("Ya existe un hotel con ese nombre")
        if not es_entero(habitaciones_texto):
            raise ValueError("Las habitaciones habilitadas deben ser un número entero")
        habitaciones_habilitadas = int(habitaciones_texto)
        if habitaciones_habilitadas < 1:
            raise ValueError("El hotel debe tener al menos una habitación habilitada")
        if not es_fecha_valida(anio_texto, mes_texto, dia_texto):
            raise ValueError("La fecha no es válida")
        fecha_inicio = date(int(anio_texto), int(mes_texto), int(dia_texto))
        hotel = Hotel(nombre, habitaciones_habilitadas, fecha_inicio)
        self.hoteles.append(hotel)
        return hotel

    # Requisito 12
    def crear_hotel_desde_linea(self, linea: str) -> Hotel:
        campos = linea.split(";")
        if len(campos) != CAMPOS_LINEA_HOTEL:
            raise ValueError("La línea no tiene cinco campos")
        hotel = self.crear_hotel(campos[0].strip(),
                                 campos[1].strip(),
                                 campos[2].strip(),
                                 campos[3].strip(),
                                 campos[4].strip())
        return hotel

    # Requisito 13
    def registrar_dia_desde_linea(self, linea: str):
        campos = linea.split(";")
        if len(campos) != CAMPOS_LINEA_OCUPACION:
            raise ValueError("La línea no tiene dos campos")
        hotel = self.buscar_hotel(campos[0])
        if hotel is None:
            raise ValueError("No hay un hotel con ese nombre")
        ocupadas = hotel.convertir_habitaciones_ocupadas(campos[1].strip())
        hotel.registrar_dia(ocupadas)

    # Requisito 11
    def buscar_hotel_mayor_ocupacion(self) -> Hotel | None:
        hotel_mayor = None
        for hotel in self.hoteles:
            if hotel.calcular_dias_registrados() > 0:
                if hotel_mayor is None:
                    hotel_mayor = hotel
                elif hotel.calcular_porcentaje_ocupacion() > hotel_mayor.calcular_porcentaje_ocupacion():
                    hotel_mayor = hotel
        return hotel_mayor

    # Requisito 11
    def buscar_hotel_menor_ocupacion(self) -> Hotel | None:
        hotel_menor = None
        for hotel in self.hoteles:
            if hotel.calcular_dias_registrados() > 0:
                if hotel_menor is None:
                    hotel_menor = hotel
                elif hotel.calcular_porcentaje_ocupacion() < hotel_menor.calcular_porcentaje_ocupacion():
                    hotel_menor = hotel
        return hotel_menor


# Requisitos 1, 2 y 3
def es_entero(texto: str) -> bool:
    resultado = True
    try:
        int(texto)
    except ValueError:
        resultado = False
    return resultado


# Requisitos 1 y 2
def es_bisiesto(anio: int) -> bool:
    bisiesto = anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
    return bisiesto


# Requisitos 1 y 2
def calcular_dias_del_mes(anio: int, mes: int) -> int:
    if mes == 2:
        if es_bisiesto(anio):
            dias_del_mes = 29
        else:
            dias_del_mes = 28
    elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
        dias_del_mes = 30
    else:
        dias_del_mes = 31
    return dias_del_mes


# Requisito 1
def es_fecha_valida(anio_texto: str, mes_texto: str, dia_texto: str) -> bool:
    if not es_entero(anio_texto) or not es_entero(mes_texto) or not es_entero(dia_texto):
        valida = False
    else:
        anio = int(anio_texto)
        mes = int(mes_texto)
        dia = int(dia_texto)
        if anio < ANIO_MINIMO or anio > ANIO_MAXIMO:
            valida = False
        elif mes < 1 or mes > MESES_POR_ANIO:
            valida = False
        elif dia < 1 or dia > calcular_dias_del_mes(anio, mes):
            valida = False
        else:
            valida = True
    return valida


# Requisito 2
def calcular_dia_siguiente(fecha: date) -> date:
    anio = fecha.year
    mes = fecha.month
    dia = fecha.day + 1
    if dia > calcular_dias_del_mes(anio, mes):
        dia = 1
        mes = mes + 1
        if mes > MESES_POR_ANIO:
            mes = 1
            anio = anio + 1
    dia_siguiente = date(anio, mes, dia)
    return dia_siguiente
