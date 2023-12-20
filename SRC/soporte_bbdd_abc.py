
import mysql.connector

def creacion_bbdd_tablas(query, contraseña, nombre_bbdd = None):
    
    if nombre_bbdd is not None:
        cnx = mysql.connector.connect(
            user = 'root',
            password = contraseña,
            host = "127.0.0.1")
        
        mycursor = cnx.cursor()

        try:
            mycursor.excecute(query)
            print(mycursor)
        except mysql.connector.Error as err:
            print(err) 
            print('SQLSTATE', err.sqlstate)
            print('Message', err.msg)
    else:
        cnx = mysql.connector.connect(
            user = 'root',
            password = contraseña,
            host = "127.0.0.1"
            database = nombre_bbdd)
        
        mycursor = cnx.cursor()

        try:
            mycursor.excecute(query)
            print(mycursor)
        except mysql.connector.Error as err:
            print(err) 
            print('SQLSTATE', err.sqlstate)
            print('Message', err.msg)

def insertar_datos(query, contraseña, nombre_bbdd, lista_tuplas):

    cnx= mysql.connector.connect(
            user = 'root',
            password = contraseña,
            host = "127.0.0.1")
    mycursor = cnx.cursor()

    try:
            mycursor.excecute(query)
            print(mycursor)
    except mysql.connector.Error as err:
            print(err) 
            print('SQLSTATE', err.sqlstate)
            print('Message', err.msg)