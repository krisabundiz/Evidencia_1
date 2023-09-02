def main():
    while True:
        print("Menú Principal")
        print("1. Registrar una nota")
        print("2. Consultas y reportes")
        print("3. Salir")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            registrar_nota()
        elif opcion == 2:
            print("Submenú de Consultas y Reportes")
            print("1. Consulta por período")
            print("2. Consulta por folio")
            print("3. Regresar al menú principal")
            
            subopcion = int(input("Seleccione una opción: "))
            
            if subopcion == 1:
                consulta_por_periodo()
            elif subopcion == 2:
                consulta_por_folio()
            elif subopcion == 3:
                continue
        elif opcion == 3:
            print("¡Hasta luego!")
            break

class Nota:
    def _init_(self, folio, fecha, cliente):
        self.folio = folio
        self.fecha = fecha
        self.cliente = cliente
        self.servicios = []
        
notas = []
folio_actual = 1
notas_canceladas = [] 


##Cancelar notas
def cancelar_nota():
    folio_cancelar=int(input("Ingrese el folio de la nota a cancelar:"))
    
    for  nota in notas:
        if nota.folio==folio_cancelar and nota not in notas_canceladas:
            print("Folio:", nota.folio)
            print("Fecha", nota.fecha)
            print("Cliente:", nota.cliente)
            print("Monto a pagar:", nota.calcular_monto_total())
            print("Servicios:")
            for servicio in nota.servicios:
                print("- Nombre:", servicio.nombre)
                print("  Costo:", servicio.costo)
            
            confirmacion = input("¿Desea cancelar esta nota? (S/N): ")
            if confirmacion.lower() == "s":
                notas_canceladas.append(nota)
                print("Nota cancelada.")
            else:
                print("Cancelación de nota abortada.")
            return
    print("La nota no existe o ya está cancelada.")
        
