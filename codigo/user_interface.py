from datetime import date
from os import system

from business_logic import FECHA_MAXIMA, NIVEL_ALTA, NIVEL_BAJA, NIVEL_CRITICA, NIVEL_MEDIA, CadenaHotelera

# Requisito 14
system("cls")
print("=====================================")
print("Bienvenido al programa de ocupación de la cadena Sol Caribe")
print("=====================================")

# Requisito 10
cadena_objeto = CadenaHotelera()

# Requisito 14
opcion = ""
while opcion != "7":
    print("=====================================")
    print("Menú")
    print("=====================================")
    print("1. Crear un hotel")
    print("2. Registrar las habitaciones ocupadas del día siguiente")
    print("3. Simular días")
    print("4. Ver el informe de un hotel")
    print("5. Ver el hotel con el porcentaje de ocupación más alto y el más bajo")
    print("6. Cargar los hoteles y la ocupación desde archivos")
    print("7. Salir")
    opcion = input("Opción: ")

    # Requisito 1
    if opcion == "1":
        nombre = input("Nombre del hotel: ")
        habitaciones_texto = input("Habitaciones habilitadas: ")
        anio_texto = input("Año de la fecha de inicio: ")
        mes_texto = input("Mes de la fecha de inicio: ")
        dia_texto = input("Día de la fecha de inicio: ")
        try:
            hotel_objeto = cadena_objeto.crear_hotel(nombre, habitaciones_texto, anio_texto, mes_texto, dia_texto)
            print(f"Se creó el hotel {hotel_objeto.nombre}, sin días registrados")
        except ValueError as error:
            print(error)

    # Requisito 2
    elif opcion == "2":
        # Requisito 10
        nombre = input("Nombre del hotel: ")
        hotel_objeto = cadena_objeto.buscar_hotel(nombre)
        if hotel_objeto is None:
            print("No hay un hotel con ese nombre")
        else:
            # Requisito 2
            fecha_dia_siguiente = hotel_objeto.calcular_fecha_dia_siguiente()
            if fecha_dia_siguiente is None:
                print(f"El registro del hotel ya llegó a la fecha máxima, {FECHA_MAXIMA}")
            else:
                ocupadas_guardadas = False
                while not ocupadas_guardadas:
                    try:
                        ocupadas_texto = input(f"Habitaciones ocupadas del {fecha_dia_siguiente}: ")
                        ocupadas = hotel_objeto.convertir_habitaciones_ocupadas(ocupadas_texto)
                        hotel_objeto.registrar_dia(ocupadas)
                        ocupadas_guardadas = True
                    except ValueError as error:
                        print(error)
                print(f"Se registró el día {fecha_dia_siguiente}")

    # Requisito 3
    elif opcion == "3":
        # Requisito 10
        nombre = input("Nombre del hotel: ")
        hotel_objeto = cadena_objeto.buscar_hotel(nombre)
        if hotel_objeto is None:
            print("No hay un hotel con ese nombre")
        else:
            # Requisito 3
            try:
                numero_de_dias = hotel_objeto.convertir_numero_de_dias(input("Número de días que se van a simular: "))
                minimo = hotel_objeto.convertir_habitaciones_ocupadas(input("Habitaciones ocupadas mínimas: "))
                maximo = hotel_objeto.convertir_habitaciones_ocupadas(input("Habitaciones ocupadas máximas: "))
                hotel_objeto.simular_dias(numero_de_dias, minimo, maximo)
                if numero_de_dias == 1:
                    print(f"Se simuló 1 día en {hotel_objeto.nombre}")
                else:
                    print(f"Se simularon {numero_de_dias} días en {hotel_objeto.nombre}")
            except ValueError as error:
                print(error)

    # Requisito 4
    elif opcion == "4":
        # Requisito 10
        nombre = input("Nombre del hotel: ")
        hotel_objeto = cadena_objeto.buscar_hotel(nombre)
        if hotel_objeto is None:
            print("No hay un hotel con ese nombre")
        else:
            # Requisito 4
            print("=====================================")
            print("Informe del hotel")
            print("=====================================")
            print(f"Hotel: {hotel_objeto.nombre}")
            print(f"Habitaciones habilitadas: {hotel_objeto.habitaciones_habilitadas}")
            dias_registrados = hotel_objeto.calcular_dias_registrados()
            if dias_registrados == 0:
                print("El hotel no tiene días registrados")
            else:
                # Requisito 4
                noches_vendidas = hotel_objeto.calcular_noches_vendidas()
                promedio = hotel_objeto.calcular_promedio_ocupadas()
                porcentaje = hotel_objeto.calcular_porcentaje_ocupacion()
                print(f"Días registrados: {dias_registrados}")
                print(f"Noches vendidas: {noches_vendidas}")
                print(f"Promedio de habitaciones ocupadas por día: {round(promedio, 2)}")
                print(f"Porcentaje de ocupación: {round(porcentaje, 2)} %")

                # Requisito 5
                desviacion = hotel_objeto.calcular_desviacion_estandar()
                print(f"Desviación estándar de las habitaciones ocupadas: {round(desviacion, 2)}")

                # Requisito 6
                fecha_mas_ocupada = hotel_objeto.calcular_fecha_del_dia(hotel_objeto.buscar_posicion_mas_ocupada())
                fecha_menos_ocupada = hotel_objeto.calcular_fecha_del_dia(hotel_objeto.buscar_posicion_menos_ocupada())
                print(f"Día de más habitaciones ocupadas: {fecha_mas_ocupada}")
                print(f"Día de menos habitaciones ocupadas: {fecha_menos_ocupada}")

                # Requisito 7
                print(f"Días en ocupación {NIVEL_CRITICA}: {hotel_objeto.contar_dias_en_nivel(NIVEL_CRITICA)}")
                print(f"Días en ocupación {NIVEL_BAJA}: {hotel_objeto.contar_dias_en_nivel(NIVEL_BAJA)}")
                print(f"Días en ocupación {NIVEL_MEDIA}: {hotel_objeto.contar_dias_en_nivel(NIVEL_MEDIA)}")
                print(f"Días en ocupación {NIVEL_ALTA}: {hotel_objeto.contar_dias_en_nivel(NIVEL_ALTA)}")

                # Requisito 8
                inicio_racha = hotel_objeto.buscar_inicio_racha_critica_mas_larga()
                if inicio_racha is None:
                    print("El hotel no tuvo ningún día en ocupación crítica")
                else:
                    dias_de_racha = hotel_objeto.contar_racha_critica_desde(inicio_racha)
                    fecha_inicio_racha = hotel_objeto.calcular_fecha_del_dia(inicio_racha)
                    if dias_de_racha == 1:
                        print(f"Racha más larga en ocupación crítica: 1 día, el {fecha_inicio_racha}")
                    else:
                        print(f"Racha más larga en ocupación crítica: {dias_de_racha} días, desde el {fecha_inicio_racha}")

                # Requisito 9
                fecha_actual = date.today()
                print(f"Último día registrado: {hotel_objeto.calcular_fecha_ultimo_dia()}")
                dias_sin_registrar = hotel_objeto.calcular_dias_sin_registrar(fecha_actual)
                if dias_sin_registrar == 0:
                    print("El registro está al día")
                else:
                    fecha_desde = hotel_objeto.calcular_fecha_dia_siguiente()
                    fecha_hasta = hotel_objeto.calcular_fecha_del_dia(dias_registrados + dias_sin_registrar - 1)
                    print(f"Días por registrar: {dias_sin_registrar}, del {fecha_desde} al {fecha_hasta}")

    # Requisito 11
    elif opcion == "5":
        hotel_mayor = cadena_objeto.buscar_hotel_mayor_ocupacion()
        hotel_menor = cadena_objeto.buscar_hotel_menor_ocupacion()
        if hotel_mayor is None:
            print("Ningún hotel tiene días registrados")
        else:
            porcentaje_mayor = round(hotel_mayor.calcular_porcentaje_ocupacion(), 2)
            porcentaje_menor = round(hotel_menor.calcular_porcentaje_ocupacion(), 2)
            print(f"Hotel con el porcentaje de ocupación más alto: {hotel_mayor.nombre}, con {porcentaje_mayor} %")
            print(f"Hotel con el porcentaje de ocupación más bajo: {hotel_menor.nombre}, con {porcentaje_menor} %")

    # Requisitos 12 y 13
    elif opcion == "6":
        # Requisito 12
        if cadena_objeto.tiene_hoteles():
            print("La carga solo se hace con el programa sin hoteles")
        else:
            # Requisito 12
            hoteles_leidos = False
            ruta_hoteles = input("Ruta del archivo de hoteles: ")
            try:
                with open(ruta_hoteles, encoding="utf-8") as archivo_hoteles:
                    hoteles_cargados = 0
                    numero_de_linea = 0
                    for linea in archivo_hoteles:
                        numero_de_linea = numero_de_linea + 1
                        if numero_de_linea > 1 and linea.strip() != "":
                            try:
                                cadena_objeto.crear_hotel_desde_linea(linea)
                                hoteles_cargados = hoteles_cargados + 1
                            except ValueError as error:
                                print(f"Línea {numero_de_linea} descartada: {error}")
                print(f"Hoteles cargados: {hoteles_cargados}")
                hoteles_leidos = True
            except FileNotFoundError:
                print("El archivo no existe")

            # Requisito 13
            if hoteles_leidos:
                ruta_ocupacion = input("Ruta del archivo de ocupación: ")
                try:
                    with open(ruta_ocupacion, encoding="utf-8") as archivo_ocupacion:
                        dias_cargados = 0
                        numero_de_linea = 0
                        for linea in archivo_ocupacion:
                            numero_de_linea = numero_de_linea + 1
                            if numero_de_linea > 1 and linea.strip() != "":
                                try:
                                    cadena_objeto.registrar_dia_desde_linea(linea)
                                    dias_cargados = dias_cargados + 1
                                except ValueError as error:
                                    print(f"Línea {numero_de_linea} descartada: {error}")
                    print(f"Días cargados: {dias_cargados}")
                except FileNotFoundError:
                    print("El archivo no existe")

    # Requisito 14
    elif opcion != "7":
        print("La opción no es válida")

# Requisito 14
print("Fin del programa")
