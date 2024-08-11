import turtle

# Configuración inicial de la pantalla y la tortuga
screen = turtle.Screen()
screen.bgcolor("white")
tu = turtle.Turtle()
tu.speed(5)
tu.pensize(5)

# Función para dibujar la forma de la máscara de Deadpool
def draw_mask():
    tu.penup()
    tu.goto(0, -100)
    tu.pendown()
    tu.color("red")
    tu.begin_fill()
    tu.circle(100)  # Cabeza
    tu.end_fill()

# Función para dibujar un ojo
def draw_eye(x, y):
    tu.penup()
    tu.goto(x, y)
    tu.pendown()
    tu.color("black")
    tu.begin_fill()
    tu.circle(30)  # Parte negra del ojo
    tu.end_fill()

    tu.penup()
    tu.goto(x, y + 10)
    tu.pendown()
    tu.color("white")
    tu.begin_fill()
    tu.circle(20)  # Parte blanca del ojo
    tu.end_fill()

# Dibuja la máscara de Deadpool
draw_mask()

# Dibuja los ojos de Deadpool
draw_eye(-40, 40)
draw_eye(40, 40)

# Finaliza el dibujo
tu.hideturtle()
turtle.done()
