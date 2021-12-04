from datetime import datetime
from conexion_mydb import mdb

class carrito():
  def __init__(self, Id_usuario, Id_forma_de_pago, total_compra):
    self.__Id_compras = None
    self.__Id_usuario = Id_usuario #######
    self.__Id_forma_de_pago = Id_forma_de_pago #####
    self.__fecha_de_compra = datetime.now()
    self.__total_compra = total_compra
    self.__productos_seleccionados = [] #######


  #getters
  def get_Id_compras(self):
    return self.__Id_compras

  def get_Id_usuario(self):
    return self.__Id_usuario

  def get_Id_forma_de_pago(self):
    return self.__Id_forma_de_pago

  def get_fecha_de_compra(self):
    return self.__fecha_de_compra

  def get_total_compra(self):
    return self.__total_compra

  def get_productos_seleccionados(self):
    return self.__productos_seleccionados


  #setters
  def set_Id_compras(self, Id_compras):
    self.__Id_compras = Id_compras

  def set_Id_usuario(self, Id_usuario):
    self.__Id_usuario = Id_usuario

  def set_Id_forma_de_pago(self, Id_forma_de_pago):
    self.__Id_forma_de_pago = Id_forma_de_pago   

  def set_fecha_de_compra(self, fecha_de_compra):
    self.__fecha_de_compra = fecha_de_compra  

  def set_total_compra(self, total_compra):
    self.__total_compra = total_compra

  def set_productos_seleccionados(self, productos_seleccionados):
    self.__productos_seleccionados = productos_seleccionados


  def registrar_compra(self):
      sql = f"INSERT INTO compras (Id_usuario, Id_forma_de_pago, fecha_de_compra, total_compra) VALUES (%s, %s, %s, %s)"

      val = (f"{self.get_Id_usuario()}", f"{self.get_Id_forma_de_pago()}", f"{self.get_fecha_de_compra()}", f"{self.get_total_compra()}")

      mdb.get_cursor().execute(sql, val)
      mdb.get_conexion().commit()

      self.set_Id_compras(mdb.get_cursor().lastrowid)
      mdb.get_cursor().rowcount

      print("""\nCompra realizada satisfactoriamente 
            
            *********GRACIAS POR SU COMPRA*********\n""")
