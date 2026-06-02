import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="gestor_gastos"
    
)


cursor = conn.cursor(dictionary=True)

#AQUÍ VA LA PRUEBA
cursor.execute("SELECT DATABASE();")
print(cursor.fetchone())