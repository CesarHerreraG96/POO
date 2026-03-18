class Persona:
    def __init__(self, nombre, correo, direccion, telefono):
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono

    def mostrar_info(self):
        return f"{self.nombre} | Tel: {self.telefono} | Correo: {self.correo}"


class Cliente(Persona):
    def __init__(self, nombre, correo, direccion, telefono, rfc):
        super().__init__(nombre, correo, direccion, telefono)
        self.rfc = rfc

    def mostrar_info(self):
        return super().mostrar_info() + f" | RFC: {self.rfc}"


class Empleado(Persona):
    def __init__(self, id_empleado, nombre, correo, direccion, telefono, departamento, usuario, contrasena):
        super().__init__(nombre, correo, direccion, telefono)
        self.id_empleado = id_empleado
        self.departamento = departamento
        self.usuario = usuario
        self.contrasena = contrasena

    def mostrar_info(self):
        return f"ID:{self.id_empleado} | {self.nombre} | Depto: {self.departamento}"


class Producto:
    def __init__(self, id_producto, nombre, precio, cantidad):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def mostrar_info(self):
        return f"ID:{self.id_producto} | {self.nombre} - ${self.precio} - Stock: {self.cantidad}"

    def reducir_stock(self, cantidad_vendida):
        if cantidad_vendida <= self.cantidad:
            self.cantidad -= cantidad_vendida
            return True
        else:
            print("No hay suficiente stock.")
            return False


class Herramientas(Producto):
    def __init__(self, id_producto, nombre, precio, cantidad, tipo):
        super().__init__(id_producto, nombre, precio, cantidad)
        self.tipo = tipo

    def mostrar_info(self):
        return f"ID:{self.id_producto} | {self.nombre} ({self.tipo}) - ${self.precio} - Stock: {self.cantidad}"


class Venta:
    def __init__(self, cliente, empleado):
        self.cliente = cliente
        self.empleado = empleado
        self.productos = []
        self.total = 0

    def agregar_producto(self, producto, cantidad):
        if producto.reducir_stock(cantidad):
            self.productos.append((producto, cantidad))
            self.total += producto.precio * cantidad
        else:
            print("No se pudo agregar el producto.")

    def mostrar_ticket(self):
        print("\n----- TICKET DE VENTA -----")
        print("Cliente:", self.cliente.mostrar_info())
        print("Empleado:", self.empleado.mostrar_info())

        print("\nProductos:")
        for producto, cantidad in self.productos:
            print(f"{producto.nombre} x{cantidad} = ${producto.precio * cantidad}")

        print("\nTotal: $", self.total)
        print("---------------------------")


class Inventario:
    def __init__(self):
        self.lista_productos = []

    def agregar_producto(self, producto):
        self.lista_productos.append(producto)

    def mostrar_productos(self):
        print("\n--- INVENTARIO ---")
        for producto in self.lista_productos:
            print(producto.mostrar_info())


# ---------------- MAIN ----------------

if __name__ == "__main__":

    inventario = Inventario()
    clientes = []
    empleados = []


    admin = Empleado(1, "Admin", "admin@mail.com", "Centro", "0000000000", "Admin", "admin", "1234")
    empleados.append(admin)


    inventario.agregar_producto(Herramientas(1, "Martillo", 150, 10, "Manual"))
    inventario.agregar_producto(Herramientas(2, "Taladro", 1200, 5, "Electrico"))

    # LOGIN
    while True:
        print("\n=== INICIO DE SESION ===")
        user = input("Usuario: ")
        password = input("Contraseña: ")

        usuario_valido = None

        for emp in empleados:
            if emp.usuario == user and emp.contrasena == password:
                usuario_valido = emp
                break

        if usuario_valido:
            print(f"\nBienvenido {usuario_valido.nombre}")

            # MENU PRINCIPAL
            while True:

                print("\n====== MENU FERRETERIA ======")
                print("1. Ver inventario")
                print("2. Agregar producto")
                print("3. Aumentar stock")
                print("4. Registrar cliente")
                print("5. Registrar empleado")
                print("6. Realizar venta")
                print("7. Cerrar sesión")

                opcion = input("Seleccione: ")

                if opcion == "1":
                    inventario.mostrar_productos()

                elif opcion == "2":
                    idp = int(input("ID: "))
                    nombre = input("Nombre: ")
                    precio = float(input("Precio: "))
                    cantidad = int(input("Cantidad: "))
                    tipo = input("Tipo: ")

                    inventario.agregar_producto(Herramientas(idp, nombre, precio, cantidad, tipo))
                    print("Producto agregado.")

                elif opcion == "3":
                    idp = int(input("ID producto: "))
                    extra = int(input("Cantidad a agregar: "))

                    for p in inventario.lista_productos:
                        if p.id_producto == idp:
                            p.cantidad += extra
                            print("Stock actualizado.")
                            break

                elif opcion == "4":
                    nombre = input("Nombre: ")
                    correo = input("Correo: ")
                    direccion = input("Direccion: ")
                    telefono = input("Telefono: ")
                    rfc = input("RFC: ")

                    clientes.append(Cliente(nombre, correo, direccion, telefono, rfc))
                    print("Cliente registrado.")

                elif opcion == "5":
                    id_emp = len(empleados) + 1
                    nombre = input("Nombre: ")
                    correo = input("Correo: ")
                    direccion = input("Direccion: ")
                    telefono = input("Telefono: ")
                    depto = input("Departamento: ")
                    usuario = input("Usuario: ")
                    contrasena = input("Contraseña: ")

                    empleados.append(Empleado(id_emp, nombre, correo, direccion, telefono, depto, usuario, contrasena))
                    print("Empleado registrado.")

                elif opcion == "6":

                    if not clientes:
                        print("No hay clientes.")
                        continue

                    print("\nClientes:")
                    for i, c in enumerate(clientes):
                        print(i + 1, "-", c.mostrar_info())

                    cliente = clientes[int(input("Seleccione cliente: ")) - 1]

                    venta = Venta(cliente, usuario_valido)

                    while True:
                        inventario.mostrar_productos()
                        idp = int(input("ID producto (0 para salir): "))

                        if idp == 0:
                            break

                        cantidad = int(input("Cantidad: "))

                        for p in inventario.lista_productos:
                            if p.id_producto == idp:
                                venta.agregar_producto(p, cantidad)
                                break

                    venta.mostrar_ticket()

                elif opcion == "7":
                    print("Cerrando sesión...")
                    break

        else:
            print("Usuario o contraseña incorrectos.")