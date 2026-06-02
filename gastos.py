from datetime import datetime
from openpyxl import Workbook

from db import conn, cursor


# metodo de pago

def obtener_metodo_pago():
    metodo_pago =input(
        " Metodo de pago (Efectivo/tarjeta/transferencia): "
        ).strip().lower()
    
    if metodo_pago =="":
        print("❌ El método de pago no pude estar vacio")
        return None,None
    
    if metodo_pago not in  ["efectivo", "tarjeta", "transferencia"]:
       print("❌ Metodo de pago invalido")
       return None , None
       
       
    numero_transferencia  = ""
    
    if metodo_pago == "transferencia":
        print("pago en transferencia")
        
        numero_transferencia = input(
            "Digite el numero de transferencia:  "
         ).strip()
        
        if numero_transferencia == "":
            print ("❌ Debes ingresar numero de trasferencia")
            return None ,None
        
    
    elif metodo_pago == "efectivo":
        print("Pago en Efectivo")
    
    else:
        print("pago en tarjeta")
     
    return metodo_pago, numero_transferencia 
    


          
# agregar gastos
def agregar_gastos():


    descripcion = input(
        "Por favor describa el gasto: "
        ).strip()
    
    if descripcion == "":
        print("❌ La descripción no puede estar vacía")
        return
    
    try:
        valor = float(
            input(
            "Por favor el valor del gasto: "
            ).strip()
            
         )
        
        # validar negativos
        if valor <= 0:
            print("❌El valor debe ser mayor que cero")
            return
        
        
    except ValueError:
        print("❌ Debes ingresar un número")
        return

    categoria = input(
        "Por favor que categoria corresponde este gasto: "
        ).strip()
    
    if categoria == "":
        print("❌ La categoria no pude estar vacio ")
        return
     
   
    metodo_pago, numero_transferencia = obtener_metodo_pago() 
    
    if metodo_pago is None:
        return
   
    fecha = datetime.now().strftime("%Y-%m-%d")
    
   

   # isert a MySQL
    sql = """
    INSERT INTO gastos
    (descripcion, valor, categoria, metodo_pago, numero_transferencia, fecha)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    valores = (
        descripcion,
        valor,
        categoria,
        metodo_pago,
        numero_transferencia,
        fecha
    )

    cursor.execute(sql, valores)

    conn.commit()

    
    print("✅ Gasto agregado correctamente")
    
    
# mostrar todos los gastos
def mostrar_gasto(gasto):
     
     print(f"id: {gasto['id']}")
     print(f"descripcion:  {gasto['descripcion']} ")
     print(f"valor: {gasto['valor']}")
     print(f"categoria: {gasto['categoria']}")

     print(f"metodo pago: {gasto['metodo_pago']}")

     print(f"fecha: {gasto['fecha']}")
     
     
     if gasto["metodo_pago"] == "transferencia":
         
         print(
             f"numero transferencia: "
             f"{gasto['numero_transferencia']}"
             
         )
         
     print("----------------------------")
         
    

# mostrar gastos

def mostrar_gastos():

    sql = "SELECT * FROM gastos"

    cursor.execute(sql)

    resultados = cursor.fetchall()

    if len(resultados) == 0:
        print("❌ No hay gastos")
        return

    print("\n📋 LISTA DE GASTOS")

    for gasto in resultados:
        
      mostrar_gasto(gasto)
            
# mostrar gasto por categoria


def ver_por_categoria():

    categoria_buscar = input(
        "Ingrese la categoria que desea ver: "
    ).strip().lower()
    
    if categoria_buscar =="":
        print("❌La categoria no pude estar vacia")
        return
    

    sql = "SELECT * FROM gastos WHERE LOWER(categoria) = %s"

    cursor.execute(sql, (categoria_buscar,))

    resultados = cursor.fetchall()

    if len(resultados) == 0:
        print("❌ No hay gastos en esta categoría")
        return

    print(f"\n📂 GASTOS DE: {categoria_buscar}")

    for gasto in resultados:

      
        mostrar_gasto(gasto)
        
 
 # buscar por descripcion
 
def buscar_descripcion():
    
    texto = input(
        "Ingrese  descripcion a buscar: "
    ).strip()   
    
    
    if texto == "":
        print("❌ Debes ingresar una descripcion")
        return 
    
    
    sql = """
    SELECT * FROM GASTOS
    WHERE descripcion LIKE %s
    """
    
    cursor.execute(sql, (f"%{texto}%",))
    
    resultados = cursor.fetchall()
    
    if len(resultados) == 0:
        print("❌ No se encontraron gastos")
        return
    
    print(f"\n🔍 Resultados patra: {texto}")
    
    for gasto in resultados:
         mostrar_gasto(gasto)
         
         
             
# ver gasto por fecha
def  ver_por_fecha():
    
    fecha_buscar = input(
        " Ingresaa la fecha (yyyy-MM-DD): " 
        ).strip()   
    
    if fecha_buscar =="":
        print("❌la fecha no puede estar vacia")
        return
    # validacion fecha
    try:
        datetime.strptime(fecha_buscar, "%Y-%m-%d")
    
    except ValueError:
        print("❌ Formato de fecha invalido")
        print("✅ Usa formato: yyyy-MM-DD")
        return
    
    
    sql = "SELECT * FROM gastos WHERE fecha = %s"
    
    cursor.execute(sql,(fecha_buscar,))
    
    resultados = cursor.fetchall()
    
    if len(resultados) == 0:
        print("❌  No hay gasto en esa fecha")
        return
  
    print(f"\n GASTO DE : {fecha_buscar}")
    
    for gasto in resultados: 
        
         mostrar_gasto(gasto)
      
        
# modificar gastos

def modificar_gastos():

    try:
        id_buscar = int(
            input(
                "Ingrese el ID del gasto a modificar: "
                ).strip()
            )
    except ValueError:
        print("❌ Debes ingresar un número")
        return

    sql = "SELECT * FROM gastos WHERE id = %s"

    cursor.execute(sql, (id_buscar,))

    gasto = cursor.fetchone()

    if gasto is None:
        print("❌ Gasto no encontrado")
        return

    print("✅ Gasto encontrado")

    nueva_descripcion = input(
        "Nueva descripcion: "
        ).strip()

    nuevo_valor = input(
        "Nuevo valor: "
        ).strip()

    nueva_categoria = input(
        "Nueva categoria: "
        ).strip()

    if nueva_descripcion == "":
        nueva_descripcion = gasto["descripcion"]

    if nuevo_valor == "":
        nuevo_valor = gasto["valor"]

    else:
        try:
            nuevo_valor = float(nuevo_valor)
            
            if nuevo_valor <=0:
                print("❌ El valor debe ser mayor que cero")
                return

        except ValueError:
            print("❌ Valor inválido")
            return

    if nueva_categoria == "":
        nueva_categoria = gasto["categoria"]


    print("\nEditar metodo pago")
    
    nuevo_metodo_pago, nuevo_numero_transferencia = obtener_metodo_pago()
    
    if nuevo_metodo_pago is None:
        return
    
    
    # confirmar modificacion
    
    confirmar = input(
        "\n¿Guardaar cambios? (si/no):"
    ).strip().lower()
    
    
    if confirmar != "si":
        print("❌  Modificacion cancelada")
        return

    sql_update = """
    UPDATE gastos
    SET descripcion = %s,
        valor = %s,
        categoria = %s,
        metodo_pago = %s,
        numero_transferencia = %s
    WHERE id = %s
    """

    valores = (
        nueva_descripcion,
        nuevo_valor,
        nueva_categoria,
        nuevo_metodo_pago,
        nuevo_numero_transferencia,
        id_buscar
    )

    cursor.execute(sql_update, valores)

    conn.commit()

    print("✅ Gasto modificado")

        
# total por  categorias  
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
    
# Eliminar gasto    
    
def eliminar_gasto():

    try:
        id_buscar = int(
            input(
                "Ingrese ID gasto a eliminar: "
                ).strip()
            )

    except ValueError:
        print("❌ Debes ingresar un número")
        return
   # buascar gasto 
    sql = "SELECT * FROM gastos WHERE id = %s"

    cursor.execute(sql, (id_buscar,))

    gasto = cursor.fetchone()
    
    if gasto is None:
        print(" ❌ No existe un gasto con ese ID")
        return
    
    print("\n GASTO ENCONTRADO")
    print(f"Descripcion : {gasto['descripcion']}")
    print(f"Valor: {gasto['valor']}")
    print(f"Categoria: {gasto['categoria']}")
    
    confirmar = input(
        "\n ¿ Seguro que deseas eliminar este gasto? (si/no): "
    ).strip().lower()
    
    if confirmar != "si":
        print("Eliminacion cancelada")
        return
    sql_delete = "DELETE FROM gastos where id = %s"
     
    cursor.execute(sql_delete, (id_buscar,))
    
    conn.commit()
    
    print("✅ Gasto eliminado correctamente") 
    
 
# exporta a excel    
def exportar_excel():
    
    sql = "SELECT *FROM gastos" 
    
    cursor.execute(sql)
    
    resultados = cursor.fetchall()
    
    if len(resultados) ==0:
        print("❌  No hay gastos para exportar")
        return
    
    # crear archivo en exel
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
    
    
    
    
    
    
    
    
    
    
def main():
   
    
    while True:
        print("\n -------GASTOS------")
        print("1. Agregar gasto")    
        print("2. Mostrar todos los gastos")
        print("3. Ver gasto por categoria ") 
        print("4. Mostrar total por categoria") 
        print("5.Mostrar total general")
        print("6.Modificar gasto")
        print("7.Eliminar gasto")
        print("8.Ver gastos por fechas")
        print("9.buscar gasto por descripcion")
        print("10. Exportar a Exel")
        print("11. Salir")
        
        opcion = input("seleccione un opcion:")
        
        if opcion  == "1":
           agregar_gastos()
           
        elif opcion == "2":
            mostrar_gastos()
           
            
        elif opcion == "3":
             ver_por_categoria()   
            
        elif opcion == "4" :
               total_categoria()
        
        elif opcion == "5" :
             total_gastos()
            
        
        elif opcion == "6" :
             modificar_gastos() 
             
        elif opcion == "7" :
            eliminar_gasto()  
                
        elif opcion == "8" :
            ver_por_fecha() 
            
        elif opcion == "9" :
            buscar_descripcion()     
                              
        elif opcion == "10" :
            exportar_excel()                       
                                   
        elif opcion == "11" :
              print("Saliendo......")  
              break
        else:
            print("❌ opcion invalida")  
            
if __name__ == "__main__":
    
 main()            
          
                     
               



