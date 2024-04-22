## - Encoding: UTF-8 -*-

from tkinter import PhotoImage
import os,os.path

images={}
def charger_images(chemin=None): # librairie importee par la vue pour charger les images et les gif
    if chemin==None:
        chemin=os.getcwd()
        chemin=chemin+"\\images"
    for i in os.listdir(chemin):
        che=chemin+"\\"+i
        if os.path.isdir(che):
            charger_images(che)
        else:
            nom, ext=os.path.splitext(os.path.basename(i))
            if ".png"==ext:
                    images[nom]=PhotoImage(file=che) # dict de nom et de fichier
    return images

def charger_gifs(): # un gif cest une list dimage une par dessus les autres avec un ping pour changer dimage a chaque intervalle
    gifs = {}
    lesgifs = ["poissons.gif", "marche.gif"]
    for nom in lesgifs:
        listeimages = []
        testverite = 1
        noindex = 0
        while testverite:
            try:
                img = PhotoImage(file='./images/GIFS/' + nom, format="gif -index " + str(noindex)) # on peut aller chercher juste une image precise dans le gif
                listeimages.append(img)
                noindex += 1
            except Exception:
                gifs[nom[:-4]] = listeimages # a -4 il y a un bout de texte
                testverite = 0 # ca sort a zero
    return gifs # ca retourne toutes les images dun gif anime



if __name__ == '__main__':
    images=charger_images()

    for i in images.keys():
            print("images ", i,images[i])
