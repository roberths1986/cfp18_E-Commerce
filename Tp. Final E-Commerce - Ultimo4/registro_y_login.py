#from typing import Counter
from registro_compra import registro_compra
from usuario import usuario
from validadores import validador
import stdiomask
from conexion_mydb import mdb
from validate_email import validate_email
import base64
from tabulate import tabulate
from carrito import carrito
import time


def menu_principal():
    print("-----------------------------------------------------------------------------")
    print("-------------------------Bienvenido/a al E-Commerce--------------------------")
    print("-----------------------------------------------------------------------------\n")
    print("""Seleccione el numero de opcion que desea: 
            1- Registrarse
            2. Ingresar (ya tengo un usuario)
            3. Salir""")
    

    opcion = int(input("--->"))
    if opcion == 1:
        registro_usuario()
        print("--------------------------Ahora puedes loguearte--------------------------\n")
        usuario1 = usuario_login()
        menu_usuario(usuario1)
    elif opcion == 2:
        usuario1 = usuario_login()
        menu_usuario(usuario1)
    elif opcion == 3:
        print("--------------------Hasta Luego, gracias por su visita--------------------\n")
        quit()
    else:
        if opcion < 1 or opcion > 3:
            print("El dato ingresado no es valido, intente de nuevo")
            menu_principal()


def menu_usuario(usuario):
    print(f"---------------------Bienvenido/a {usuario.get_nombre()}---------------------\n")
    print("""Seleccione el numero de opcion que desea: 
            1- Comprar (Ver productos)
            2. Modificar datos de registro
            3. Darse de baja
            4. Salir
            """)

    opcion = int(input("--->"))
    if opcion == 1:
        mostrar_productos()
        menu_compra(usuario)
    elif opcion == 2:
        modificar_registro(usuario)
        menu_usuario(usuario)
    elif opcion == 3:
        baja_usuario(usuario)
        print("-------------------------------Hasta Luego-------------------------------\n")
        menu_usuario(usuario)
    elif opcion == 4:
        print("--------------------Hasta Luego, gracias por su visita-------------------")
        quit()
    else:
        print("*********Al ingresar los datos, ingresaste algun dato no permitido, por favor comienza de vuelta*********\n")
        menu_usuario(usuario)


def menu_compra(usuario1):
    print("""\nSeleccione el numero de opcion que desea: 

            1- Agregar producto/s al carrito
            2- Volver al menu anterior
            """)
    
    opcion = int(input("--->"))
    if opcion == 1: #ESTA OPCION DEBERIA CREARME UN OBJETO CARRITO EN UN DICCIONARIO
        i = False
        lista_productos = []
        monto = 0
        contar_productos = {}
        cantidad_productos = 0
        while i == False:
            print("Ingrese el id del producto que desea agregar: ")
            opcion2 = int(input("Id de Producto: "))
            lista_productos.append(agregar_al_carrito(opcion2))
            opcion3 = int(input("Si desea agregar otro producto marque 1, si desea finalizar la compra marque 2\n--->"))
            if opcion3 == 1:
                continue
            elif opcion3 == 2:
                print("""Seleccione el numero de opcion de pago que desea: 
                    1- Efectivo
                    2- Tarjeta de Credito
                    3- tarjeta de Debito
                    4- Mercado Pago
                    """)
                forma_de_pago = int(input("--->"))

            for i in lista_productos:
                monto += i[4]
                contar_productos[i] = contar_productos.get(i, 0) + 1

            for v in contar_productos.values():
                cantidad_productos += v

            print("\n----Procesando su factura----\n")
            time.sleep(3)
            #print(contar_productos)
            print("-------------------------FACTURA-------------------------")
            print(tabulate(lista_productos, headers=['Id', 'Tipo de Producto.', 'Nombre', 'Marca', 'Precio', 'Cantidad']))
                
            print(f"\nCANTIDAD DE PRODUCTOS --------->>>>>> {cantidad_productos}")
            print(f"TOTAL A PAGAR ----------------->>>>>> $ {monto}\n")


                
            carrito1 = carrito(usuario1.get_Id_usuario(), forma_de_pago, monto)
            carrito1.set_productos_seleccionados(lista_productos)

            comprar = int(input("Marque 1 si desea terminar su compra o marque 2 si desea salir del sistema ---> "))
            if comprar == 1:
                print("\n----Procesando su compra----\n")
                time.sleep(3)
                carrito1.registrar_compra()
            else:
                print("\n--------------------Hasta Luego, gracias por su visita--------------------\n")
                quit()

            #return carrito1

            for k, v in contar_productos.items():
                stock_actualizado = 0
                registrarCompra1 = registro_compra(carrito1.get_Id_compras(), k[0], v)
                registrarCompra1.finalizar_compra()
                stock_actual_producto = registrarCompra1.revisar_stock()
                stock_actualizado = stock_actual_producto - v
                registrarCompra1.modificar_stock(stock_actualizado)


    elif opcion == 2: 
        menu_usuario(usuario1)



def registro_usuario():
    i = False
    while i == False:
        nuevoUsuario = {'Id_usuario': "", 
                        'nombre': "",
                        'apellido': "", 
                        'sexo': "", 
                        'telefono': "", 
                        'fecha_de_nacimiento': "", 
                        'correo': "", 
                        'password': "", 
                        'Id_localidad': ""
                        }

        for keys, values in nuevoUsuario.items():
            if keys == "nombre" or keys == "apellido" or keys == "correo":
                nuevoUsuario[keys] = input(f"Escriba su {keys}: ").lower()
            elif keys == "sexo":
                print("\nIntroduce 'F' si es Femenino o 'M' si es Masculino")
                nuevoUsuario[keys] = input(f"Escriba su {keys}: ").upper()
            elif keys == "telefono":
                print("\nIntroducir solo caracteres numericos")
                nuevoUsuario[keys] = input(f"Escriba su {keys}: ")
            elif keys == "fecha_de_nacimiento":
                print("\nIntroducir la fecha en formato yyyy-mm-dd")
                nuevoUsuario[keys] = input(f"Escriba su {keys}: ")
            elif keys == "password":
                print("\nLa password debe contener mas de 8 caracteres y tener al menos una mayuscula, una minuscula, un numero y alguno de los siguientes caracteres especiales ($,@,#,%)")
                nuevoUsuario[keys] = stdiomask.getpass(prompt=f"Escriba su {keys}: ", mask = "*")
            elif keys == "Id_localidad":
                print("")
                print("""\nIntroducir el numero de la localidad a la cual pertenece:
                \nARGENTINA
                1- Lanus
                2- Avellaneda
                3- Paternal
                4- Recoleta
                \nURUGUAY
                5- Carmelo
                6- Campana
                7- Ciudad Vieja
                8- Barrio Sur
                \nCHILE
                9- Providencia
                10- Padahuel
                \nPERU
                11- Barranca
                12- Matucana
                13- Poroy
                14- Santiago
                \nVENEZUELA
                15- El Paraiso
                16- La Candelaria
                17- Chacao
                18- Altamira\n---->""")
                nuevoUsuario[keys] = input(f"Escriba su {keys}: ")

                
        cpassword = stdiomask.getpass(prompt=f"Escriba de nuevo su password: ", mask = "*")

        if cpassword == "":
            print("Campo de cpassword vacio")
        elif cpassword != nuevoUsuario["password"]:
            print("La password no coincide con la validacion de password, intente registrarse nuevamente")
            registro_usuario()



        validar = validador()
        errores = validar.validar_usuario(nuevoUsuario)
        if not errores:
            usuario1 = usuario(**nuevoUsuario)
            usuario1.registrarse()
            i = True
            return usuario1
        else:
            print(errores)
            print("Intente registrarse nuevamente")




def usuario_login():
    i = 3
    while i != 0:
        login_usuario = {'correo': input("Ingrese su correo: ").lower(), 
                        'password': stdiomask.getpass(prompt="Ingrese password: ", mask = "*")
                        }

        validar = validador()
        errores = validar.validar_login(login_usuario)
        #print(errores)
        if errores:
            usuario2 = usuario(*validar.validar_login(login_usuario))
            print("-------------Se ha logueado satisfactoriamente-------------")
            return usuario2
        else:
            print(f"\n***********Intente loguearse nuevamente. Le quedan {i-1} intento/s***********\n")
            i -= 1
            if i == 0:
                print("\n**************Agotaste tus opciones, intenta de vuelta**************\n")
            


def modificar_registro(usuario):
    opcion = int(input("""\nIntroducir el numero que corresponde al dato que desea modificar:\n
            1- Modificar Nombre
            2- Modificar Apellido
            3- Modificar Sexo
            4- Modificar Telefono
            5- Modificar Fecha de Nacimiento
            6- Modificar Correo
            7- Modificar Password
            8- Modificar Id de Localidad\n---->"""))
    
    if opcion == 1:
        campo= input("Ingrese el nuevo Nombre: ").capitalize()
        if campo == "":
            print("Campo nombre vacio")
        else:
            usuario.actualizar_nombre(campo)
            print("Se modifico el Nombre correctamente")

    elif opcion == 2:
        campo= input("Ingrese el nuevo Apellido: ").capitalize()
        if campo == "":
            print("Campo Apellido vacio")
        else:
            usuario.actualizar_apellido(campo)
            print("Se modifico el Apellido correctamente")

    elif opcion == 3:
        campo= input("Ingrese el nuevo Sexo: ").upper()
        if campo == "":
            print("Campo Sexo vacio")
        else:
            usuario.actualizar_sexo(campo)
            print("Se modifico el Sexo correctamente")

    elif opcion == 4:
        campo= input("Ingrese el nuevo Telefono: ")
        if campo == "":
            print("Campo Telefono vacio")
        elif campo.isdigit() == False:
            print("Los datos deben ser unicamente numericos")
        elif campo:
            sql = "select Id_usuario from usuario WHERE telefono = %s"
            val = (campo,)

            mdb.get_cursor().execute(sql, val)
            resultado = mdb.get_cursor().fetchone()

            if resultado is not None:
                print("El Telefono ya existe en la base de datos")
            else:
                usuario.actualizar_telefono(campo)
                print("Se modifico el Telefono correctamente")

    elif opcion == 5:
        campo= input("Ingrese la nueva Fecha de Nacimiento en formato yyyy-mm-dd: ")
        if campo == "":
            print("Campo Fecha de Nacimiento vacio")
        else:
            usuario.actualizar_fecha_nacimiento(campo)
            print("Se modifico la Fecha de Nacimiento correctamente")

    elif opcion == 6:
        campo= input("Ingrese el nuevo Correo: ").lower()
        if campo == "":
            print("Campo Correo vacio")
        elif validate_email(campo) == False:
            print("El correo no tiene el formato correcto")
        elif campo:
            sql = "select Id_usuario from usuario WHERE correo = %s"
            val = (campo,)

            mdb.get_cursor().execute(sql, val)
            resultado = mdb.get_cursor().fetchone()

            if resultado is not None:
                print("El Correo ya existe en la base de datos")
            else:
                usuario.actualizar_correo(campo)
                print("Se modifico el Correo correctamente")

    elif opcion == 7:
        #campo= input("Ingrese el nuevo Password: ")
        campo = stdiomask.getpass(prompt="Ingrese el nuevo Password: ", mask = "*")
        if campo == "":
            print("Campo Password vacio")
        elif len(campo) < 8:
            print("La password debe contener mas de 8 caracteres")
        elif not any(i.isupper() for i in campo):
            print("Debe contener al menos una mayuscula")
        elif not any(i.isdigit() for i in campo):
            print("Debe contener al menos un numero")
        elif not any(i.islower() for i in campo):
            print("Debe contener al menos una minuscula")
        elif not any(i in "$,@,#,%" for i in campo):
            print("Debe contener al menos un caracter especial ($,@,#,%)")
        else:
            usuario.actualizar_password(campo)
            print("Se modifico el Password correctamente")

    elif opcion == 8:
        campo= input("""Ingrese el nuevo Id de Localidad: 
        \nARGENTINA
            1- Lanus
            2- Avellaneda
            3- Paternal
            4- Recoleta
            \nURUGUAY
            5- Carmelo
            6- Campana
            7- Ciudad Vieja
            8- Barrio Sur
            \nCHILE
            9- Providencia
            10- Padahuel
            \nPERU
            11- Barranca
            12- Matucana
            13- Poroy
            14- Santiago
            \nVENEZUELA
            15- El Paraiso
            16- La Candelaria
            17- Chacao
            18- Altamira\n---->""")
        if campo == "":
            print("Campo Id de Localidad vacio")
        else:
            usuario.actualizar_Id_localidad(campo)
            print("Se modifico el Id de Localidad correctamente")



def baja_usuario(usuario):
    opcion = int(input("""Si desea darse de baja, seleccione el numero de opcion: 
                        1. Si darse de baja
                        2. Volver al menu anterior\n---->"""))
    if opcion == 1:
        usuario.darse_de_baja()
        print("----------------Usuario dado de baja satisfactoriamente----------------\n")
        menu_principal()
    else:
        pass


def mostrar_productos():
    mdb.get_cursor().execute("SELECT * FROM productos_venta")

    resultado = mdb.get_cursor().fetchall()

    lista = []
    for productos in resultado:
        lista.append(list(productos))
    print(tabulate(lista, headers=['Id', 'Tipo de Producto', 'Nombre', 'Marca', 'Precio']))


def agregar_al_carrito(Id_producto):
    sql = "SELECT * FROM productos_venta where Id_producto = %s"
    val = (Id_producto,)
    mdb.get_cursor().execute(sql, val)
    resultado = mdb.get_cursor().fetchone()
    return resultado