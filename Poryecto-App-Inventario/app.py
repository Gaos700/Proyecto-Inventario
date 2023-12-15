from tkinter import*
from tkinter import ttk

import sqlite3

class product:
    db_name = 'database_app.db'

    def __init__(self,window):
        self.wind = window
        self.wind.title('Aplicacion Inventario')

        #contenedor frame
        frame= LabelFrame(self.wind, text='Registra un nuevo producto')
        frame.grid(row=0, column= 0, columnspan= 3, pady=20)

        #nombre input
        Label(frame, text='Nombre').grid(row =1, column =0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row= 1, column = 1)

        #Precio Input
        Label(frame, text='Precio').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        #Cantidad Input
        Label(frame, text='Cantidad').grid(row=3, column=0)
        self.cant = Entry(frame)
        self.cant.grid(row=3, column=1)

        #Talla Input

        Label(frame, text='Talla').grid(row=4, column=0)
        self.talla = Entry(frame)
        self.talla.grid(row=4, column=1)

        #Boton para Agregar

        ttk.Button(frame, text='Añadir inventario', command=self.add_inventario).grid(row=5, columnspan=2, sticky= W +E)

        #Boton para Eliminar

        ttk.Button(frame, text='Eliminar', command= self.delete).grid(row=7, columnspan=2, sticky=W +E)
        ttk.Button(frame, text='Editar', command= self.edit).grid(row=8, columnspan=2, sticky=W +E)

        #Atributo mensajes
        self.message = Label(text='', fg='red')
        self.message.grid(row=8, column=0, columnspan= 3, sticky=W +E)

        # Tabla
        self.tree = ttk.Treeview(height = 10, columns =('#1', '#2', '#3', '#4'), show='headings')
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#1', text='Nombre', anchor=CENTER)
        self.tree.heading('#2', text='Precio', anchor=CENTER)
        self.tree.heading('#3', text='Cantidad', anchor=CENTER)
        self.tree.heading('#4', text='Talla', anchor=CENTER)
        
        # Llenando las filas
        self.get_product()

    # Esta funcion ejecuta las query en las demas funciones que la necesiten, necesitando el string de la query y los parametros (opcionales)
    def run_query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result
    
    def get_product(self):
        # Limpiando la tabla
        records = self.tree.get_children()
        for elementos in records:
            self.tree.delete(elementos)
        # Mostrando los datos en la tabla
        query = 'SELECT nombre, precio,cantidad, talla FROM productos ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values= row)
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
    def add_inventario(self):
        if self.validation():
            query = 'INSERT INTO productos VALUES (NULL, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.price.get(),self.cant.get(), self.talla.get())
            self.run_query(query,parameters)
            self.message['text'] = 'El Producto {} ha sido añadido satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0,END)
            self.cant.delete(0,END)
            self.talla.delete(0,END)
        else:
            self.message['text'] = 'Ingrese un Nombre y un Precio'
        self.get_product()
    def delete(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Por favor seleccione un producto'
            return
        self.message['text']= ''
        name = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM productos WHERE nombre = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'El Producto {} ha sido eliminado satisfactoriamente'.format(name)
        self.get_product()
    def edit(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Porfavor seleccione un Producto'
        name= self.tree.item(self.tree.selection())['values'][0]
        cantidad = self.tree.item(self.tree.selection())['values'][2]
        antiguo_precio = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind = Toplevel()
        self.edit_wind.title= 'Editar Producto'

        #Antigua Cantidad
        Label(self.edit_wind, text= 'Cantidad Actual: ').grid(row= 0, column= 1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value= cantidad), state='readonly').grid(row=0, column=2)

        #Nuevo Cantidad
        Label(self.edit_wind, text='Cantidad Nueva').grid(row=1, column=1)
        new_cantidad = Entry(self.edit_wind)
        new_cantidad.grid(row=1, column=2)

        #Antiguo Precio
        Label(self.edit_wind, text= 'Precio Actual: ').grid(row= 2, column= 1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value= antiguo_precio), state='readonly').grid(row=2, column=2)

        #Nuevo Precio
        Label(self.edit_wind, text='Precio Nuevo').grid(row=3, column=1)
        new_precio = Entry(self.edit_wind)
        new_precio.grid(row=3, column=2)

        Button(self.edit_wind, text='Actualizar', command= lambda: self.edit_records(new_cantidad.get(), cantidad, new_precio.get(), antiguo_precio,name)).grid(row=4, column=2, sticky=W)

    def edit_records(self, new_cantidad, cantidad, new_precio, antiguo_precio, name):
        query = 'UPDATE productos SET cantidad = ?, precio = ? WHERE nombre = ? AND cantidad = ? AND precio = ?'
        parameters = (new_cantidad,new_precio,name, cantidad,antiguo_precio)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.get_product()


if __name__ == '__main__':
    window = Tk()
    aplication = product(window)
    window.mainloop()