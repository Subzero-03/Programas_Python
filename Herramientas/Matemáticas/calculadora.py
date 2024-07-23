import tkinter as tk
from tkinter import ttk
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora Científica")
        self.geometry("400x700")
        self.configure(bg="#000000")

        # Estilo para botones y pantalla
        self.style = ttk.Style(self)
        self.style.configure("TButton",
                             font=("Helvetica", 16),
                             relief="flat",
                             foreground="#FF9500",  # Naranja para botones importantes
                             background="#3C3C3C",  # Gris oscuro para el fondo del botón
                             borderwidth=0,         # Eliminar borde para suavizar
                             padding=15)

        # Map para el estilo de los botones
        self.style.map("TButton",
                       foreground=[('pressed', 'white'), ('active', 'white')],
                       background=[('pressed', '!disabled', '#555555'), ('active', '#555555')])

        self.expression = ""
        self.input_text = tk.StringVar()

        self.basic_buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('C', 5, 0), ('(', 5, 1), (')', 5, 2)
        ]

        self.create_widgets()
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Frame de entrada
        input_frame = ttk.Frame(self, style="TButton")
        input_frame.pack(expand=True, fill="both")

        # Campo de entrada
        input_field = ttk.Entry(input_frame, font=('Helvetica', 24), textvariable=self.input_text, state="readonly", justify="right")
        input_field.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, sticky=tk.NSEW)

        # Frame de botones
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(expand=True, fill="both")

        # Crear botones básicos
        self.create_buttons(self.basic_buttons)

    def create_buttons(self, buttons):
        # Limpiar los botones anteriores
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for (text, row, col, *colspan) in buttons:
            self.create_button(text, row, col, colspan[0] if colspan else 1)

    def create_button(self, text, row, col, colspan=1):
        # Crear un botón con el estilo definido
        frame = tk.Frame(self.button_frame, bg="#000000")
        frame.grid(row=row, column=col, columnspan=colspan, sticky=tk.NSEW, padx=5, pady=5)

        # Crear un botón
        button = tk.Button(frame, text=text, font=("Helvetica", 16), fg="#FF9500", bg="#3C3C3C",
                           relief="flat", command=lambda b=text: self.on_button_click(b),
                           width=2, height=1)
        button.place(relwidth=1, relheight=1, anchor='nw', bordermode='inside')

        # Ajustar tamaño y disposición
        self.button_frame.grid_rowconfigure(row, weight=1)
        self.button_frame.grid_columnconfigure(col, weight=1)

    def on_button_click(self, button):
        print(f"Button clicked: {button}")  # Debugging message
        try:
            if button == "=":
                self.evaluate_expression()
            elif button == "C":
                self.clear_expression()
            elif button == "⌫":
                self.backspace_expression()
            elif button == "√":
                self.calculate_square_root()
            elif button == "xʸ":
                self.expression += "**"
                self.input_text.set(self.expression)
            elif button == "sin":
                self.expression += "math.sin("
                self.input_text.set(self.expression)
            elif button == "cos":
                self.expression += "math.cos("
                self.input_text.set(self.expression)
            elif button == "tan":
                self.expression += "math.tan("
                self.input_text.set(self.expression)
            elif button == "ln":
                self.expression += "math.log("
                self.input_text.set(self.expression)
            elif button == "lg":
                self.expression += "math.log10("
                self.input_text.set(self.expression)
            elif button == "π":
                self.expression += str(math.pi)
                self.input_text.set(self.expression)
            elif button == "e":
                self.expression += str(math.e)
                self.input_text.set(self.expression)
            elif button == "x!":
                try:
                    self.expression = str(math.factorial(eval(self.expression)))
                except Exception as e:
                    print(f"Error calculating factorial: {e}")  # Debugging message
                    self.expression = "Error"
                self.input_text.set(self.expression)
            elif button == "1/x":
                try:
                    self.expression = str(1 / eval(self.expression))
                except Exception as e:
                    print(f"Error calculating reciprocal: {e}")  # Debugging message
                    self.expression = "Error"
                self.input_text.set(self.expression)
            elif button == "deg":
                self.expression += "math.degrees("
                self.input_text.set(self.expression)
            else:
                self.expression += button
                self.input_text.set(self.expression)
        except Exception as e:
            print(f"Unhandled error in on_button_click: {e}")  # Debugging message

    def evaluate_expression(self):
        try:
            self.expression = str(eval(self.expression))
        except Exception as e:
            print(f"Error evaluating expression: {e}")  # Debugging message
            self.expression = "Error"
        self.input_text.set(self.expression)

    def clear_expression(self):
        self.expression = ""
        self.input_text.set(self.expression)

    def backspace_expression(self):
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)

    def calculate_square_root(self):
        try:
            self.expression = str(math.sqrt(eval(self.expression)))
        except Exception as e:
            print(f"Error calculating square root: {e}")  # Debugging message
            self.expression = "Error"
        self.input_text.set(self.expression)

    def on_resize(self, event):
        # Ajustar los botones entre modo básico y científico
        print(f"Resizing to width: {self.winfo_width()}")  # Debugging message

if __name__ == "__main__":
    try:
        app = Calculator()
        app.mainloop()
    except Exception as e:
        print(f"Unhandled exception: {e}")  # Debugging message
