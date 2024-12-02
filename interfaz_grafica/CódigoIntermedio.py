import tkinter as tk

class VentanaSecundaria:
    def __init__(self, parent, titulo):
        self.parent = parent
        self.ventana = None
        self.text_widget = None
        self.titulo = titulo

    def abrir(self, texto="Texto inicial"):
        # Si la ventana ya está abierta, no crear otra
        if self.ventana is not None and tk.Toplevel.winfo_exists(self.ventana):
            self.actualizar_texto(texto)
            return

        # Crear una ventana secundaria
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title(self.titulo)

        # Frame para contener el texto y la barra de desplazamiento
        frame = tk.Frame(self.ventana)
        frame.pack(fill="both", expand=True)

        # Crear un widget de texto con barra de desplazamiento
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.text_widget = tk.Text(
            frame,
            wrap="word",  # Ajuste de palabras
            font=("Monaco", 14),
            yscrollcommand=scrollbar.set
        )
        self.text_widget.pack(side="left", fill="both", expand=True)
        self.text_widget.insert("1.0", texto)  # Insertar texto inicial
        self.text_widget.config(state="disabled")  # Hacerlo de solo lectura

        scrollbar.config(command=self.text_widget.yview)


    def actualizar_texto(self, nuevo_texto):
        if self.text_widget is not None:
            self.text_widget.config(state="normal")  # Permitir edición temporal
            self.text_widget.delete("1.0", tk.END)  # Borrar el contenido previo
            self.text_widget.insert("1.0", nuevo_texto)  # Insertar el nuevo texto
            self.text_widget.config(state="disabled")  # Volver a hacerlo de solo lectura
