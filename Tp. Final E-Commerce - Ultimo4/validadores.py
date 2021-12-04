from validate_email import validate_email
from datetime import datetime
from conexion_mydb import mdb
import base64

class validador():
  def __init__(self):
    pass


  def validar_usuario(self, dicc):
    datosFinales = {}
    errores = {}
    caracteresEspeciales = ["$","@","#","%"]

    for k, v in dicc.items():
      datosFinales[k] = v.strip() #para eliminar los espacio en blanco


    if datosFinales["nombre"] == "":
      errores["nombre"] = "Campo nombre vacio" 

    if datosFinales["apellido"] == "":
      errores["apellido"] = "Campo apellido vacio" 

    if datosFinales["sexo"] == "":
      errores["sexo"] = "Campo sexo vacio" 

    if datosFinales["telefono"] == "":
      errores["telefono"] = "Campo telefono vacio" 
    elif datosFinales["telefono"].isdigit() == False:
      errores["telefono"] = "Los datos deben ser unicamente numericos"
    #Acá se valida si el numero ya se encuentra en la base de datos
    if errores == {}:
      sql = "select Id_usuario from usuario WHERE telefono = %s"
      val = (datosFinales["telefono"],)

      mdb.get_cursor().execute(sql, val)
      resultado = mdb.get_cursor().fetchone()

      if resultado is not None:
        errores["telefono"] = "El Telefono ya existe en la base de datos"

    if datosFinales["fecha_de_nacimiento"] == "":
      errores["fecha_de_nacimiento"] = "campo Fecha de nacimiento vacio"  
    #elif datosFinales["fecha_de_nacimiento"].datetime.strptime(v, "%Y-%m-%d") == False:
      #errores["fecha_de_nacimiento"] = "La fecha debe ingresarse en el formato YYYY-MM-DD"

    if datosFinales["correo"] == "":
      errores["correo"] = "Campo correo vacio"  
    elif validate_email(datosFinales["correo"]) == False:
      errores["correo"] = "El correo no tiene el formato correcto"
    #Acá se valida si el numero ya se encuentra en la base de datos
    if errores == {}:
      sql = "select Id_usuario from usuario WHERE correo = %s"
      val = (datosFinales["correo"],)

      mdb.get_cursor().execute(sql, val)
      resultado = mdb.get_cursor().fetchone()

      if resultado is not None:
        errores["correo"] = "El Correo ya existe en la base de datos"

    if len(datosFinales["password"]) < 8:
      errores["password"] = "La password debe contener mas de 8 caracteres"
    elif datosFinales['password'] == "":
      errores["password"] = "Campo de password vacio"
    elif not any(i.isupper() for i in datosFinales["password"]):
      errores["password"] = "Debe contener al menos una mayuscula"
    elif not any(i.isdigit() for i in datosFinales["password"]):
      errores["password"] = "Debe contener al menos un numero"
    elif not any(i.islower() for i in datosFinales["password"]):
      errores["password"] = "Debe contener al menos una minuscula"
    elif not any(i in caracteresEspeciales for i in datosFinales["password"]):
      errores["password"] = "Debe contener al menos un caracter especial ($,@,#,%)"
    #elif datosFinales["Password"] != datosFinales["cpassword"]:
      #errores["Password"] = "La password no coincide con la validacion de password"
    if errores is not None:
      return errores



  def validar_login(self, dicc):
    errores = {}
    datosFinales = {}
    for k, v in dicc.items():
      datosFinales[k] = v.strip()

    sql = "select * from usuario where correo = %s"
    val = (datosFinales["correo"],)
    mdb.get_cursor().execute(sql, val)
    resultado = mdb.get_cursor().fetchone()
    if resultado is None:
      errores["correo"] = "El correo ingresado no existe en la base o no completó el campo"
    elif base64.decodebytes(resultado[7].encode("UTF-8")).decode("UTF-8") == datosFinales["password"]:
      return resultado#[1:]
    else:
      errores["password"] = "Password incorrecto o no completó el campo"
    print(errores)
      