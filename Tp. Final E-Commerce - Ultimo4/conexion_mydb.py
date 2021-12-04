import mysql.connector

conf = {
    'host': "localhost",
    'user': "root",
    'password': "",
    'database': "tp_ecommerce"
    }

class conect_basededatos():
  def __init__(self):
    self.__conexion = mysql.connector.connect(**conf)
    self.__cursor = self.__conexion.cursor()

  def get_cursor(self):
    return self.__cursor

  def get_conexion(self):
    return self.__conexion
    
mdb = conect_basededatos()