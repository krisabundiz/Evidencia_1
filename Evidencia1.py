def menu_principal():
    print('-------MENU--------')
    print('\n(1) Registar nota')
    print('(2) Consultas y reportes')
    print('(3) Cancelar nota')
    print('(4) Salir del sistema')
    opcion=input('\nIngrese el núnmero del servicio que desea solicitar: ')
    if opcion == '1':


class Nota:
    def _init_(self, folio, fecha, cliente):
        self.folio = folio
        self.fecha = fecha
        self.cliente = cliente
        self.servicios = []
        
notas = []
folio_actual = 1
notas_canceladas = [] 

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
        
