from tkinter import *
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

############################################################

from math import cos, sin, pi, atan2
import matplotlib.pyplot as plt
import numpy as np

#creation des variable de notre probleme
L0, L1, L2, T = 0,0,0,0
class Point:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y

    def getX(self):
        return self.y

    def setX(self,x):
        self.y = x

    def getY(self):
        return self.x

    def setY(self,y):
        self.x = y
        
    def getPosition(self):
        return np.array([[self.getY()],
                         [self.getX()],
                         [0],
                         [1]])

def distance(point1,point2):
    return ((point1.getX()-point2.getX())**2 + (point1.getY()-point2.getY())**2)**0.5

def passage(theta,a):
    return np.array([[cos(theta),-sin(theta),0,a],
                     [sin(theta),cos(theta),0,0],
                     [0,0,1,0],
                     [0,0,0,1]])

def passage2(theta1,theta2,L0,L1):
    return np.array([[cos(theta1+theta2),-sin(theta1+theta2),0,L0+cos(theta1)*L1],
                     [sin(theta1+theta2),cos(theta1+theta2),0,sin(theta1)*L1],
                     [0,0,1,0],
                     [0,0,0,1]])

def radian(deg):
    return deg*pi/180

#parametres variables
def initialisationVariables(l0=3.5,l1=3,l2=3,the1=55,the2=75,x=1,y=0):
    global tableau,A0,A1,A2,A3,B,theta1,theta2,T0_1,T0_2,A,L0,L1,L2

    #parametres invariables
    L0,L1,L2 = l0, l1, l2

    A0 = Point(0,0)
    A1 = Point(0,L0)
    B = Point(x,y)

    A2 = Point(L1)
    A3 = Point(L2)

    theta1 = radian(the1)
    theta2 = radian(the2)
    T0_1 = passage(theta1, L0)
    T0_2 = passage2(theta1, theta2, L0, L1)
    A2 = Point(np.dot(T0_1,A2.getPosition())[1],np.dot(T0_1,A2.getPosition())[0])
    A3 = Point(np.dot(T0_2,A3.getPosition())[1],np.dot(T0_2,A3.getPosition())[0])
    A = A3

#Equations
def pente(point1,point2):
    return (point2.getX()[0]-point1.getX())/(point2.getY()[0]-point1.getY())

def ydroite(x):
    return pente(B,A3)*x + B.getX() - pente(B,A3)*B.getY()

#determination de theta1 et theta2
def solutiontheta1(x,y):
    W = L2
    Z1 = 0
    Z2 = -L1
    X = x
    Y = L0 - y
    B1 = 2*(Y*Z1 + X*Z2)
    B2 = 2*(X*Z1 - Y*Z2)
    B3 = W**2 - X**2 - Y**2 - Z1**2 - Z2**2
    sinustheta1 = (B3*B1 + B2*(B1**2 + B2**2 - B3**2)**0.5)/(B1**2 + B2**2)
    cosinustheta1 = (B3*B2 - B1*(B1**2 + B2**2 - B3**2)**0.5)/(B1**2 + B2**2)

    return atan2(sinustheta1,cosinustheta1)

def solutiontheta2(x,y,theta1):
    W = L2
    Z1 = 0
    Z2 = -L1
    X = x
    Y = L0 - y
    X1 = W
    X2 = W
    Y1 = X*cos(theta1) + Y*sin(theta1) + Z1
    Y2 = X*sin(theta1) - Y*cos(theta1) + Z2
    
    return atan2(Y1/X1,Y2/X2)

#pas
def pasX(n):
    return (B.getY()-A3.getY()[0])/n

def listePositionA3(n):
    X = [A3.getY()[0]]
    Y = [A3.getX()[0]]
    for i in range(n):
        X.append(A3.getY()[0]+(i+1)*pasX(n))    
        Y.append(ydroite(X[-1]))
    print("liste des abscisses", X)
    print("liste des ordonnées", Y)
    return X,Y

#affichage
#affichage des segments
def initialisationGraph():
    global root,L0,L1,L2,A0,A1,B,A2,A3,theta1,theta2,T0_1,T0_2,A2,A3,A,fig,graph,canvasRobot,monCanvas
    
    x = np.array([A0.getY(),A1.getY(),A2.getY(),A3.getY()])
    y = np.array([A0.getX(),A1.getX(),A2.getX(),A3.getX()])
    #affichage des points
    xprim = np.array([A0.getY(),A1.getY(),A2.getY(),A.getY(),B.getY()])
    yprim = np.array([A0.getX(),A1.getX(),A2.getX(),A.getX(),B.getX()])

    fig = plt.figure(figsize=(4, 4),dpi=97)
    graph = plt.subplot(1,1,1)
    #graph.axis([L1+L2+0.25, -0.25, -0.25, L0+L1+0.25])

    graph.scatter(xprim,yprim,s=100,edgecolors='black',linewidth=3)
    graph.plot(x,y,linewidth=3)
    graph.plot([0,L1+L2],[0,0],ls='--',c = 'green')
    #droite rouge
    graph.plot([B.getY(),A3.getY()[0]],[B.getX(),A3.getX()[0]],ls='--',c = 'red')
    #cadriage arriere
    graph.axis('square')

    #graph.axes().set_xlim([-0.25, L1+L2+0.25])
    #graph.axes().set_ylim([-0.25, L0+L1+0.25])

    graph.grid()

    graph.yaxis.set_ticks_position('right')
    graph.invert_xaxis()
    canvasRobot = FigureCanvasTkAgg(fig,root)
    monCanvas = canvasRobot.get_tk_widget()


#affichage des positions suivantes

def mouvement(N):
    global tab,ak,etatdeB,root,L0,L1,L2,A0,A1,B,A2,A3,theta1,theta2,T0_1,T0_2,A2,A3,A,fig,graph,canvasRobot,monCanvas

    if distance(A1,B) > L1+L2 or distance(A1,B) < abs(L1-L2):
        #etatdeB.set('B est hors d\'atteinte !!')
        print('Le point est impossible à atteindre!!')

    else:

        tab = [L0,L1,L2,theta1*180/pi,theta2*180/pi,B.getY(),B.getX()]

        positionA3 = listePositionA3(N)
        var = True

        for k in range(1,len(positionA3[0])-1):
            if ( (positionA3[0][k] - A1.getX())**2 + (positionA3[1][k] - A1.getY())**2 )**0.5 < abs(L1-L2) :
                var = False
               # etatdeB.set('Certains Pk sont hors d\'atteintes !!')
                break

        if var:
            
            #etatdeB.set('B peut être atteint !')

            for i in range(1,N+1):

                fig.clear()
                graph.clear()
                theta1 = solutiontheta1(positionA3[0][i],positionA3[1][i])
                print("teta1-", i, theta1)
                theta2 = solutiontheta2(positionA3[0][i],positionA3[1][i],theta1)
                print("teta2-", i, theta2)
                T0_1 = passage(theta1, L0)
                T0_2 = passage2(theta1, theta2, L0, L1)
                A2 = Point(np.dot(T0_1,Point(L1).getPosition())[1],np.dot(T0_1,Point(L1).getPosition())[0])
                print(A2)
                A3 = Point(np.dot(T0_2,Point(L2).getPosition())[1],np.dot(T0_2,Point(L2).getPosition())[0])
                print(A3)

                Theta11.set(str(theta1*180/pi)[:5]+'°')
                Theta22.set(str(theta2*180/pi)[:5]+'°')
                #affichage
                #affichage des segments
                x = np.array([A0.getY(),A1.getY(),A2.getY(),A3.getY()])
                y = np.array([A0.getX(),A1.getX(),A2.getX(),A3.getX()])
                #affichage des points
                xprim = np.array([A0.getY(),A1.getY(),A2.getY(),A3.getY(),A.getY(),B.getY()])
                yprim = np.array([A0.getX(),A1.getX(),A2.getX(),A3.getX(),A.getX(),B.getX()])

                fig = plt.figure(figsize=(4, 4),dpi=97)
                graph = plt.subplot(1,1,1)
                #graph.axis([0, 6, 0, 7])

                graph.scatter(xprim,yprim,s=100,edgecolors='black',linewidth=3)
                graph.plot(x,y,linewidth=3)
                graph.plot([0,L1+L2],[0,0],ls='--',c = 'grey')
                graph.plot([B.getY(),A.getY()[0]],[B.getX(),A.getX()[0]],ls='--',c = 'red')

                graph.axis('square')

                #axes = plt.axes()
                #axes.set_xlim([-0.25, L1+L2+0.25])
                #axes.set_ylim([-0.25, L0+L1+0.25])

                graph.grid()

                graph.yaxis.set_ticks_position('right')
                graph.invert_xaxis()
                canvasRobot = FigureCanvasTkAgg(fig,root)
                monCanvas = canvasRobot.get_tk_widget()
                
                graphe = monCanvas
                graphe.place(x=367,y=72)


                #ak.insert('end','X{}={}'.format(i,positionA3[1][i]))
                #ak.insert('end','\nY{}={}\n\n'.format(i,positionA3[0][i]))
                
                root.update()


B=Point()
################################################################
root =Tk()
root.config (bg = "#B5D650")
root.title("interface graphique robotique")
root.geometry('1080x720')
root.minsize(480,60)
root.maxsize(1080,720)

#pour mettre les informations par defaut
initialisationVariables()
initialisationGraph()

#frame pour le titre

titre = Frame(root,relief = SUNKEN, bg = "#B5D650")
Label(titre,text='ROBOT MANIPULATEUR 2D',fg='#000000',width=28,font=('Courrier',20,'bold'), bg = "#B5D650").pack(anchor='w',padx=5,pady=5)

#frame de gauche
#les variables du problème
Gauche = Frame(root,relief = SUNKEN, bg = "#B5D650" )
Label(Gauche,text='LES PARAMETRES',fg='#000000',width=20,bg = "#B5D650", font=('Courrier',15,'bold')).pack(anchor='n',padx=5,pady=5)

Label(Gauche,text='Variables géometriques',fg='#000000',width=25,font=('Courrier',15,'bold'),bg='#8F8F8F').pack(anchor='w',padx=5,pady=5)

lien0 = DoubleVar()
lien0.set(L0)
Label(Gauche,width=16,text='Longueur du lien L0 :',fg='#000000', bg = "#B5D650", font=('Courrier',14)).pack(anchor='w',padx=5,pady=5)
Entry(Gauche,width=5,textvariable=lien0).place(x=245,y=90)

lien1 = DoubleVar()
lien1.set(L1)
Label(Gauche,width=16,text='Longueur du lien L1 :',fg='#000000',bg = "#B5D650", font=('Courrier',14)).pack(anchor='w',padx=5,pady=5)
Entry(Gauche,width=5,textvariable=lien1).place(x=245,y=125)

lien2 = DoubleVar()
lien2.set(L2)
Label(Gauche,width=16,text='Longueur du lien L2:',fg='#000000',bg = "#B5D650", font=('Courrier',14)).pack(anchor='w',padx=5,pady=5)
Entry(Gauche,width=5,textvariable=lien2).place(x=245,y=165)

Label(Gauche,width=25,text='Variables articulaires',fg='#000000',font=('Courrier',15,'bold'),bg='#8F8F8F').pack(anchor='w',padx=5,pady=5)

#pour les angles

Theta1 = DoubleVar()

Theta11 = StringVar()
Label(Gauche,width=18,text='Mesure de l\' angle θ1 :',fg='#000000',bg = "#B5D650", font=('Courrier',15)).pack(anchor='w',padx=5,pady=5)
Entry(Gauche,width=5,textvariable=Theta1).place(x=245,y=245)

Theta2 = DoubleVar()
Theta22 = StringVar()
Label(Gauche,width=18,text='Mesure de l\' angle θ2 :',fg='#000000',bg = "#B5D650", font=('Courrier',15)).pack(anchor='w',padx=5,pady=5)
Entry(Gauche,width=5,textvariable=Theta2).place(x=245,y=285)

#pour les coordonnée du point a atteindre

Label(Gauche,width=25,text='Coordonnées du point B',fg='#000000',font=('Courrier',15,'bold'),bg='#8F8F8F').pack(anchor='w',padx=5,pady=5)

xb = DoubleVar()
xb.set(B.getX())
Label(Gauche,text='Abscisse du point B :',fg='#000000',bg = "#B5D650", font=('Courrier',15)).pack(anchor='w',padx=5,pady=5)
Entry(Gauche,width=5,textvariable=xb).place(x=245,y=365)

yb = DoubleVar()
yb.set(B.getY())
Label(Gauche,text='Ordonnée du point B :',fg='#000000',bg = "#B5D650", font=('Courrier',15)).pack(anchor='w',padx=5,pady=5)
Entry(Gauche,width=5,textvariable=yb).place(x=245,y=405)

#pour les parmettres de temps et le pas
Label(Gauche,width=25,text='Paramètres du mouvement',fg='#000000',font=('Courrier',15,'bold'),bg='#8F8F8F').pack(anchor='w',padx=5,pady=5)
n = IntVar()
listpas = tuple(i for i in range(1,100))
Label(Gauche,width=16,text='Nombre de pas :',fg='#000000',bg = "#B5D650", font=('Courrier',15)).pack(anchor='w',padx=5,pady=5)

#Entry(pasFrame,width=5,textvariable=n).grid(row=1,column=1,sticky='w')
n.set(listpas[9])
OptionMenu(Gauche,n,*listpas).place(x=235,y=485)

Time = DoubleVar()
Time.set(T)
Label(Gauche,width=16,text='Durée du trajet A-B :',fg='#000000',bg = "#B5D650", font=('Courrier',15)).pack(anchor='w',padx=5,pady=5)
Entry(Gauche,width=5,textvariable=Time).place(x=245,y=525)

#Frame de droit pour les boutons
DroiteHaut = Frame(root,relief = SUNKEN, bg = "#B5D650")
Label(DroiteHaut,text='Boutons du simulateur',fg='#000000',width=20,font=('Courrier',15,'bold'),bg='#8F8F8F').pack(anchor='w',padx=5,pady=5)

#Frame pour l'auteur du simulateur
DroiteBas = Frame(root,relief = SUNKEN)
Label(DroiteBas,text='Auteur du simulateur',fg='#000000',width=20,font=('Courrier',15,'bold'),bg='#8F8F8F').pack(anchor='w',padx=5,pady=5)

#Frame pour l'affichage du debogade
CentreBas = Frame(root,relief = SUNKEN, bg = "#B5D650")
Label(CentreBas,text='Informations de débogage',fg='#000000',width=35,font=('Courrier',15,'bold'),bg='#8F8F8F').pack(anchor='w',padx=5,pady=5)


#Scrollbar
scrollbar = Scrollbar(CentreBas)
scrollbar.pack(side = RIGHT, fill = Y)
liste = Listbox(CentreBas,yscrollcommand = scrollbar.set ,width=70,height=6)
for i in range(200):
    liste.insert(END, " ")
liste.pack(side = LEFT,fill=BOTH)
scrollbar.config(command = liste.yview)

#Pour inserer l'image de l'auteur

#img = ImageTk.PhotoImage(Image.open("Dimi.png"))
Aut_z = Frame(DroiteBas,bd=2,relief=RAISED)
Aut_z.pack()
photo = Canvas(Aut_z,width = 200,height=90,bg="white")
photo.pack(anchor='n')
#photo.create_image(70,40,image=img)
#Création des boutons pour le simulateur
####################################################################

#Frame pour la simulation

CentreHaut = Frame(root,relief = SUNKEN)
ak = Text(CentreHaut,width=55,height=25,fg='#000000').pack()


def dessiner():
    initialisationVariables(l0=lien0.get(),l1=lien1.get(),l2=lien2.get(),the1=Theta1.get(),the2=Theta2.get(),x=yb.get(),y=xb.get())
    initialisationGraph()

    graphe = monCanvas
    graphe.place(x=367,y=72)


    ak.delete('1.0','end')


boutonDemo = Button(DroiteHaut,width=15,height=3,text='Demo',bd=5,bg='yellow').pack(anchor='n',padx=5,pady=5)

boutonDessiner = Button(DroiteHaut,width=15,height=3,text='Dessiner',command=dessiner,bd=5,bg='green').pack(anchor='n',padx=5,pady=5)

boutonSimuler = Button(DroiteHaut,width=15,height=3,command=lambda: mouvement(n.get()),text='Simuler',bd=5,bg='green').pack(anchor='n',padx=5,pady=5)

boutonNouveau = Button(DroiteHaut,width=15,height=3,text='Nouveau',bd=5,bg='#8F8F8F').pack(anchor='n',padx=5,pady=5)

boutonQuitter = Button(DroiteHaut,width=15,height=3,text='Quitter',bd=5,command=root.quit,bg='red').pack(anchor='n',padx=5,pady=5)

###################################################################
titre.place(x=325,y=0)
Gauche.place(x=10,y=65)
DroiteHaut.place(x=800,y=65)
DroiteBas.place(x=800,y=480)
CentreHaut.place(x=342,y=65)
CentreBas.place(x=344,y=480)
root.mainloop()
