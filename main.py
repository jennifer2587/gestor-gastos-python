from models.gastos import *
from reports.informes import *


  
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
          
                     
               



