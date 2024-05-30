# importamos tkinter
# el paquete ttk es el paquete/módulo principal de tkinter donde están todos los componentes gráficos de esta libreria
# en ttk2 hay también algunos componentes más nuevos
# el constructor lo tenemos que invocar también con el * para que importe además de los elementos gráficos el constructor

from tkinter import ttk
from tkinter import *
import sqlite3


# Es mejor externalizar las classes en un archivo models.py, pero en este ejemplo lo dejamos aquí en main
class Producto:
    # vinculamos la clase con nuestra ventana gráfica. Le pasamos al constructor root la variable.

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root  # le asigno una variable a la ventana (root)
        self.ventana.title("App Gestor de Productos")  # Personalizamos el título
        self.ventana.resizable(1,
                               1)  # 1,1 hace referencia a horizontal y vertical y es como true, si ponemos 0,0 no será redimensionable
        self.ventana.wm_iconbitmap(
            "recursos/icon.ico")  # comando para cargar el icono con windows. Con mac o linux puede cambiar.

        # creamos un frame, marcos, donde insertamos varios widgets
        # Frame Principal
        framePrincipal = LabelFrame(self.ventana, pady=10, padx=10, text="Registrar un nuevo producto", font=('Calibri', 16, 'bold'))
        framePrincipal.grid(row=0, column=0, columnspan=4, pady=10, padx=10)  # El frame partiría de la esquina superior izquierda

        # Label Nombre
        self.etiquetaNombre = Label(framePrincipal, text="Nombre: ")  # a la variable etiquetaNombre le asignamos una label que queremos que esté dentro de framePrincipal
        self.etiquetaNombre.grid(row=1, column=0)
        # Entry Nombre
        self.nombreInput = Entry(framePrincipal)
        self.nombreInput.focus()  # Para que el cursor aparezca en el input al iniciar la aplicación. Solo lo puede llevar un cajón de texto.
        self.nombreInput.grid(row=1, column=1, pady=10)

        # Label Precio
        self.etiquetaPrecio = Label(framePrincipal, text="Precio: ")
        self.etiquetaPrecio.grid(row=1, column=2)
        # Entry Precio
        self.precioInput = Entry(framePrincipal)
        self.precioInput.grid(row=1, column=3, pady=10)

        # Label Categoría
        self.etiquetaCategoria = Label(framePrincipal, text="Categoría: ")
        self.etiquetaCategoria.grid(row=2, column=0)
        # Entry Categoría
        self.categoriaInput = Entry(framePrincipal)
        self.categoriaInput.grid(row=2, column=1, pady=10)

        # Label Stock
        self.etiquetaStock = Label(framePrincipal, text="Stock: ")
        self.etiquetaStock.grid(row=2, column=2)
        # Entry Stock
        self.stockInput = Entry(framePrincipal)
        self.stockInput.grid(row=2, column=3, pady=10)

        # Botón Guardar
        # ttk es porque utilizamos la libreria ttk
        # Aunque self.add_producto es un método y lleva normalmente paréntesis al final, en este caso no los lleva porque va con command
        self.botonGuardar = ttk.Button(framePrincipal, text="Guardar Producto", command=self.add_producto)
        self.botonGuardar.grid(row=3, columnspan=4, sticky=W + E, pady=10)

        # Label de mensaje de error que añadiremos en la parte de las validaciones.
        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=1, column=0, columnspan=4, sticky=W + E)

        # Estructura de la tabla
        self.listaProductos = ttk.Treeview(framePrincipal, height=20, columns=("#1", "#2", "#3"), style="mystyle.Treeview")
        self.listaProductos.grid(row=4, column=0, columnspan=4)
        self.listaProductos.heading("#0", text="Nombre", anchor=CENTER)  # Encabezado 0
        self.listaProductos.heading("#1", text="Precio", anchor=CENTER)  # Encabezado 1
        self.listaProductos.heading("#2", text="Categoría", anchor=CENTER)  # Encabezado 2
        self.listaProductos.heading("#3", text="Stock", anchor=CENTER)  # Encabezado 3

        # Botones Eliminar y Editar
        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 14, "bold"))

        botonEliminar = ttk.Button(text="ELIMINAR", style="my.TButton", command=self.del_producto, width=40)
        botonEliminar.grid(row=4, column=1, sticky=W + E)
        botonEditar = ttk.Button(text="EDITAR", style="my.TButton", command = self.edit_producto, width=40)
        botonEditar.grid(row=4, column=2, sticky=W + E)

        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:  # Iniciamos una conexión con la base de datos (alias con)
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.listaProductos.get_children()  # Obtengo los registros de la base de datos y los borro
        for fila in registros_tabla:
            self.listaProductos.delete(fila)

        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)

        for fila in registros:
            self.listaProductos.insert("", 0, text=fila[1], values=fila[2:5])  #Empieza a insertar productos dese la posición 0. Borramos en las instrucciones anteriores para que al insertar no se encuentre contenido y de error.

    # Método encargados de leer los cajones de texto y comprobaciones. En este caso solo se va a comprobar que el cajón esté vacío
    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombreInput.get()
        return len(nombre_introducido_por_usuario) != 0  # Retornamos el tamaño de la información en caso que sea distinto de 0

    def validacion_precio(self):
        precio_introducido_usuario = self.precioInput.get()
        return len(precio_introducido_usuario) != 0

    def validacion_categoria(self):
        categoria_introducida_usuario = self.categoriaInput.get()
        return len(categoria_introducida_usuario) != 0

    def validacion_stock(self):
        stock_introducido_usuario = self.stockInput.get()
        return len(stock_introducido_usuario) != 0

    #Reiniciar Cajas y Mensaje
    def reiniciar_cajas_mensaje(self):
        self.nombreInput.delete(0, END)
        self.precioInput.delete(0, END)
        self.categoriaInput.delete(0, END)
        self.stockInput.delete(0, END)
        self.nombreInput.focus()

    # Función Añadir producto
    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)"  # NULL es porque es una columna con autoincrementador, el id en este caso. Hay que dejar NULL porque si no daría error. Los interrogantes son variables que les vamos a pasar.
            parametros = (self.nombreInput.get(), self.precioInput.get(), self.categoriaInput.get(), self.stockInput.get())
            self.db_consulta(query, parametros)
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            self.mensaje["text"] = "El nombre es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() == False and self.validacion_categoria() and self.validacion_stock():
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() == False and self.validacion_stock():
            self.mensaje["text"] = "La categoría es obligatoria"
        elif self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock() == False:
            self.mensaje["text"] = "El stock es obligatorio"
        else:
            self.mensaje["text"] = "Todos los campos son obligatorios"

        self.mensaje["text"] = "Producto {} guardado con éxito".format(self.nombreInput.get())
        self.get_productos()  # invocamos a get_productos para acutalizar lo que vemos en la lista por pantalla
        self.reiniciar_cajas_mensaje() #Reiniciamos

    #Función Eliminar
    def del_producto(self):
        self.mensaje["text"] = "" #Mensaje inicialmente vacio
        #Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            self.listaProductos.item(self.listaProductos.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.listaProductos.item(self.listaProductos.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'  #Consulta SQL
        self.db_consulta(query, (nombre,))  #Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con éxito'.format(nombre)
        self.get_productos()  # Actualizar la tabla de productos

    def edit_producto(self):
        self.mensaje['text'] = ''  # ensaje inicialmente vacio
        try:
            self.listaProductos.item(self.listaProductos.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.listaProductos.item(self.listaProductos.selection())['text']
        old_precio = self.listaProductos.item(self.listaProductos.selection())['values'][0]  # El precio se encuentra dentro de una lista
        old_categoria = self.listaProductos.item(self.listaProductos.selection())['values'][1]
        old_stock = self.listaProductos.item(self.listaProductos.selection())['values'][2]
        # Ventana nueva (editar producto)
        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana
        self.ventana_editar.resizable(1, 1)  # Activar la redimension de la ventana. Paradesactivarla: (0, 0)
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico')  # Icono de la ventana
        titulo = Label(self.ventana_editar)
        titulo.grid(column=0, row=0)
        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))
        #frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ")  #Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)  # Posicionamiento a traves de grid
        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly')
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ")
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ")  #Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0)  # Posicionamiento a traves de grid
        #Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio), state='readonly')
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ")
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoria antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoría antigua: ")
        self.etiqueta_categoria_antigua.grid(row=6, column=0)
        # Entry Categoria antigua
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria), state='readonly')
        self.input_categoria_antigua.grid(row=6, column=1)

        # Label Categoría nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoría nueva: ")
        self.etiqueta_categoria_nueva.grid(row=7, column=0)
        # Entry Categoría nueva (texto que si se podra modificar)
        self.input_categoria_nueva = Entry(frame_ep)
        self.input_categoria_nueva.grid(row=7, column=1)

        # Label Stock Antiguo
        self.etiqueta_stock_antigua = Label(frame_ep, text="Stock antiguo: ")
        self.etiqueta_stock_antigua.grid(row=8, column=0)
        # Entry Sock Antiguo
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock), state='readonly')
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label Stock Nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ")
        self.etiqueta_stock_nuevo.grid(row=9, column=0)
        # Entry Stock Nuevo (texto que si se podra modificar)
        self.input_stock_nuevo = Entry(frame_ep)
        self.input_stock_nuevo.grid(row=9, column=1)


        # Boton Actualizar Producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
                                           command=lambda:
                                           self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                     self.input_nombre_antiguo.get(),
                                                                     self.input_precio_nuevo.get(),
                                                                     self.input_precio_antiguo.get(),
                                                                     self.input_categoria_nueva.get(),
                                                                     self.input_categoria_antigua.get(),
                                                                     self.input_stock_nuevo.get(),
                                                                     self.input_stock_antiguo.get()))
        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_categoria, antigua_categoria, nuevo_stock, antiguo_stock):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ? WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ?'
        if nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':

            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (antiguo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock == '':
            parametros = (nuevo_nombre, nuevo_precio, antigua_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre == '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (antiguo_nombre, antiguo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria != '' and nuevo_stock == '':
            parametros = (nuevo_nombre, antiguo_precio, nueva_categoria, antiguo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre == '' and nuevo_precio != '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (antiguo_nombre, nuevo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        elif nuevo_nombre != '' and nuevo_precio == '' and nueva_categoria == '' and nuevo_stock != '':
            parametros = (nuevo_nombre, antiguo_precio, antigua_categoria, nuevo_stock, antiguo_nombre, antiguo_precio, antigua_categoria, antiguo_stock)
            producto_modificado = True

        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado'.format(antiguo_nombre) #Mostrar mensaje para el usuario

if __name__ == "__main__":
    # inicializamos la ventana, tipo calculadora de windows
    # Tk() es el constructor de nuestra ventana gráfica.
    root = Tk()  # instacia de la ventana principal
    app = Producto(root)  # Creamos un objeto de la clase producto y le pasamos la ventana gráfica(root)
    root.mainloop()  # a la variable anterior le ejecutamos el comando mainloop, para que la ventana se quede abierta hasta que el usuario la cierre pulsando por ejemplo x