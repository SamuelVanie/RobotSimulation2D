from tkinter import *
from playsound import playsound
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from math import cos, degrees, sin, atan2, atan, radians, sqrt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import multiprocessing


"""
quitter
@desc: quitter le programme
"""
def quitter():
    global window
    playsound('./Music/end.wav')
    time.sleep(0.4)
    window.destroy()


"""
demo
@desc: 
    initialise les données avec des valeurs par défaut
"""
def demo():

    global entry0
    global entry1
    global entry2
    global entry3
    global entry4
    global entry5
    global entry6
    global entry7
    global entry8
    global entry9

    entry0.insert(END, str("\nDes variables de démo ont été définies"))
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)
    entry7.delete(0, END)
    entry8.delete(0, END)
    entry9.delete(0, END)

    entry1.insert(0, str(3.5))
    entry2.insert(0, str(3.0))
    entry3.insert(0, str(3.0))
    entry4.insert(0, str(55.0))
    entry5.insert(0, str(75.0))
    entry6.insert(0, str(0.0))
    entry7.insert(0, str(1.0))
    entry8.insert(0, str(10))
    entry9.insert(0, str(10))

"""
nouveau
reinitialise les données
"""
def nouveau():
    global entry0
    global entry1
    global entry2
    global entry3
    global entry4
    global entry5
    global entry6
    global entry7
    global entry8

    #insertion message log
    entry0.insert(END, str("\nRéinitialiation des variables"))

    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)
    entry7.delete(0, END)
    entry8.delete(0, END)

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


def dessiner():
    global window
    # longueur lien 3
    global entry3
    # longueur lien 2
    global entry2
    # longueur lien 1
    global entry1
    # définition des logs
    global entry0

    entry0.insert(END, str("\nDessin du robot dans sa position initiale"))

    figure = plt.Figure(figsize=(6,5), dpi=100)

    # Détermination des coordonnées des points
    A2 = coord_un(np.array([[float(entry2.get())], [0], [0], [1]]))
    A1 = np.array([[float(entry1.get())], [0], [0], [1]])
    A = coord_zero(np.array([[float(entry3.get())], [0], [0], [1]]))

    ax = figure.add_subplot(111)
    ax.invert_xaxis()
    ax.grid()
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


def passage_repere_A1_A2_A3(l0,l1,l2,angle1,angle2) : 
    Lien_L0 = l0
    Lien_L1 = l1
    Lien_L2 = l2
    theta1 = angle1
    theta2 = angle2
    theta1=radians(theta1)
    theta2=radians(theta2)
    matrice_R1=np.array([[cos(theta1),-sin(theta1),0,Lien_L0],
                         [sin(theta1),cos(theta1),0,0],
                         [0,0,1,0],
                         [0,0,0,1]],dtype=np.float16)
    matrice_R2=np.array([[cos(theta2),-sin(theta2),0,Lien_L1],
                         [sin(theta2),cos(theta2),0,0],
                         [0,0,1,0],
                         [0,0,0,1]],dtype=np.float16)
    matrice_R0=np.dot(matrice_R1,matrice_R2)
    A_R2=np.array([[Lien_L2],[0],[0],[1]],dtype=np.float16)
    primA_R1=np.array([[Lien_L1],[0],[0],[1]],dtype=np.float16)
    primA_R0=np.dot(matrice_R1,primA_R1)
    A_R1=np.dot(matrice_R2,A_R2)
    A_R0=np.dot(matrice_R1,A_R1)
    A_0=np.array([[0],[Lien_L0],[0],[1]],dtype=np.float16)
    return A_0,primA_R0,A_R0

def calculer_teta(bx,by) :
    global entry1
    global entry2
    global entry3

    l2 = float(entry3.get())
    l1 = float(entry2.get())
    l0 = float(entry1.get())
    w=l2
    x=by
    y=l0-bx
    z1=0
    z2=-l1
    b1=2*(y*z1+x*z2)
    b2=2*(x*z1-y*z2)
    b3=w**2-x**2-y**2-z1**2-z2**2
    X=b1
    Y=b2
    Z=b3
    if(Z==0) :
        Y=-Y
        if(X>0) :
            theta1=degrees(atan(Y/X))
        elif((X<0)&(Y>=0)):
            theta1=degrees(atan(Y/X))+180
        elif((X<0)&(Y<0)):
            theta1=degrees(atan(Y/X))-180
        elif((X==0)&(Y>0)):
            theta1=90
        elif((X==0)&(Y<0)):
            theta1=-90
        elif((X==0)&(Y==0)):
            theta1=0
    else :
        contenu=X*X+Y*Y-Z*Z
        racine = sqrt(contenu)
        numSin = Z*X+Y*racine
        numCos = Z*Y-X*racine
        denom = X**2+Y**2
        cosangle = numCos/denom
        sinangle = numSin/denom
        if(cosangle>0) :
            theta1 = degrees(atan(sinangle/cosangle))
        elif((cosangle<0)&(sinangle>=0)):
            theta1 = degrees(atan(sinangle/cosangle))+180
        elif((cosangle<0)&(sinangle<0)):
            theta1 = degrees(atan(sinangle/cosangle))-180
        elif((cosangle==0)&(sinangle>0)):
            theta1=90
        elif((cosangle==0)&(sinangle<0)):
            theta1=-90
        elif((cosangle==0)&(sinangle==0)):
            theta1=0
    Y1 = by*cos(radians(theta1))+y*sin(radians(theta1))+z1
    Y2 = by*sin(radians(theta1))-y*cos(radians(theta1))+z2
    ysin=Y1/l2
    xcos=Y2/l2
    if(xcos>0) :
        theta2 = degrees(atan(ysin/xcos))
    elif((xcos<0)&(ysin>=0)):
        theta2 = degrees(atan(ysin/xcos))+180
    elif((xcos<0)&(ysin<0)):
        theta2 = degrees(atan(ysin/xcos))-180
    elif((xcos == 0)&(ysin>0)):
        theta2 = 90
    elif((xcos == 0)&(ysin<0)):
        theta2 = -90
    elif((xcos ==0)&(ysin==0)):
        theta2=0
    return theta1,theta2


def simuler():
#Definition du graphe
    global window
    global entry0
    global entry1
    global entry2
    global entry3
    global entry4
    global entry5
    global entry6
    global entry7
    global entry8
    global entry9

    entry0.insert(END, str("\nDebut de simulation"))
    entry0.insert(END, str(f"\nLa duree de la simulation est de {int(entry9.get())} secondes"))
    fig = plt.figure(figsize=(6,5),dpi=100)
    ax = fig.add_subplot(111)
    ax.grid()
    ax.invert_xaxis()
    ax.axis('off')
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_xlabel("Y")
    ax.set_ylabel("X")
    chart_type = FigureCanvasTkAgg(fig,window)
    chart_type.get_tk_widget().place(x = 380, y = 105, width=380+159, height=105+223)


    ax.clear()

    # Début du tracé
    duree = float(entry9.get())
    L0=float(entry1.get())
    L1=float(entry2.get())
    L2=float(entry3.get())
    teta1=float(entry4.get())
    teta2=float(entry5.get())
    B = (float(entry6.get()), float(entry7.get()))
    pas=int(entry8.get())
    pointsA=passage_repere_A1_A2_A3(L0,L1,L2,teta1,teta2)
    A3 = (pointsA[2][1], pointsA[2][0])
    A2 = (pointsA[1][1], pointsA[1][0])
    xDif=A3[0]-B[0]
    yDif=A3[1]-B[1]
    listeAbscisses=[]
    listeOrdonnees=[]
    listeTeta1=[]
    listeTeta2=[]
    listePointA3abscisses=[]
    listePointA3ordonnees=[]
    listePointA2abscisses=[]
    listePointA2ordonnees=[]
    
    #Ajout du point final à la liste des points à dessiner
    fi=calculer_teta(B[1],B[0])
    coord=passage_repere_A1_A2_A3(L0,L1,L2,fi[0],fi[1])
    listePointA3abscisses.append(coord[2][1])
    listePointA3ordonnees.append(coord[2][0])
    listePointA2abscisses.append(coord[1][1])
    listePointA2ordonnees.append(coord[1][0])
    
    #Fixation du repere
    fig = plt.figure(figsize=(6,5),dpi=100)
    ax = fig.add_subplot(111)
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.grid()
    ax.invert_xaxis()
    ax.set_xlabel("Y")
    ax.set_ylabel("X")
    chart_type = FigureCanvasTkAgg(fig,window)
    chart_type.get_tk_widget().place(x = 380, y = 105, width=380+159, height=105+223)

    #Segmentation en nombre de pas
    for i in range(pas-1) :
        listeAbscisses.append((i+1)*xDif/(pas)+B[0])
        listeOrdonnees.append((i+1)*yDif/(pas)+B[1])
    for i in range(pas-1) :
        fi=calculer_teta(listeOrdonnees[i],listeAbscisses[i])
        listeTeta1.append(fi[0])
        listeTeta2.append(fi[1])
    for i in range(pas-1) :
        coord=passage_repere_A1_A2_A3(L0,L1,L2,listeTeta1[i],listeTeta2[i])
        listePointA3abscisses.append(coord[2][1])
        listePointA3ordonnees.append(coord[2][0])
        listePointA2abscisses.append(coord[1][1])
        listePointA2ordonnees.append(coord[1][0])
        
    ax.clear()
    ax.invert_xaxis()
    ax.set_xlabel("Y")
    ax.grid()
    ax.set_ylabel("X")
    chart_type = FigureCanvasTkAgg(fig,window)
    chart_type.get_tk_widget().place(x = 380, y = 105, width=380+159, height=105+223)
    coord=passage_repere_A1_A2_A3(L0,L1,L2,teta1,teta2)
    ax.plot([B[0],A3[0]],[B[1],A3[1]], '--')

    for i in range(pas-1) :
        ax.plot(listeAbscisses[i],listeOrdonnees[i],'x', lw=5, color='black')
    ax.plot(B[0],B[1],'o-')
    ax.plot([0,0],[0,L0])
    x_points = [coord[0][0],coord[1][1],coord[2][1]]
    y_points = [coord[0][1],coord[1][0],coord[2][0]]
    droite, = ax.plot(x_points, y_points, 'o-')
    ax.plot(coord[2][1],coord[2][0],'o-')
    droite.set_markevery(0.3)
    droite.set_mec('orange')
    droite.set_mew('2.5')
    org, = ax.plot(coord[2][1], coord[2][0],marker="D",markersize=5)
    
    #ajout du point initiale a la liste
    dernierPoint=passage_repere_A1_A2_A3(L0,L1,L2,teta1,teta2)
    listePointA3abscisses.append(dernierPoint[2][1])
    listePointA3ordonnees.append(dernierPoint[2][0])
    listePointA2abscisses.append(dernierPoint[1][1])
    listePointA2ordonnees.append(dernierPoint[1][0])    
    k=pas


    for p in range(k+1):
        #Mise à jours des valeur
        z = multiprocessing.Process(target=playsound, args=("./Music/mouvement.wav",))
        z.start()
        x_points =[0,listePointA2abscisses[k-p],listePointA3abscisses[k-p]]
        y_points =[L0,listePointA2ordonnees[k-p],listePointA3ordonnees[k-p]] 
        droite.set_data(x_points,y_points)
        org.set_data(listePointA3abscisses[k-p],listePointA3ordonnees[k-p])
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(duree/pas)
        z.terminate()
        



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

# Création d'un popup d'aide
messagebox.showinfo("Aide", """
        DEMO -> Remplissage des cases par des variables aléatoires
        DESSINER -> Dessiner le robot dans sa situation initiale
        SIMULER -> Debuter le déplacement du robot vers la destination finale
        NOUVEAU -> Effacer toutes les données des champs
        QUITTER -> Quitter l'application
        """)

playsound('./Music/Hello.mp3')
time.sleep(1)

# Ajout du textBox de debogage
entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    649.5, 571.0, # Position sur le canvas
    image = entry0_img)

entry0 = Text(
    bd = 0,
    bg = "#ededed",
    highlightthickness = 0)

# Placement d'un scrollbar de défilement
scroll = Scrollbar(master=entry0, orient='vertical', command=entry0.yview)
scroll.pack(side=RIGHT)

entry0.configure(yscrollcommand=scroll.set)

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
    command = demo,
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
    command = simuler,
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
    command = nouveau,
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
    command = quitter,
    relief = "flat")

b4.place(
    x = 1040, y = 380,
    width = 140,
    height = 39)

window.resizable(False, False)
window.mainloop()
