from openpyxl import Workbook
from database.db import get_connection


conn = get_connection()
cursor = conn.cursor(dictionary=True)



#total por  categorias  
def total_categoria():

    sql = """
    SELECT categoria, SUM(valor) AS total
    FROM gastos
    GROUP BY categoria
    """

    cursor.execute(sql)

    resultados = cursor.fetchall()

    if len(resultados) == 0:
        print("❌ No hay gastos")
        return

    print("\n💰 TOTAL POR CATEGORIAS")

    for gasto in resultados:

        print(f"{gasto['categoria']}: ${gasto['total']}")
             
         
          
# total gastos        
def total_gastos():

    sql = "SELECT SUM(valor) AS total FROM gastos"

    cursor.execute(sql)

    resultado = cursor.fetchone()

    total = resultado["total"]

    if total is None:
        total = 0

    print(f"💰 Total gastado: {total}")
    
    
# exporta a excel    
def exportar_excel():
    
    sql = "SELECT * FROM gastos" 
    
    cursor.execute(sql)
    
    resultados = cursor.fetchall()
    
    if len(resultados) == 0:
        print("❌  No hay gastos para exportar")
        return
    
    # crear archivo en Excel
    libro = Workbook()
    
    hoja = libro.active
    
    hoja.title = "Gastos"

    # encabezados
    hoja.append([
        "ID",
        "Descripcion",
        "Valor",
        "Categoria",
        "Metodo Pago",
        "Numero Transferencia",
        "Fecha"
    ])
    
    # agregar datos
    for gasto in resultados:
        
        hoja.append([
            gasto["id"],
            gasto["descripcion"],
            gasto["valor"],
            gasto["categoria"],
            gasto["metodo_pago"],
            gasto["numero_transferencia"],
            str(gasto["fecha"])
        ])
        
        
   # guardar archivos
    libro.save("gastos.xlsx")
        
    print("✅ Excel exportado correctamente")    
    
    
    
    
