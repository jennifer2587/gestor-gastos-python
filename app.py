from flask import Flask, render_template, request, redirect, url_for, send_file
from database.db import get_connection
from flask import redirect, url_for
from openpyxl import Workbook
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gastos")
def gastos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM gastos ORDER BY id DESC")
    gastos = cursor.fetchall()
    
    total = sum(float(g["valor"]) for g in gastos)
    
    cantidad = len(gastos)
    
    if gastos: 
        mayor = max(gastos, key=lambda x: float(x["valor"]))
    else:
        mayor = None
        
             
    cursor.close()
    conn.close()
      
    
    return render_template(
        "gastos.html",
        gastos=gastos,
        total=total,
        cantidad=cantidad,
        mayor=mayor
        )



@app.route("/agregar" , methods=["GET"])
def agregar():
     return render_template("agregar.html")
 
 
@app.route("/agregar", methods=["POST"])
def guardar_gasto():
    descripcion = request.form["descripcion"]
    valor = request.form["valor"]
    categoria = request.form["categoria"]
    fecha = request.form["fecha"]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO gastos (descripcion, valor, categoria, fecha)
    VALUES(%s, %s, %s, %s )
    """
    
    cursor.execute(sql, (descripcion, valor, categoria, fecha))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for("gastos"))


@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    
    gastos = []
    
    if  request.method == "POST":
        
        descripcion = request.form["descripcion"]
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT *  FROM gastos WHERE descripcion LIKE %s",
             (f"%{descripcion}%",)
        )
        
        
        gastos = cursor.fetchall()
        
        
        cursor.close()
        conn.close()
        
        
    return render_template("buscar.html", gastos=gastos)
 
 
@app.route("/fechas", methods=["GET", "POST"])
def fechas():
    gastos = []
    
    if request.method == "POST":
        fecha = request.form["fecha"]
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM gastos WHERE fecha = %s"
        cursor.execute(sql, (fecha,))

        gastos = cursor.fetchall()
        
        cursor.close()
        conn.close()
         
    
         
    return render_template("fechas.html", gastos=gastos)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = "DELETE FROM gastos WHERE id = %s"
    cursor.execute(sql, (id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for("gastos"))

@app.route("/modificar/<int:id>", methods=["GET","POST"])
def modificar(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        
        descripcion = request.form["descripcion"]
        valor = request.form["valor"]
        categoria = request.form["categoria"]
        
        
        sql = """
        UPDATE gastos
        SET descripcion=%s, valor=%s, categoria=%s
        WHERE id=%s
        
        """
        
        cursor.execute(sql, (descripcion, valor, categoria, id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for("gastos"))
    
    cursor.execute(
        "SELECT * FROM gastos WHERE id=%s",
        (id,)
    )
    
    gasto = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return render_template("modificar.html", gasto=gasto)

@app.route("/categoria", methods=["GET", "POST"])
def categoria():
    
    gastos = []
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        
        categoria = request.form["categoria"]
        
    
    
        sql = """
        SELECT * FROM gastos
        WHERE categoria LIKE %s
        ORDER BY  categoria
    
          """
    
        cursor.execute(sql, (f"%{categoria}%",))
    
    else:
      
         cursor.execute(
        "SELECT * FROM  gastos ORDER BY  categoria"
        )
    
    
    gastos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("categoria.html", gastos=gastos)


@app.route("/total_categoria")
def total_categoria():
    
    conn = get_connection()
    
    cursor = conn.cursor(dictionary=True)
     
    sql="""
    SELECT categoria, SUM(valor) AS total
    FROM gastos
    GROUP BY  categoria
    """
     
    cursor.execute(sql)
    
    totales = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("total_categoria.html", totales=totales)

@app.route("/total")
def total():
    
    conn = get_connection()
    cursor = conn.cursor(dictionary= True)
    
    
    cursor.execute(
        "SELECT SUM(valor) AS  total FROM gastos"
        
    )
    
    resultado = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    

    return render_template(
        "total.html",
        total=resultado["total"]
    )


@app.route("/exportar")
def exportar():
    
    conn = get_connection()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT * FROM gastos")
    datos = cursor.fetchall()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Gastos"
    
    ws.append(["ID", "Descripcion", "Valor", "categoria", "fecha"])
    
    for gasto in datos:
        ws.append(gasto)
        
    archivo = "gastos.xlsx"
    wb.save(archivo)
        
    cursor.close()
    conn.close()
        
        
    
    return send_file(archivo, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    
    