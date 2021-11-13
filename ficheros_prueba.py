
from tkinter import messagebox as MessageBox
from tkinter import Tk, Label, Button, Frame, messagebox, filedialog, ttk, Scrollbar, VERTICAL, HORIZONTAL, Toplevel, \
    StringVar, Entry
import pandas as pd
import sys

ventana = Tk()
ventana.config(bg='black')
ventana.geometry('600x400')
ventana.minsize(width=600, height=400)

ventana.columnconfigure(0, weight=25)
ventana.rowconfigure(0, weight=25)
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(1, weight=1)

frame1 = Frame(ventana, bg='gray26')
frame1.grid(column=0, row=0, sticky='nsew')
frame2 = Frame(ventana, bg='gray26')
frame2.grid(column=0, row=1, sticky='nsew')





frame1.columnconfigure(0, weight=1)
frame1.rowconfigure(0, weight=1)

frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(0, weight=1)

frame2.columnconfigure(1, weight=1)
frame2.rowconfigure(0, weight=1)

frame2.columnconfigure(2, weight=1)
frame2.rowconfigure(0, weight=1)

frame2.columnconfigure(3, weight=2)
frame2.rowconfigure(0, weight=1)


frame2.columnconfigure(4, weight=2)
frame2.rowconfigure(0, weight=1)




def abrir_archivo():
    global ruta  # GLOBAL porque las distintas funciones tienen que acceder a la ruta del archivo
    ruta = filedialog.askopenfilename(initialdir='/',
                                      title='Selecione archivo',
                                      filetype=(('csv files', '*.csv*'), ('All files', '*.*')))
    if ruta == '':
        sys.exit()
    datos_csv()


def datos_csv():
    global listaFilas
    listaFilas = []  # VARIABLE GLOBAL PARA GUARDAR EL NUMERO DE FILAS, SE USARA PARA LA FUNCION DE BORRAR Y MODIFICAR
    datos_obtenidos = ruta
    try:
        archivoCSV = r'{}'.format(datos_obtenidos)

        df = pd.read_csv(archivoCSV)


    except ValueError:
        messagebox.showerror('Informacion', 'Formato incorrecto')

    except FileNotFoundError:
        messagebox.showerror('Informacion', 'Archivo no encontrado')
    except UnboundLocalError:
        pass

    Limpiar()  # si no se sobrescribe la tabla

    tabla['column'] = list(df.columns)
    tabla['show'] = "headings"  # encabezado

    for columna in tabla['column']:
        tabla.heading(columna, text=columna)

    df_fila = df.to_numpy().tolist()
    numFila = 1  # SE INICIALIZA LA VARIABLE QUE GUARDA LAS FILAS (NUMERO)
    for fila in df_fila:

        tabla.insert('', 'end', values=fila)
        listaFilas.append(numFila)
        numFila += 1


def Limpiar():
    tabla.delete(*tabla.get_children())



def borrar():
    """
    FUNCION QUE ES LLAMADA CUANDO SE LE DA AL BOTON DE BORRAR, SE LE PREGUNTA AL USUARIO POR EL NUMERO DE LA FILA QUE
    QUIERE BORRAR, SI LE DA A QUE SI, SE LLAMA A UN FUNCION QUE BORRA LA FILA SELCCIONADA
    """

    def confirmar_borrado():
        """
        FUNCION QUE BORRA EL REGISTRO INDICADO POR EL USUARIO, LA FUNCION LEE ELARCHIVO Y CARGA TODAS LAS LINEAS
        EN UNA LISTA, SE EXTRAE LA LINEA QUE QUIERE BORRAR EL USUARIO Y SE VUELVE A ESCRIBIR EL ARCHIVO

        """
        try:
            resultado = MessageBox.askquestion("Eliminar",
                                               "¿Está seguro de borrar la fila seleccionada?")
            if resultado == "yes":


                f = open(ruta, "r")
                lineas_anteriores = f.readlines()  # leer todo el archivo antes de borrarlo
                f.close()
                # POSICION O LINEA QUE TIENE QUE BORRAR

                linea_para_borrar = lineas_anteriores[int(comboExample.get()) ]  # EXTRAE  LA LINEA A BORRAR, EMPIEZA EN 0
                lineas_anteriores.remove(linea_para_borrar)
                f2 = open(ruta, "w")
                for linea in lineas_anteriores:
                    f2.write(linea)
                f2.close()

                datos_csv()  # SE LLAMA A LA FUNCION PARA QUE ACTUALIZE LA TABLA
                ventanaBorrar.destroy()
        except IndexError:
            MessageBox.showinfo("Error", "Numero de Fila no correcto!")



    ventanaBorrar = Toplevel(ventana)
    ventanaBorrar.geometry("400x400")
    ventanaBorrar.title("Borrar Persona")
    ventanaBorrar.resizable(False, False)
    ventanaBorrar.config(background="#213141")
    Label(ventanaBorrar, text="Introduce Datos", font=("Cambria", 14), bg="#56CD63", fg="black",
                             width="500",
                             height="2").pack()

    # Labels correspondientes
    numFila = Label(ventanaBorrar, text="Numero de fila", bg="#FFEEDD")
    numFila.place(x=22, y=70)

    # guardar info del usario
    numFila = StringVar()


    entrada_nombre = Entry(ventanaBorrar, textvariable=numFila, width="20")
    entrada_nombre.place(x=22, y=100)

    comboExample = ttk.Combobox(ventanaBorrar,
                                values= listaFilas,
                                state = "readonly")
    comboExample.place(x = 22, y = 100)

    # BOTON DE BORRAR UNA  PERSONA
    botonAñadirPersona = Button(ventanaBorrar, text="BORRAR", width="15", height="2",
                                command= confirmar_borrado, bg="#00CD63")
    botonAñadirPersona.place(x=20, y=150)



def modificar():
    """
    FUNCION PARA MODIFICAR UN REGISTRO, PRIMERO SE SELECCIONA EL REGISTRO Y POSTERIORMENTE
    SE LE PIDE AL USUARIO EL LOS NUEVOS DATOS PARA MODIFICAT
    :return:
    """


    try:
        def modificarRegistro():

            try:
                resultado = MessageBox.askquestion("Eliminar",
                                                   "¿Está seguro de modificar la fila seleccionada?")
                if resultado == "yes":

                    lineaModificada = [textoNombre.get(), textoApellidos.get(), texxtoTelefono.get()]

                    f = open(ruta, "r")
                    lineas_anteriores = f.readlines()  # leer todo el archivo antes de borrarlo
                    f.close()
                    # POSICION O LINEA QUE TIENE QUE MODIFICAR
                    # REEMPLAZA LA FILA SELECCIONADA EN EL COMBO POR LOS VALORES DE LAS CASILLAS DE TEXTO
                    lineas_anteriores[int(comboExample.get())] = textoNombre.get() + ',' + textoApellidos.get() +',' + texxtoTelefono.get() + '\n'

                    f2 = open(ruta, "w")
                    for linea in lineas_anteriores:
                        f2.write(linea)
                    f2.close()

                    datos_csv()  # SE LLAMA A LA FUNCION PARA QUE ACTUALIZE LA TABLA
                    ventanaModificar.destroy()
            except IndexError:
                MessageBox.showinfo("Error", "Numero de Fila no correcto!")




        # Crear una nueva ventana que hereda de la principal
        ventanaModificar = Toplevel(ventana)
        ventanaModificar.geometry("400x400")
        ventanaModificar.title("Añadir Persona")
        ventanaModificar.resizable(False, False)
        ventanaModificar.config(background="#213141")
        titulo_principal = Label(ventanaModificar, text="Introduce Datos", font=("Cambria", 14), bg="#56CD63", fg="black",
                                 width="500",
                                 height="2").pack()

        # Labels correspondientes
        comboExample = ttk.Combobox(ventanaModificar,
                                    values= listaFilas,
                                    state = "readonly")
        comboExample.place(x = 22, y = 70)
        textoNombre = Label(ventanaModificar, text="Nombre", bg="#FFEEDD")
        textoNombre.place(x=22, y=100)
        textoApelldio = Label(ventanaModificar, text="Apellido", bg="#FFEEDD")
        textoApelldio.place(x=22, y=160)
        textoTelefono = Label(ventanaModificar, text="Telefono", bg="#FFEEDD")
        textoTelefono.place(x=22, y=220)

        # guardar info del usario
        textoNombre = StringVar()
        textoApellidos = StringVar()
        texxtoTelefono = StringVar()

        entrada_nombre = Entry(ventanaModificar, textvariable=textoNombre, width="20")
        entrada_apellidos = Entry(ventanaModificar, textvariable=textoApellidos, width="20")
        entrada_telefono = Entry(ventanaModificar, textvariable=texxtoTelefono, width="20")

        entrada_nombre.place(x=22, y=130)
        entrada_apellidos.place(x=22, y=190)
        entrada_telefono.place(x=22, y=250)

        # BOTON DE AÑADIR UNA NUEVA PERSONA
        botonModificarPersona = Button(ventanaModificar, text="Añadir Persona a la BBDD", width="30", height="2",
                                       command= modificarRegistro, bg="#00CD63")
        botonModificarPersona.place(x=22, y=320)

        # BOTON DE AÑADIR UNA NUEVA PERSONA
        botonModificarPersona = Button(ventanaModificar, text="Modificar Persona de la BBDD", width="30", height="2",
                                    command=modificarRegistro, bg="#00CD63")
        botonModificarPersona.place(x=22, y=320)

    except NameError:
        MessageBox.showinfo("Error", "Tienes que abrir un fichero antes!")
        ventanaModificar.destroy()


def añadir():
    """
    FUNCION QUE OCURRE CUANDO SE LE DA AL BOTON DE AÑADIR, ABRE UNA NUEVA VENTANA Y CUANDO SE LE DA AL BOTON
     DE AÑADIR LLAMA A LA FUNCION
    ESCRIBIR PARA QUE AÑADA UNA NUEVA PERSONA
    """

    try:

        def escribir():
            """
            ESCRIBI EN EL ARCHIVO ABIERTO UNA NUEVA PERSONA
            :return:
            """
            try:
                with open(ruta, 'a') as file:
                    file.write('\n')
                    file.write(textoNombre.get() + ',')
                    file.write(textoApellidos.get() + ',')
                    file.write(texxtoTelefono.get())

                ventanaAñadir.destroy()
                datos_csv()  # para refrescar la tabla y que se vea el elemento añadio

            except NameError:
                MessageBox.showinfo("Error", "Tiene que abrir un fichero antes!")


        # Crear una nueva ventana que hereda de la principal
        ventanaAñadir = Toplevel(ventana)
        ventanaAñadir.geometry("400x400")
        ventanaAñadir.title("Añadir Persona")
        ventanaAñadir.resizable(False, False)
        ventanaAñadir.config(background="#213141")
        titulo_principal = Label(ventanaAñadir, text="Introduce Datos", font=("Cambria", 14), bg="#56CD63", fg="black", width="500",
                                 height="2").pack()


        # Labels correspondientes
        textoNombre = Label(ventanaAñadir, text="Nombre", bg="#FFEEDD")
        textoNombre.place( x=22, y=70)
        textoApelldio = Label(ventanaAñadir, text="Apellido", bg="#FFEEDD")
        textoApelldio.place( x=22, y=130)
        textoTelefono = Label(ventanaAñadir, text="Telefono", bg="#FFEEDD")
        textoTelefono.place(x=22, y=190)

        # guardar info del usario
        textoNombre = StringVar()
        textoApellidos = StringVar()
        texxtoTelefono = StringVar()

        entrada_nombre = Entry(ventanaAñadir, textvariable=textoNombre, width="20")
        entrada_apellidos = Entry(ventanaAñadir, textvariable=textoApellidos, width="20")
        entrada_telefono = Entry(ventanaAñadir, textvariable=texxtoTelefono, width="20")

        entrada_nombre.place(x=22, y=100)
        entrada_apellidos.place(x=22, y=160)
        entrada_telefono.place(x=22, y=220)

        # BOTON DE AÑADIR UNA NUEVA PERSONA
        botonModificarPersona = Button(ventanaAñadir, text="Añadir Persona a la BBDD", width="30", height="2",
                                    command=escribir, bg="#00CD63")
        botonModificarPersona.place(x=22, y=320)

    except NameError:
        ventanaAñadir.destroy()
        MessageBox.showinfo("Error", "Tienes que abrir un fichero antes!")




# ------------------------- OBJETOS PRINCIPALES  Y BOTONES PRINCIPALES -----------------------


tabla = ttk.Treeview(frame1, height=10)

tabla.grid(column=0, row=0, sticky='nsew')

ladox = Scrollbar(frame1, orient=HORIZONTAL, command=tabla.xview)
ladox.grid(column=0, row=1, sticky='ew')

ladoy = Scrollbar(frame1, orient=VERTICAL, command=tabla.yview)
ladoy.grid(column=1, row=0, sticky='ns')

tabla.configure(xscrollcommand=ladox.set, yscrollcommand=ladoy.set)

estilo = ttk.Style(frame1)
estilo.theme_use('clam')
estilo.configure(".", font=('Arial', 14), foreground='red2')
estilo.configure("Treeview", font=('Helvetica', 12), foreground='black', background='white')
estilo.map('Treeview', background=[('selected', 'green2')], foreground=[('selected', 'black')])

botonAbrir = Button(frame2, text='Abrir', bg='green2', command=abrir_archivo)
botonAbrir.grid(column=0, row=0, sticky='nsew', padx=10, pady=10)


botonLimpiar = Button(frame2, text='Limpiar', bg='red', command=Limpiar)
botonLimpiar.grid(column=1, row=0, sticky='nsew', padx=10, pady=10)

botonAñadir = Button(frame2, text='Añadir', bg='blue', command= añadir)
botonAñadir.grid(column=2, row=0, sticky='nsew', padx=10, pady=10)

botonBorrar = Button(frame2, text='Borrar', bg='pink', command= borrar)
botonBorrar.grid(column=3, row=0, sticky='nsew', padx=10, pady=10)

botonModificar = Button(frame2, text='Modificar', bg='Yellow', command= modificar)
botonModificar.grid(column=4, row=0, sticky='nsew', padx=10, pady=10)


ventana.mainloop()