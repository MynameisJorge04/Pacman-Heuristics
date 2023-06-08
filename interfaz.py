import subprocess
import tkinter as tk
from PIL import Image, ImageTk

def ejecutar_jugador():
    comando = "python pacman.py --layout smallClassic"
    subprocess.Popen(comando, shell=True)

def ejecutar_maquina():
    comando = "python pacman.py -l mediumMaze -z 1 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic"
    subprocess.Popen(comando, shell=True)

root = tk.Tk()
root.title("Pacman")
root.geometry("1280x640")

# cargar la imagen de fondo
imagen = Image.open("fondo.jpg")
root.imagen_tk = ImageTk.PhotoImage(imagen)  # asignar a root

# poner la imagen de fondo
canvas = tk.Canvas(root, width=1280, height=640)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=root.imagen_tk, anchor="nw")  # usar root.imagen_tk

# crear los botones, hacerlos más grandes y centrarlos en la ventana
boton_jugador = tk.Button(root, text="Jugador", command=ejecutar_jugador, height = 2, width = 25,
                          bg='blue', fg='white', font=('Helvetica', '20'))
boton_maquina = tk.Button(root, text="Máquina", command=ejecutar_maquina, height = 2, width = 25,
                          bg='red', fg='white', font=('Helvetica', '20'))

canvas.create_window(640, 240, window=boton_jugador)
canvas.create_window(640, 400, window=boton_maquina)

root.mainloop()
