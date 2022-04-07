#
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Ce programme est le jeu du Casse Brique
#
# Ce programme utilise l'interface graphique Tkinter
#
# Auteur        : Gautier Pauliat
# Platforme testée : Windows
#
#----------------------------------------------------------------------

#----------------------------------- Modules

from tkinter import *
from tkinter.font import *
import tkinter.messagebox
import tkinter.filedialog
import fileinput
from random import *
from time import *

#----------------------------------- Fonctions

#---- Fonction de déplacement de la balle
def mvment_balle():

    global xa
    global ya
    global xp
    global yp
    global xmax
    global ymax
    global canvas
    global fenetre
    global balle
    global play
    global xr
    global yr
    global actualisation_time
    global debug
    global tableau_briques
    global largeur_plaque

    if play:

        #On calcule la nouvelle position de la balle
        xs = xa #On met de côté la valeur x actuelle de la balle
        ys = ya #On met de côté la valeur y actuelle de la balle

        #On calcule la nouvelle position de la balle en supposant qu'il n'y a pas de brique(s)
        xf = xa + (xa-xp)
        yf = ya + (ya-yp)
        if yf == -1: yf = 1                     #On rebondit sur le plafond
        if debug and yf == ymax: yf = ymax-2    #On rebondit sur le sol en mode debug
        if xf == -1: xf = 1                     #On rebondit sur le mur de gauche
        if xf == xmax: xf = xmax-2              #On rebondit sur le mur de droite

        #Cas n°1: aucune brique ne gêne le mouvement de la balle
        if tableau_briques[xf][yf] == "vide" and tableau_briques[xa][yf] == "vide" and tableau_briques[xf][ya] == "vide":
            xa = xf
            ya = yf

        #Cas n°2: une seule brique gêne le mouvement, en (xf,yf)
        #On casse la brique et repart en sens inverse
        elif tableau_briques[xf][yf] == "brique" and tableau_briques[xa][yf] == "vide" and tableau_briques[xf][ya] == "vide":
            efface_brique(xf,yf)
            xa = xp
            ya = yp


        #Cas n°3: deux briques gênent le mouvement de la balle, à gauche et à droite
        #On casse les deux briques et repart en sens inverse
        elif tableau_briques[xa][yf] == "brique" and tableau_briques[xf][ya] == "brique":
            efface_brique(xa,yf)
            efface_brique(xf,ya)
            xa = xp
            ya = yp


        #Cas n°4: une seule brique gêne le mouvement de la balle, à gauche
        #On casse la brique et rebondit dessus, on change la direction x
        elif tableau_briques[xa][yf] == "vide" and tableau_briques[xf][ya] == "brique":
            efface_brique(xf,ya)
            xa = xp
            ya = yf


        #Cas n°5: une seule brique gêne le mouvement de la balle, à droite
        #On casse la brique et on rebondit dessus,on change la direction y
        elif tableau_briques[xa][yf] == "brique" and tableau_briques[xf][ya] == "vide":
            efface_brique(xa,yf)
            xa = xf
            ya = yp

        #Pour rebondir sur la plaque
        if ya == yr:
            if xa >= xr and xa <= xr + largeur_plaque - 1:
                ya -= 2


        #On retient l'ancienne position de la balle
        xp = xs
        yp = ys

        #On efface la balle à son ancienne position
        canvas.delete(balle)

        #On affiche la balle à sa nouvelle position
        balle = canvas.create_image(xa*taille_balle+2, ya*taille_balle+2,anchor=NW,image=image_balle)

        #Si on touche le sol sans être en mode debug, on perd une vie
        if not(debug) and ya == ymax - 1:

            #On perd une vie
            life_loss()
            #On repositionne la balle au centre
            xa=xmax//2
            ya=ymax-4
            xp=xa-1
            yp=ya+1
            canvas.delete(balle)
            balle = canvas.create_image(xa*taille_balle+2, ya*taille_balle+2,anchor=NW,image=image_balle)
            #On met le jeu en pause
            pause()


        #On rappelle la fonction après un certain temps, qui varie en fonction de la variable actualisation_time
        fenetre.after(actualisation_time, mvment_balle)

#---- Fonction qui affiche les briques
def affiche_briques():
    global taille_balle
    global nb_briques
    global nb_briques_restantes
    global tableau_briques
    global xmax
    global couleurs_brique
    global image_brique_grise
    global image_brique_bleue
    global image_brique_jaune
    global image_brique_verte
    global image_brique_rouge
    global nb_lignes_briques

    for x in range(xmax):
        for y in range(nb_lignes_briques):
            if tableau_briques[x][y] == "brique":
                canvas.create_image(x*taille_balle+2,y*taille_balle+2,anchor=NW, image=choice(couleurs_brique))
                nb_briques += 1
    nb_briques_restantes = nb_briques

#---- Fonction qui détruit une brique
def efface_brique(x,y):
    global score
    global taille_balle
    global nb_briques_restantes
    global pts
    global tableau_briques
    global couleur_bg

    canvas.create_rectangle(x*taille_balle+2,y*taille_balle+2,(x+1)*taille_balle+2,(y+1)*taille_balle+2,fill=couleur_bg,width=0)
    tableau_briques[x][y] = "vide"

    #Le joueur gagne un point
    pts += 1
    new_highscore()
    #On actualise l'affichage du score
    Label(frame,bg="grey",text="Score: "+str(pts),font=Font(family='Arial Black',size=15)).grid(row=0,column=0,columnspan=3,sticky=W)
    #On actualise l'affichage du nombre de briques
    nb_briques_restantes -= 1
    Label(frame,bg="grey",text="Briques restantes: "+str(nb_briques_restantes),font=Font(family='Arial Black',size=15)).grid(row=2,column=0,columnspan=3,sticky=W)
    #Si toutes les briques sont cassées, le joueur gagne
    if pts == nb_briques:
        win()

#---- Fonction pour le meilleur score
def new_highscore():
    global pts
    global highscore
    if pts > highscore:
        highscore = pts
        Label(frame,bg="grey",text="Highscore: "+str(highscore),font=Font(family='Arial Black',size=15)).grid(row=2,column=3,sticky=W)

def save():
    global fichier_highscore
    global highscore
    fichier_highscore = open("score\highscore.txt","w")
    fichier_highscore.write(str(highscore))
    fichier_highscore.close()

#---- Fonction pour la perte d'une vie
def life_loss():
    global vie
    global xr
    global yr

    #Tant que le joueur a plus d'une vie (après la perte de vie)
    if vie > 2:
        vie -= 1
        tkinter.messagebox.showwarning("Une vie de moins !","Attention !\nVous venez de perdre une vie. \nPlus que "+str(vie)+" vie restantes")

    #Quand le joueur n'a plus qu'une vie (après la perte de vie)
    elif vie == 2:
        vie -= 1
        tkinter.messagebox.showwarning("Une vie de moins !","Attention ! \nVous venez de perdre une vie.\nPlus qu'une vie restante !!")

    #Quand le joueur n'a plus de vie
    else:
        tkinter.messagebox.showwarning("Perdu !", "Vous n'avez plus de vies, vous avez perdu !")
        vie -= 1
        fenetre.destroy()

    xr = xmax // 2 - largeur_plaque // 2
    #On actualise l'affichage du nombre de vies
    Label(frame,bg="grey",text="Vies restantes: "+str(vie)+"♥",font=Font(family='Arial Black',size=15)).grid(row=1,column=0,columnspan=3,sticky=W)
    mvment_plaque()

#---- Fonction de victoire
def win():
    global nb_briques
    if tkinter.messagebox.showinfo("Victoire !","Vous avez cassé les " +str(nb_briques) +" briques ! \nVous avez gagné ! Bravo !"):
        fenetre.destroy()

#---- Fonction pour lancer la partie
def start():
    global play
    global bpause
    global xmax
    global ymax
    global window_difficulty_choice

    play = True
    mvment_balle()
    bpause = Button(frame,bg="grey", text="Pause",font=Font(family='Arial Black',size=15), command = pause,width=10).grid(row=1, column=3)
    canvas.delete(window_difficulty_choice)
#---- Fonction pour mettre en pause la partie
def pause():
    global play
    global bpause

    play = False
    bpause = Button(frame,bg="grey", text="Resume",font=Font(family='Arial Black',size=15), command = resume,width=10).grid(row=1, column=3)

#---- Fonction pour résumer la partie
def resume():
    global play
    global mvment_balle
    global bpause

    bpause = Button(frame,bg="grey", text="Pause",font=Font(family='Arial Black',size=15), command = pause,width=10).grid(row=1, column=3)
    play = True
    mvment_balle()


#---- Fonction de déplacement de la plaque
def mvment_plaque():
    global play
    global taille_balle
    global plaque
    global xr
    global yr

    if play:
        #On change les coordonnées de la plaque
        canvas.coords(plaque,xr*taille_balle+2,yr*taille_balle+2)

#---- Fonction qui permet au joueur de déplacer la plaque vers la gauche
def gauche(event):
    global xr

    if play: #Quand le jeu est lancé et n'est pas en pause
        if xr >= 1:
            xr -= 1
            #On rappelle la fonction mvment_plaque pour actualiser sa position
            mvment_plaque()

#---- Fonction qui permet au joueur de déplacer la plaque vers la droite
def droite(event):
    global xr
    global taille_balle

    if play: #Quand le jeu est lancé et n'est pas en pause
        if xr + largeur_plaque < xmax:
            xr += 1
            #On rappelle la fonction mvment_plaque pour actualiser sa position
            mvment_plaque()

#---- Fonction pour quitter le jeu
def quitter():
    if tkinter.messagebox.askokcancel("QUITTER LE JEU","Etes vous sur de vouloir quitter le jeu ?"):
        save()
        fenetre.destroy()

#---- Ce qui se passe quand on choisit la difficulté
def difficulty():
    global difficulty_choice
    global window_difficulty_choice
    global window_facile
    global window_moyen
    global window_difficile

    if difficulty_choice:
        canvas.delete(window_difficulty_choice)
        canvas.delete(window_facile)
        canvas.delete(window_moyen)
        canvas.delete(window_difficile)
        but = "But : \n Casser toutes les briques sans que la balle touche le sol \n Cliquez sur Start quand vous êtes prêt"
        label_but = Label(canvas, text=but, font=Font(family='Arial', size=20), bg="#606060", fg="red")
        window_difficulty_choice = canvas.create_window (xmax*taille_balle/2-350,200, window=label_but, anchor=NW)
        bpause = Button(frame, text="Start", command = start,bg="grey",font=Font(family='Arial Black',size=15),width=10,activebackground="white").grid(row=1, column=3)

    elif not(difficulty_choice):
        window_facile = canvas.create_window(xmax*taille_balle/2-101,300, window=button_facile, anchor=NE)
        window_moyen = canvas.create_window(xmax*taille_balle/2-54,300, window=button_moyen, anchor=NW)
        window_difficile = canvas.create_window(xmax*taille_balle/2+101,300, window=button_difficile, anchor=NW)

#---- Difficulté Facile
def facile():
    global difficulty_choice
    global actualisation_time
    difficulty_choice = True
    actualisation_time = 150
    # affichage_difficulty()
    difficulty()

#---- Difficulté Moyen
def moyen():
    global difficulty_choice
    global actualisation_time
    difficulty_choice = True
    actualisation_time = 100
    # affichage_difficulty()
    difficulty()

#---- Difficulté Difficile
def difficile():
    global difficulty_choice
    global actualisation_time
    difficulty_choice = True
    actualisation_time = 50
    # affichage_difficulty()
    difficulty()

#----------------------------------- Programme Principal

#---- Fenêtre principale
fenetre = Tk()

#---- On nomme la fenêtre principale
fenetre.title("Casse Brique")

#---- On empêche l'utilisateur de resizer la fenêtre
fenetre.resizable(width=False,height=False)
#---- On active ou non le mode debug
debug = True #En mode debug la balle rebondit sur le sol au lieu de faire perdre une vie


#---- Largeur en "case" du canvas
xmax=20

#---- Hauteur en "case" du canvas

ymax=18
nb_lignes_briques = 3

#---- Taille de la balle et Largeur, Hauteur d'une case
taille_balle = 40

#---- On donne la couleur de l'arrière plan
couleur_bg = "#606060"

#---- On crée la zone de dessin (canvas)
canvas = Canvas(fenetre, width=xmax*taille_balle, height=ymax*taille_balle, background = couleur_bg)
canvas.pack()

#---- On crée une variable nous permettant de mettre pause sur le jeu, quand play = false, le jeu est en pause, et quand play = true le jeu est marche
play = False

xa=xmax//2 # Position actuelle x du haut gauche de la balle
ya=ymax-4 # Position actuelle y du haut gauche de la balle
xp=xa-1 # Position précédente x du haut gauche de la balle
yp=ya+1# Position précédente y du haut gauche de la balle

#---- On demande à l'utilisateur de choisir la difficulté

difficulty_choice = False #False tant que l'utilisateur n'a pas fait le choix de difficulté

label_difficulty = Label(canvas, text="Choisir la difficulté", font=Font(family='Arial', size=40), bg="#606060", fg="red")
window_difficulty_choice = canvas.create_window (xmax*taille_balle/2-209,200, window=label_difficulty, anchor=NW)

button_facile = Button(canvas, text="Facile",font=Font(family='Arial', size=20),bg="black",fg="#4CFF00",command=facile)
window_facile = canvas.create_window(xmax*taille_balle/2-101,300, window=button_facile, anchor=NE)

button_moyen = Button(canvas, text="Moyen",font=Font(family='Arial', size=20),bg="black",fg="orange",command=moyen)
window_moyen = canvas.create_window(xmax*taille_balle/2-54,300, window=button_moyen, anchor=NW)

button_difficile = Button(canvas, text="Difficile",font=Font(family='Arial', size=20),bg="black",fg="red",command=difficile)
window_difficile = canvas.create_window(xmax*taille_balle/2+101,300, window=button_difficile, anchor=NW)

#---- On crée le tableau

tableau_briques = []
for i in range(xmax):
    tableau_briques.append(["brique"]*nb_lignes_briques+["vide"]*(ymax-nb_lignes_briques))

#---- On crée une variable nb_briques pour compter le nombre de briques
nb_briques = 0

#---- On crée une variable nb_briques pour compter le nombre de briques restantes
nb_briques_restantes = 0

#---- On définit la largeur de la plaque (nb pair)
largeur_plaque = 6

#---- On définit les coordonnées de départ du sommet en haut à gauche de la plaque
xr = xmax // 2 - largeur_plaque // 2
yr = ymax - 1

#---- On charge l'animation (ensemble d'images) de la plaque
image_plaque = PhotoImage(file="images/plaquev2 240x40.gif")

#---- On crée la plaque où rebondira la balle
plaque = canvas.create_image(xr*taille_balle+2,yr*taille_balle+2,anchor=NW,image=image_plaque)

#---- On charge l'image de la balle
image_balle = PhotoImage(file="images/ballev2 40x40.gif")

#---- On crée la balle rebondissante
balle = canvas.create_image(xa*taille_balle+2, ya*taille_balle+2,anchor=NW,image=image_balle)

#---- On charge l'image des briques
image_brique_grise = PhotoImage(file="images/brique_grise 40x40.gif")
image_brique_rouge = PhotoImage(file="images/brique_rouge 40x40.gif")
image_brique_jaune = PhotoImage(file="images/brique_jaune 40x40.gif")
image_brique_verte = PhotoImage(file="images/brique_verte 40x40.gif")
image_brique_bleue = PhotoImage(file="images/brique_bleue 40x40.gif")
couleurs_brique = [image_brique_grise,image_brique_rouge,image_brique_jaune,image_brique_verte,image_brique_bleue]

#---- On affiche les briques
affiche_briques()

#---- On execute la fonction mvment_plaque pour initialiser le mouvement de la plaque où la balle rebondira
mvment_plaque()

#---- On associe le bouton Flèche Gauche à la fonction gauche
fenetre.bind("<Left>",gauche)

#---- On associe le bouton Flèche Droite à la fonction droite
fenetre.bind("<Right>",droite)

#---- On crée la frame pour les boutons
frame = Frame(fenetre)
frame.pack(fill=X)
frame.configure(bg="white")

#---- On défini la valeur de départ du temps d'actualisation de la fonction mvment_balle (qui définit la vitesse de la balle). La valeur de actualisation_time est soit 50, 100 ou 150. Plus cette valeur est élevée, plus la balle est lente

actualisation_time = 150

#---- On affiche les briques restantes
Label(frame,bg="grey",text="Briques restantes: "+str(nb_briques_restantes),font=Font(family='Arial Black',size=15)).grid(row=2,column=0,columnspan=3,sticky=W)


#---- On met le score à 0
pts = 0

#---- Highscore
fichier_highscore = open("score\highscore.txt","r")
highscore = int(fichier_highscore.readline())
fichier_highscore.close()
Label(frame,bg="grey",text="Highscore: "+str(highscore),font=Font(family='Arial Black',size=15)).grid(row=2,column=3,sticky=W)


#---- On affiche le score
Label(frame,bg="grey",text="Score: "+str(pts),font=Font(family='Arial Black',size=15)).grid(row=0,column=0,columnspan=3,sticky=W)

#---- On définit le nombre de vies
vie = 5

#---- On affiche les vies restantes
Label(frame,bg="grey",text="Vies restantes: "+str(vie)+" ♥",font=Font(family='Arial Black',size=15)).grid(row=1,column=0,columnspan=3,sticky=W)

#---- Bouton pour quitter le jeu
Button(frame,bg="grey", text="Quitter le jeu",font=Font(family='Arial Black',size=15),command=quitter).grid(row=2,column=5,sticky=E)

#---- On configure les colonnes de la frame
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)
frame.columnconfigure(4, weight=1)
frame.columnconfigure(5, weight=1)

fenetre.mainloop()
