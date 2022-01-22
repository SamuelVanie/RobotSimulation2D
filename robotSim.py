from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, radians
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def btn_clicked():
    print("Vous avez cliqué sur le bouton")

# Passage des coordonnées de R1 vers R0
def coord_un(A):
    global entry1
    global entry4

    teta1 = float(entry4.get())
    l0 = float(entry1.get())
    teta1 = radians(teta1)

    matricePassage = np.array([[cos(teta1), -sin(teta1), 0, l0],
        [sin(teta1), cos(teta1), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    return np.dot(matricePassage, A)

# Passage des coordonnées de R2 vers R0
def coord_zero(A):
    global entry1
    global matricePassage2
    global entry2
    global entry4
    global entry5
    
    teta1 = float(entry4.get())
    teta2 = float(entry5.get())
    teta1 = radians(teta1) 
    teta2 = radians(teta2) 

    l0 = float(entry1.get())
    l1 = float(entry2.get())

    matricePassage2 = np.array([[cos(teta1+teta2), -sin(teta1+teta2), 0, l1*cos(teta1)+l0],
                            [sin(teta1+teta2), cos(teta1+teta2), 0, l1*sin(teta1)],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]
    ])

    return np.dot(matricePassage2, A)

# Passage inverse, coordonnées de R0 vers R2
def coord_inv_zero(A):
    global matricePassage2
    matriceInvPassage = np.linalg.inv(matricePassage2)

    return np.dot(matriceInvPassage, A)


def dessiner():
    global window
    global entry3
    global entry2
    global entry1

    figure = plt.Figure(figsize=(6,5), dpi=100)

    # Détermination des coordonnées des points
    A2 = coord_un(np.array([[float(entry2.get())], [0], [0], [1]]))
    A1 = np.array([[float(entry1.get())], [0], [0], [1]])
    A = coord_zero(np.array([[float(entry3.get())], [0], [0], [1]]))

    ax = figure.add_subplot(111)
    ax.invert_xaxis()
    #ax.axis('off')
    ax.plot(A[1], A[0], marker='o')
    ax.plot(0, 0, marker='o')
    ax.plot(A1[1], A1[0], marker='o')
    ax.plot(A2[1], A2[0], marker='o')


    # Dessin des lignes
    ax.plot([A1[1],0], [A1[0], 0])
    ax.plot([A1[1], A2[1]], [A1[0], A2[0]])
    ax.plot([A2[1], A[1]], [A2[0], A[0]])

    chart_type = FigureCanvasTkAgg(figure, master=window)
    chart_type.get_tk_widget().place(x = 380, y = 105, width=380+159, height=105+223)


window = Tk()
window.title('Simulation Robot 2D')

window.geometry("1300x680")
window.configure(bg = "#484041")

# Création du canvas principal
canvas = Canvas(
    window,
    bg = "#484041",
    height = 680,
    width = 1300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
# Mettre le canvas sur toute l'etendue de la fenêtre
canvas.place(x = 0, y = 0)

# Ajout du textBox de debogage
entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    649.5, 571.0, # Position sur le canvas
    image = entry0_img)

entry0 = Text(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

# Placement de la zone de texte
entry0.place(
    x = 417.0, y = 485,
    width = 465.0,
    height = 170)


# Rectangle sur lequel on va dessiner le robot
rect = canvas.create_rectangle(
    380, 105, 380+539, 105+328,
    fill = "#ededed",
    outline = "")



# Choix de l'image de fond sur lequel on place toutes les composantes
background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    649.5, 339.5,
    image=background_img)

# Lieu pour insérer le texte
entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    262.5, 212.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry1.place(
    x = 249.0, y = 203, # Premier Entry
    width = 27.0,
    height = 16)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    262.5, 240.5,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry2.place(
    x = 248.5, y = 233, # deuxième Entry
    width = 28.0,
    height = 13)

entry3_img = PhotoImage(file = f"img_textBox3.png")
entry3_bg = canvas.create_image(
    262.5, 269.0,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry3.place(
    x = 249.0, y = 261, # Troisième Entry
    width = 27.0,
    height = 14)

entry4_img = PhotoImage(file = f"img_textBox4.png")
entry4_bg = canvas.create_image(
    262.5, 343.5,
    image = entry4_img)

entry4 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry4.place(
    x = 249.0, y = 335, # Quatrième Entry
    width = 27.0,
    height = 15)

entry5_img = PhotoImage(file = f"img_textBox5.png")
entry5_bg = canvas.create_image(
    262.5, 378.5,
    image = entry5_img)

entry5 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry5.place(
    x = 249.0, y = 370, # Cinquième Entry
    width = 27.0,
    height = 15)

entry6_img = PhotoImage(file = f"img_textBox6.png")
entry6_bg = canvas.create_image(
    262.5, 459.5,
    image = entry6_img)

entry6 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry6.place(
    x = 249.0, y = 451, # Sixième Entry
    width = 27.0,
    height = 15)

entry7_img = PhotoImage(file = f"img_textBox7.png")
entry7_bg = canvas.create_image(
    262.5, 491.5,
    image = entry7_img)

entry7 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry7.place(
    x = 248.5, y = 484, # Septième Entry
    width = 28.0,
    height = 13)

entry8_img = PhotoImage(file = f"img_textBox8.png")
entry8_bg = canvas.create_image(
    262.5, 564.0,
    image = entry8_img)

entry8 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry8.place(
    x = 249.0, y = 556, # Huitième Entry
    width = 27.0,
    height = 14)

entry9_img = PhotoImage(file = f"img_textBox9.png")
entry9_bg = canvas.create_image(
    262.5, 601.5,
    image = entry9_img)

entry9 = Entry(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

entry9.place(
    x = 248.5, y = 594, # Neuvième Entry
    width = 28.0,
    height = 13)

img0 = PhotoImage(file = f"img0.png") # Image du bouton DEMO
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 1040, y = 142,
    width = 140,
    height = 38)

img1 = PhotoImage(file = f"img1.png") # Image du bouton DESSINER
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = dessiner,
    relief = "flat")

b1.place(
    x = 1039, y = 201,
    width = 141,
    height = 38)

img2 = PhotoImage(file = f"img2.png") # Image du bouton SIMULER
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 1039, y = 261,
    width = 141,
    height = 38)

img3 = PhotoImage(file = f"img3.png") # Image du bouton NOUVEAU
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 1039, y = 321,
    width = 141,
    height = 37)

img4 = PhotoImage(file = f"img4.png") # Image du bouton QUITTER
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b4.place(
    x = 1040, y = 380,
    width = 140,
    height = 39)

window.resizable(False, False)
window.mainloop()
