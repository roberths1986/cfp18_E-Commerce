from carrito import carrito
from conexion_mydb import mdb

class registro_compra():
  def __init__(self, Id_compras, Id_producto, cantidad_compra):
    self.__Id_compras = Id_compras
    self.__Id_producto = Id_producto
    self.__cantidad_compra = cantidad_compra

  #getters
  def get_Id_compras(self):
    return self.__Id_compras

  def get_Id_producto(self):
    return self.__Id_producto

  def get_cantidad_compra(self):
    return self.__cantidad_compra

  #setters
  def set_Id_compras(self, Id_compras):
    self.__Id_compras = Id_compras

  def set_Id_producto(self, Id_producto):
    self.__Id_producto = Id_producto

  def set_cantidad_compra(self, cantidad_compra):
    self.__cantidad_compra = cantidad_compra


  def finalizar_compra(self):
      sql = f"INSERT INTO compras_productos (Id_compras, Id_producto, cantidad_compra) VALUES (%s, %s, %s)"

      val = (f"{self.get_Id_compras()}", f"{self.get_Id_producto()}", f"{self.get_cantidad_compra()}")

      mdb.get_cursor().execute(sql, val)
      mdb.get_conexion().commit()

      #self.set_Id_compras(mdb.get_cursor().lastrowid)

      #print(mdb.get_cursor().rowcount, "Registro Insertado.")


  def revisar_stock(self):
      sql = "SELECT stock FROM producto where Id_producto = %s"
      val = (self.get_Id_producto(),)
      mdb.get_cursor().execute(sql, val)
      resultado = mdb.get_cursor().fetchone()
      return resultado[0]


  def modificar_stock(self, numero):
    sql = "update producto set stock = %s where Id_producto = %s"
    val = (numero, self.get_Id_producto())
    mdb.get_cursor().execute(sql,val)
    mdb.get_conexion().commit()
