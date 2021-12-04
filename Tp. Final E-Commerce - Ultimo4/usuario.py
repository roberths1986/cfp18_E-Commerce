from datetime import datetime
import base64
from conexion_mydb import mdb
from validadores import validador
from carrito import carrito


class usuario():
  def __init__(self, Id_usuario, nombre, apellido, sexo, telefono, fecha_de_nacimiento, correo, password, Id_localidad):
    self.__Id_usuario = Id_usuario
    self.__nombre = nombre    
    self.__apellido = apellido    
    self.__sexo = sexo   
    self.__telefono = telefono    
    self.__fecha_de_nacimiento = fecha_de_nacimiento
    self.__correo = correo    
    self.__password = self.encriptarPass(password) 
    self.__Id_localidad = Id_localidad
    #self.__carrito = None

  #getters
  def get_Id_usuario(self):
    return self.__Id_usuario

  def get_nombre(self):
    return self.__nombre

  def get_apellido(self):
    return self.__apellido

  def get_sexo(self):
    return self.__sexo

  def get_telefono(self):
    return self.__telefono

  def get_fecha_de_nacimiento(self):
    return self.__fecha_de_nacimiento

  def get_correo(self):
    return self.__correo

  def get_password(self):
    return self.__password

  def get_Id_localidad(self):
    return self.__Id_localidad

  #def get_carrito(self):
    #return self.__carrito


  #setters

  def set_Id_usuario(self, Id_usuario):
    self.__Id_usuario = Id_usuario

  def set_nombre(self, nombre):
    self.__nombre = nombre

  def set_apellido(self, apellido):
    self.__apellido = apellido

  def set_sexo(self, sexo):
    self.__sexo = sexo

  def set_telefono(self, telefono):
    self.__telefono = telefono

  def set_fecha_de_nacimiento(self, fecha_de_nacimiento):
    self.__fecha_de_nacimiento = fecha_de_nacimiento

  def set_correo(self, correo):
    self.__correo = correo

  def set_password(self, password):
    self.__password = self.encriptarPass(password)

  def set_Id_localidad(self, Id_localidad):
    self.__Id_localidad = Id_localidad

  #def set_carrito(self, carrito):
    #self.__carrito = carrito


  def encriptarPass(self, password):
    return base64.encodebytes(bytes(password, "utf-8")).decode("utf-8")

  def desencriptarPass(self, password):
    return base64.decodebytes(password.encode("UTF-8")).decode("utf-8")



  def registrarse(self):
    sql = f"INSERT INTO usuario (Id_usuario, nombre, apellido, sexo, telefono, fecha_nacimiento, correo, password, Id_localidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    val = (f"{self.get_Id_usuario()}", f"{self.get_nombre()}", f"{self.get_apellido()}", f"{self.get_sexo()}", f"{self.get_telefono()}", f"{self.get_fecha_de_nacimiento()}", f"{self.get_correo()}", f"{self.get_password()}", f"{self.get_Id_localidad()}")

    mdb.get_cursor().execute(sql, val)
    mdb.get_conexion().commit()

    self.set_Id_usuario(mdb.get_cursor().lastrowid)

    print(mdb.get_cursor().rowcount, "Registro Insertado.")


  def actualizar_nombre(self, campo):
    sql = "update usuario set nombre = %s where Id_usuario = %s"
    val = (campo, self.get_Id_usuario())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()

  def actualizar_apellido(self, campo):
    sql = "update usuario set apellido = %s where Id_usuario = %s"
    val = (campo, self.get_Id_usuario())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()

  def actualizar_sexo(self, campo):
    sql = "update usuario set sexo = %s where Id_usuario = %s"
    val = (campo, self.get_Id_usuario())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()

  def actualizar_telefono(self, campo):
    sql = "update usuario set telefono = %s where Id_usuario = %s"
    val = (campo, self.get_Id_usuario())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()

  def actualizar_fecha_nacimiento(self, campo):
    sql = "update usuario set fecha_nacimiento = %s where Id_usuario = %s"
    val = (campo, self.get_Id_usuario())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()

  def actualizar_correo(self, campo):
    sql = "update usuario set correo = %s where Id_usuario = %s"
    val = (campo, self.get_Id_usuario())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()

  def actualizar_password(self, campo):
    sql = "update usuario set password = %s where Id_usuario = %s"
    val = (self.encriptarPass(campo), self.get_Id_usuario())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()

  def actualizar_Id_localidad(self, campo):
    sql = "update usuario set Id_localidad = %s where Id_usuario = %s"
    val = (campo, self.get_Id_usuario())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()


  def darse_de_baja(self):
    sql = "delete from usuario where Id_usuario = %s"
    val = (self.get_Id_usuario(),)
    
    mdb.get_cursor().execute(sql, val)
    mdb.get_conexion().commit()