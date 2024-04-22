## -*- Encoding: UTF-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import *

from chargeurdimages import *


class Vue():
    def __init__(self, parent, url_serveur, nom_joueur_local):  # , testdispo):

        self.gagnant = "ARI"
        self.parent = parent
        self.root = Tk()
        self.root.title("Je suis " + nom_joueur_local)
        self.nom_joueur_local = nom_joueur_local
        # attributs
        self.cadrechaton = 0  # fenetre de chat on ou non
        self.textchat = ""
        self.infohud = {}  # overhead display : les ressources et autres
        # # minicarte
        self.tailleminicarte = 220
        self.cadreactif = None
        self.limbo = 0
        # # objet pour cumuler les manipulations du joueur pour generer une action de jeu
        self.action = Action(self)  # pour avoir une action fraiche. C,est comme un Singleton
        # cadre principal de l'application
        self.cadreapp = Frame(self.root, width=500, height=400, bg="red")  # un frame generique pour toute lapp
        self.cadreapp.pack(expand=1, fill=BOTH)

        # # un dictionnaire pour conserver les divers cadres du jeu, creer plus bas
        self.cadres = {}
        self.creer_cadres(url_serveur, nom_joueur_local, "testdispo")
        self.changer_cadre("splash")

        # self.root.protocol("WM_DELETE_WINDOW", self.demanderabandon)
        # # sera charge apres l'initialisation de la partie, contient les donnees pour mettre l'interface a jour
        self.modele = None
        # # variable pour suivre le trace du multiselect
        self.debut_selection = []
        self.selecteuractif = None
        # # images des assets, definies dans le modue loadeurimages
        self.images = charger_images()
        self.gifs = charger_gifs()

    ####### INTERFACES GRAPHIQUES

    def changer_cadre(self, nomcadre: str):
        cadre = self.cadres[nomcadre]
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif = cadre
        self.cadreactif.pack(expand=1, fill=BOTH)

    ###### LES CADRES ############################################################################################
    # Appel de la création des divers cadre
    def creer_cadres(self, url_serveur: str, nom_joueur_local: str, testdispo: str):
        self.cadres["splash"] = self.creer_cadre_splash(url_serveur, nom_joueur_local, testdispo)
        self.cadres["lobby"] = self.creer_cadre_lobby()

        self.cadres["jeu"] = self.creer_cadre_jeu()

    # le splash (ce qui 'splash' à l'écran lors du démarrage)
    # sera le cadre visuel initial lors du lancement de l'application

    def creer_cadre_fin(self):
        self.cadreFin = Frame(self.cadreapp, bg="gold", width=500, height=400)

        self.cadreFin.pack_propagate(False)
        label_text = "FIN DE LA PARTIE"
        label = Label(self.cadreFin, text=label_text, bg=self.cadreFin['bg'], font=("arial", 12, "bold"))
        label.config()
        t1 = Label(self.cadreFin, text="Gagnant", bg=self.cadreFin['bg'], font=("arial", 14, "bold"))

        gagnant = Label(self.cadreFin, text=self.gagnant, bg=self.cadreFin['bg'], font=("arial", 18, "bold"))
        gagnant.config()


        label.pack(expand=True)
        t1.pack(expand=True)
        gagnant.pack(expand=True)
        self.cadreFin.rowconfigure(0, weight=1)
        self.cadreFin.columnconfigure(0, weight=1)

        # self.btnurlconnect = Button(text="Connecter", font=("Arial", 12),
        #                             command=self.initialiser_splash_post_connection)
        # self.btnurlconnect = Button(text="Connecter", font=("Arial", 12),

        return self.cadreFin

    def afficher_fin(self, gagnant):

        self.gagnant = gagnant
        self.cadres["fin"] = self.creer_cadre_fin()
        self.changer_cadre("fin")

    def creer_cadre_splash(self, url_serveur: str, nom_joueur_local: str, testdispo: str) -> Frame:
        self.cadresplash = Frame(self.cadreapp)
        # un canvas est utilisé pour 'dessiner' les widgets de cette fenêtre voir 'create_window' plus bas
        self.canevassplash = Canvas(self.cadresplash, width=600, height=480, bg="wheat1")
        self.canevassplash.pack()

        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        # creation ds divers widgets (champ de texte 'Entry' et boutons cliquables (Button)
        # les champs et
        self.etatdujeu = Label(text=testdispo, font=("Arial", 18), borderwidth=2, relief=RIDGE)
        self.nomsplash = Entry(font=("Arial", 14))
        self.url_initial = Entry(font=("Arial", 14))
        self.btnurlconnect = Button(text="Connecter", font=("Arial", 12),
                                    command=self.initialiser_splash_post_connection)
        # on insère les infos par défaut (nom url) et reçu au démarrage (dispo)
        self.nomsplash.insert(0, nom_joueur_local)
        self.url_initial.insert(0, url_serveur)
        # on les place sur le canevassplash
        self.canevassplash.create_window(320, 100, window=self.etatdujeu, width=400, height=30)
        self.canevassplash.create_window(320, 200, window=self.nomsplash, width=400, height=30)
        self.canevassplash.create_window(240, 250, window=self.url_initial, width=200, height=30)
        self.canevassplash.create_window(420, 250, window=self.btnurlconnect, width=100, height=30)

        # les boutons d'actions
        self.btncreerpartie = Button(text="Creer partie", font=("Arial", 12), state=DISABLED, command=self.creer_partie)
        self.btninscrirejoueur = Button(text="Inscrire joueur", font=("Arial", 12), state=DISABLED,
                                        command=self.inscrire_joueur)
        self.btnreset = Button(text="Reinitialiser partie", font=("Arial", 9), state=DISABLED,
                               command=self.reset_partie)
        # on place les boutons
        self.canevassplash.create_window(420, 350, window=self.btncreerpartie, width=200, height=30)
        self.canevassplash.create_window(420, 400, window=self.btninscrirejoueur, width=200, height=30)
        self.canevassplash.create_window(420, 450, window=self.btnreset, width=200, height=30)

        return self.cadresplash

    def initialiser_splash_post_connection(self):
        url_serveur = self.url_initial.get()
        if url_serveur:
            self.btninscrirejoueur.config(state=NORMAL)
            self.btncreerpartie.config(state=NORMAL)
            self.btnreset.config(state=NORMAL)
            self.parent.initialiser_splash_post_connection(url_serveur)
        else:
            self.etatdujeu.config(text="Aucune adresse de serveur")

    def creer_cadre_lobby(self):
        # le cadre lobby, pour isncription des autres joueurs, remplace le splash
        self.cadrelobby = Frame(self.cadreapp)
        self.canevaslobby = Canvas(self.cadrelobby, width=640, height=480, bg="lightblue")
        self.canevaslobby.pack()
        # widgets du lobby
        # un listbox pour afficher les joueurs inscrit pour la partie à lancer
        self.listelobby = Listbox(borderwidth=2, relief=GROOVE)

        # bouton pour lancer la partie, uniquement accessible à celui qui a creer la partie dans le splash
        self.btnlancerpartie = Button(text="Lancer partie", state=DISABLED, command=self.lancer_partie)
        # affichage des widgets dans le canevaslobby (similaire au splash)
        self.canevaslobby.create_window(440, 240, window=self.listelobby, width=200, height=400)
        self.canevaslobby.create_window(200, 400, window=self.btnlancerpartie, width=100, height=30)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrelobby

    def creer_cadre_jeu(self):
        # le cadre principal du jeu, remplace le Lobby
        self.cadrepartie = Frame(self.cadreapp, bg="green", width=400, height=400)
        # cadre du jeu et ses scrollbars
        self.creer_aire_de_jeu()
        # cadre pour info sur les ressources du joueur en haut de l'aire de jeu
        self.creer_HUD()
        # cadre pour commandes et infos des objets de jeu, situe a droite
        self.creer_cadre_jeu_action()
        # configuration de la section qui s'etire lorsque la fenetre change de taille
        self.cadrepartie.rowconfigure(0, weight=1)
        self.cadrepartie.columnconfigure(0, weight=1)
        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        return self.cadrepartie

    def creer_aire_de_jeu(self):
        # definition du cadre avec le canvas de jeu et les scrollbars
        self.cadrecanevas = Frame(self.cadrepartie)
        # on crée les scrollbar AVANT le canevas de jeu car le canevas est dépendant de leur
        self.scrollV = Scrollbar(self.cadrecanevas, orient=VERTICAL)
        self.scrollH = Scrollbar(self.cadrecanevas, orient=HORIZONTAL)
        self.canevas = Canvas(self.cadrecanevas, width=400, height=400, bg="DarkOliveGreen2",
                              yscrollcommand=self.scrollV.set,
                              xscrollcommand=self.scrollH.set)
        self.scrollV.config(command=self.canevas.yview)
        self.scrollH.config(command=self.canevas.xview)
        # on visualise utilisant grid (grille)
        # le grid avec 'sticky' indique que l'objet doit s'acroitre pour coller aux 'points cardinaux' (anglais)

        self.canevas.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollV.grid(row=1, column=1, sticky=N + S)
        self.scrollH.grid(row=2, column=0, sticky=E + W)

        # visualise le cadre qui contient le canevas de jeu
        self.cadrecanevas.grid(column=0, row=0, sticky=N + S + E + W)
        # on doit preciser quelle partie de la grille (grid) va s'accroitre, colonne et rangée
        # ici on precise que c'est le canevas et non les scrollbar qui doit s'agrandir
        self.cadrecanevas.rowconfigure(1, weight=1)
        self.cadrecanevas.columnconfigure(0, weight=1)
        self.connecter_event()

    def creer_HUD(self):

        self.cadrejeuinfo = Frame(self.cadrecanevas, bg="blue")
        self.cadretemp = self.cadrejeuinfo
        # des etiquettes d'info
        self.infohud = {"Nourriture": None,
                        "Bois": None,
                        "Roche": None,
                        "Aureus": None}

        # fonction interne uniquement pour reproduire chaque item d'info
        def creer_champ_interne(listechamp):  # refactoriser pour etiquette au lieu de champ
            titre = Champ(self.cadrejeuinfo, text=i, bg="red", fg="white")
            varstr = StringVar()
            varstr.set(0)
            donnee = Champ(self.cadrejeuinfo, bg="red", fg="white", textvariable=varstr)
            titre.pack(side=LEFT)
            donnee.pack(side=LEFT)
            self.infohud[i] = [varstr, donnee]

        for i in self.infohud.keys():
            creer_champ_interne(i)

        varstr = StringVar()
        varstr.set("")

        champmsg = Label(self.cadrejeuinfo, text="", fg="red")
        champmsg.pack(side=LEFT)
        self.infohud["msggeneral"] = [champmsg]
        self.btnchat = Button(self.cadrejeuinfo, text="Chat", command=self.action.chatter)
        self.btnaide = Button(self.cadrejeuinfo, text="Aide", command=self.action.aider)

        self.btnaide.pack(side=RIGHT)
        self.btnchat.pack(side=RIGHT)

        self.cadrejeuinfo.grid(row=0, column=0, sticky=E + W, columnspan=2)

    def creer_cadre_jeu_action(self):
        # Ajout du cadre d'action a droite pour identifier les objets permettant les commandes du joueur
        self.cadreaction = Frame(self.cadrepartie)
        self.cadreaction.grid(row=0, column=1, sticky=N + S)
        self.scrollVaction = Scrollbar(self.cadreaction, orient=VERTICAL)
        self.canevasaction = Canvas(self.cadreaction, width=200, height=300, bg="lightblue",
                                    yscrollcommand=self.scrollVaction.set)

        self.scrollVaction.config(command=self.canevasaction.yview)
        self.canevasaction.grid(row=0, column=0, sticky=N + S)
        self.scrollVaction.grid(row=0, column=1, sticky=N + S)
        # les widgets
        self.canevasaction.create_text(100, 30, text=self.parent.nom_joueur_local, font=("arial", 18, "bold"), anchor=S,
                                       tags=("nom"))

        # minicarte
        self.minicarte = Canvas(self.cadreaction, width=self.tailleminicarte, height=self.tailleminicarte, bg="tan1",
                                highlightthickness=0)
        self.minicarte.grid(row=2, column=0, columnspan=2)
        self.minicarte.bind("<Button-1>", self.deplacer_carte)

        # on retourne ce cadre pour l'insérer dans le dictionnaires des cadres
        self.canevasaction.rowconfigure(0, weight=1)
        self.cadreaction.rowconfigure(0, weight=1)

    def creer_aide(self):
        self.cadreaide = Frame(self.canevas)
        self.scrollVaide = Scrollbar(self.cadreaide, orient=VERTICAL)
        self.textaide = Text(self.cadreaide, width=50, height=10,
                             yscrollcommand=self.scrollVaide.set)
        self.scrollVaide.config(command=self.textaide.yview)
        self.textaide.pack(side=LEFT)
        self.scrollVaide.pack(side=LEFT, expand=1, fill=Y)
        fichieraide = open("aide.txt")
        monaide = fichieraide.read()
        fichieraide.close()
        self.textaide.insert(END, monaide)
        self.textaide.config(state=DISABLED)

    def creer_chatter(self):
        self.cadrechat = Frame(self.canevas, bd=2, bg="orange")
        self.cadrechatlist = Frame(self.cadrechat)
        # Make topLevelWindow remain on top until destroyed, or attribute changes.
        self.scrollVchat = Scrollbar(self.cadrechatlist, orient=VERTICAL)
        self.textchat = Listbox(self.cadrechatlist, width=30, height=6,
                                yscrollcommand=self.scrollVchat.set)
        self.scrollVchat.config(command=self.textchat.yview)
        self.textchat.pack(side=LEFT)
        self.scrollVchat.pack(side=LEFT, expand=1, fill=Y)
        self.textchat.delete(0, END)
        self.cadrechatlist.pack()
        # inscrire texte et choisir destinataire
        self.cadreparler = Frame(self.cadrechat, bd=2)
        self.joueurs = ttk.Combobox(self.cadreparler,
                                    values=list(self.modele.joueurs.keys()))
        self.entreechat = Entry(self.cadreparler, width=20)
        self.entreechat.bind("<Return>", self.action.envoyer_chat)
        self.joueurs.pack(expand=1, fill=X)
        self.entreechat.pack(expand=1, fill=X)
        self.cadreparler.pack(expand=1, fill=X)

    def connecter_event(self):
        # on attache (bind) desF événements soit aux objets eux même
        self.canevas.bind("<Button-1>", self.annuler_action)
        self.canevas.bind("<Button-3>", self.construire_batiment)
        # faire une multiselection
        self.canevas.bind("<Shift-Button-1>", self.debuter_selection)
        self.canevas.bind("<Shift-B1-Motion>", self.afficher_selection)
        self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_selection)

        self.canevas.bind("<Button-2>", self.indiquer_position)

        self.canevas.bind("<MouseWheel>", self.OnMouseWheel)
        self.canevas.bind("<Control-MouseWheel>", self.OnCtrlMouseWheel)

        # soit aux dessins, en vertu de leur tag (propriétés des objets dessinés)
        # ALL va réagir à n'importe quel dessin
        # sinon on spécifie un tag particulier, exemple avec divers tag, attaché par divers événements
        self.canevas.tag_bind("batiment", "<Button-1>", self.creer_entite)
        self.canevas.tag_bind("perso", "<Button-1>", self.ajouter_selection)
        self.canevas.tag_bind("arbre", "<Button-1>", self.ramasser_ressource)
        self.canevas.tag_bind("aureus", "<Button-1>", self.ramasser_ressource)
        self.canevas.tag_bind("roche", "<Button-1>", self.ramasser_ressource)
        self.canevas.tag_bind("baie", "<Button-1>", self.ramasser_ressource)
        self.canevas.tag_bind("eau", "<Button-1>", self.ramasser_ressource)
        self.canevas.tag_bind("daim", "<Button-1>", self.chasser_ressource)
        # self.canevas.tag_bind("daim", "<Button-1>", self.afficher_fin)

        # self.canevas.bind("<space>", self.test)

    def OnMouseWheel(self, evt):
        print(evt.keysym)
        rep = self.scrollV.get()[0]
        if evt.delta < 0:
            rep = rep + 0.02
        else:
            rep = rep - 0.02
        self.canevas.yview_moveto(rep)

    def OnCtrlMouseWheel(self, evt):
        print("IN X")
        rep = self.scrollH.get()[0]
        if evt.delta < 0:
            rep = rep + 0.02
        else:
            rep = rep - 0.02
        self.canevas.xview_moveto(rep)

        # cette méthode sert à changer le cadre (Frame) actif de la fenêtre, on n'a qu'à fournir le cadre requis

    def test_HUD(self):
        self.limbo = 1

    ##### FONCTION DU SPLASH #########################################################################
    def creer_partie(self):
        nom = self.nomsplash.get()
        ## ON VA LIRE LA VALEUR DE LA VARIABLE ASSOCIEE AU BTN RADION CHOISI
        urljeu = self.url_initial.get()
        self.parent.creer_partie(nom)  # , urljeu)  # ,valciv)

    ###  METHODES POUR SPLASH ET LOBBY INSCRIPTION pour participer a une partie
    def update_splash(self, etat):
        if "attente" in etat or "courante" in etat:
            self.btncreerpartie.config(state=DISABLED)
        if "courante" in etat:
            self.etatdujeu.config(text="Desole - partie encours !")
            self.btninscrirejoueur.config(state=DISABLED)
        elif "attente" in etat:
            self.etatdujeu.config(text="Partie en attente de joueurs !")
            self.btninscrirejoueur.config(state=NORMAL)
        elif "dispo" in etat:
            self.etatdujeu.config(text="Bienvenue ! Serveur disponible")
            self.btninscrirejoueur.config(state=DISABLED)
            self.btncreerpartie.config(state=NORMAL)
        else:
            self.etatdujeu.config(text="ERREUR - un probleme est survenu")

    ##### FONCTION DU LOBBY #############
    def update_lobby(self, dico):
        self.listelobby.delete(0, END)
        for i in dico:
            self.listelobby.insert(END, i[0])
        if self.parent.ego_serveur:
            self.btnlancerpartie.config(state=NORMAL)

    def inscrire_joueur(self):
        nom = self.nomsplash.get()
        urljeu = self.url_initial.get()
        self.parent.inscrire_joueur(nom, urljeu)

    def lancer_partie(self):
        self.parent.lancer_partie()

    def reset_partie(self):
        rep = self.parent.reset_partie()

    def initialiser_avec_modele(self):
        # on reassigne le nom final localement pour eviter
        # de toujours le requerir du parent
        self.nom_joueur_local = self.parent.nom_joueur_local
        # on ajuste la taille du canevas de jeu
        self.canevas.config(scrollregion=(0, 0, self.modele.aireX, self.modele.aireY))
        self.canevasaction.delete("nom")
        self.canevasaction.create_text(100, 30, text=self.nom_joueur_local, font=("arial", 18, "bold"), anchor=S,
                                       tags=("nom"))

        # on cree les cadres affichant les items d'actions du joueur
        # cadre apparaissant si on selectionne un ouvrier
        coul = self.modele.joueurs[self.parent.nom_joueur_local].couleur
        self.cadrejeuinfo.config(bg=coul[1])
        self.creer_aide()
        self.creer_cadre_ouvrier(coul[0] + "_", ["maison", "caserne", "abri", "usineballiste"])
        self.creer_chatter()
        # on affiche les maisons, point de depart des divers joueurs
        self.afficher_depart()
        self.root.update()
        # self.centrer_maison()

    def creer_cadre_ouvrier(self, coul, artefacts):
        self.cadreouvrier = Frame(self.canevasaction)
        for i in artefacts:
            btn = Button(self.cadreouvrier, text=i, image=self.images[coul + i])
            btn.bind("<Button>", self.batir_artefact)
            btn.pack()

    ##FONCTIONS D'AFFICHAGES##################################
    def afficher_depart(self):
        self.modele.listebiotopes.sort(key=lambda c: c.y)
        for i in self.modele.listebiotopes:
            if i.montype == "daim":
                monitem = self.canevas.create_image(i.x, i.y, image=self.images[i.img], anchor=S,
                                                    tags=("mobile", "", i.id, "biotope", i.montype, ""))
                # tags=("mobile","",i.id,)
            else:
                monitem = self.canevas.create_image(i.x, i.y, image=self.images[i.img], anchor=S,
                                                    tags=("statique", "", i.id, "biotope", i.montype, ""))
                # tags=("mobile","",i.id,)

        self.modele.listebiotopes = []
        minitaillecase = int(self.tailleminicarte / self.modele.taillecarte)
        couleurs = {0: "",
                    "arbre": "light green",
                    "eau": "light blue",
                    "aureus": "tan",
                    "roche": "gray30",
                    "marais": "orange"}
        for i, t in enumerate(self.modele.regions):
            if t != "plaine":
                for j, c in enumerate(self.modele.regions[t]):
                    for cle, k in self.modele.regions[t][c].dicocases.items():
                        y1 = k.y * minitaillecase
                        y2 = y1 + minitaillecase
                        x1 = k.x * minitaillecase
                        x2 = x1 + minitaillecase
                        self.minicarte.create_rectangle(x1, y1, x2, y2, outline="",
                                                        # fill=couleurs[self.modele.cartecase[k[1]][k[0]].type]),
                                                        fill=couleurs[k.parent.montype])

        # Affichage des batiments intiaux sur l'aire de jeu et sur la minicarte
        px = int(self.tailleminicarte / self.modele.aireX)
        py = int(self.tailleminicarte / self.modele.aireY)

        for j in self.modele.joueurs.keys():
            for i in self.modele.joueurs[j].batiments["maison"].keys():
                m = self.modele.joueurs[j].batiments["maison"][i]
                coul = self.modele.joueurs[j].couleur[0]
                self.canevas.create_image(m.x, m.y, image=self.images[coul + "_maison"],
                                          tags=("statique", j, m.id, "batiment", m.montype, ""))
                # tags=("mobile","",i.id,)
                # afficher sur minicarte
                coul = self.modele.joueurs[j].couleur[1]
                x1 = int((m.x / self.modele.aireX) * self.tailleminicarte)
                y1 = int((m.y / self.modele.aireY) * self.tailleminicarte)
                self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=coul,
                                                tags=(j, m.id, "artefact", "maison"))

    def afficher_bio(self, bio):
        self.canevas.create_image(bio.x, bio.y, image=self.images[bio.img],
                                  tags=("statique", "", bio.id, "biotope", bio.montype, ""))

    def afficher_batiment(self, joueur, batiment):
        coul = self.modele.joueurs[joueur].couleur[0]

        self.canevas.delete(batiment.id)

        print(self.parent.nom_joueur_local)
        chose = self.canevas.create_image(batiment.x, batiment.y, image=self.images[batiment.image],
                                          tags=(
                                              "statique", self.parent.nom_joueur_local, batiment.id, "batiment",
                                              batiment.montype,
                                              ""))

        x0, y0, x2, y2 = self.canevas.bbox(chose)

        couleurs = {0: "",
                    1: "light green",
                    2: "light blue",
                    3: "tan",
                    4: "gray30",
                    5: "orange"}
        coul = self.modele.joueurs[joueur].couleur[1]
        x1 = int((batiment.x / self.modele.aireX) * self.tailleminicarte)
        y1 = int((batiment.y / self.modele.aireY) * self.tailleminicarte)
        self.minicarte.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill=coul,
                                        tags=(self.parent.nom_joueur_local, batiment.id, "artefact", batiment.montype))
        return [x0, y0, x2, y2]

    def afficher_jeu(self):

        # On efface tout ce qui est 'mobile' (un tag)
        self.canevas.delete("mobile")

        # on se debarrasse des choses mortes (disparues), le id est dans le tag du dessin
        for i in self.modele.ressourcemorte:
            self.canevas.delete(i.id)

        # commencer par les choses des joueurs
        for j in self.modele.joueurs.keys():
            # ajuster les infos du HUD
            if self.limbo == 1:
                self.cadrejeuinfo.destroy()
                self.canevasaction.destroy()
                self.canevasaction = Canvas(self.cadreaction, width=200, height=300, bg="lightblue",
                                            yscrollcommand=self.scrollVaction.set)
                self.canevasaction.grid(row=0, column=0, sticky=N + S)
                self.canevasaction.create_text(100, 30, text="Vous êtes mort", font=("arial", 18, "bold"),
                                               anchor=S,
                                               tags=("nom"))
                self.canevasaction.create_text(100, 60, text="Joueurs Restant", font=("arial", 12, "bold"),
                                               anchor=S,
                                               tags=("nom"))

                # update lsit of dead for everyone bug
                i = 30
                for t in self.modele.joueurs.keys():
                    if t != self.parent.nom_joueur_local:
                        self.canevasaction.create_text(100, 80 + i, text=t, font=("arial", 10, "bold"),
                                                       anchor=S,
                                                       tags=("nom"))
                        i += 30

                self.canevasaction.rowconfigure(0, weight=1)

            elif j == self.parent.nom_joueur_local:
                self.infohud["Nourriture"][0].set(self.modele.joueurs[j].ressources["nourriture"])
                self.infohud["Bois"][0].set(self.modele.joueurs[j].ressources["arbre"])
                self.infohud["Roche"][0].set(self.modele.joueurs[j].ressources["roche"])
                self.infohud["Aureus"][0].set(self.modele.joueurs[j].ressources["aureus"])
                self.infohud["msggeneral"][0].config(text=self.modele.msggeneral)

            # ajuster les constructions de chaque joueur
            for p in self.modele.joueurs[j].batiments['siteconstruction']:
                s = self.modele.joueurs[j].batiments['siteconstruction'][p]
                if s.etat == "attente":
                    self.canevas.create_image(s.x, s.y, anchor=CENTER, image=self.images["siteX"],
                                              tags=("mobile", j, p, "batiment", type(s).__name__, ""))
                    # tags=(j,s.id,"artefact","mobile","siteconstruction","batiments"))
                else:
                    self.canevas.create_image(s.x, s.y, anchor=CENTER, image=self.images["EnConstruction"],
                                              tags=("mobile", j, p, "batiment", type(s).__name__, ""))

            # ajuster les persos de chaque joueur et leur dépendance (ici javelots des ouvriers)
            for p in self.modele.joueurs[j].persos.keys():
                for k in self.modele.joueurs[j].persos[p].keys():
                    i = self.modele.joueurs[j].persos[p][k]
                    coul = self.modele.joueurs[j].couleur[0]
                    self.canevas.create_image(i.x, i.y, anchor=S, image=self.images[i.image],
                                              tags=("mobile", j, k, "perso", i.montype))
                    # tags=(j,k,"artefact","mobile","perso",p))
                    if k in self.action.persochoisi:
                        self.canevas.create_rectangle(i.x - 10, i.y + 5, i.x + 10, i.y + 10, fill="yellow",
                                                      tags=("mobile", j, p, "perso", type(i).__name__, "persochoisi"))
                        # tags=(j,k,"artefact","mobile","persochoisi"))

                    # dessiner javelot de l'ouvrier
                    if p == "ouvrier":
                        for b in self.modele.joueurs[j].persos[p][k].javelots:
                            self.canevas.create_image(b.x, b.y, image=self.images[b.image],
                                                      tags=("mobile", j, b.id, "", type(b).__name__, ""))
                    if p == "ballista" or p == "archer":
                        for b in self.modele.joueurs[j].persos[p][k].fleches:
                            self.canevas.create_image(b.x, b.y, image=self.images[b.image],
                                                      tags=("mobile", j, b.id, "", type(b).__name__, ""))
                            # tags=(j,b.id,"artefact","mobile","javelot"))

        # ajuster les choses vivantes dependantes de la partie (mais pas des joueurs)
        for j in self.modele.biotopes["daim"].keys():
            i = self.modele.biotopes["daim"][j]
            if i.etat == "mort":
                self.canevas.create_image(i.x, i.y, image=self.images["daimMORT"],
                                          tags=("mobile", "", i.id, "biotope", i.montype, ""))
                # tags=("",i.id,"artefact","daim","mobile"))

            else:
                self.canevas.create_image(i.x, i.y, image=self.images[i.img],
                                          tags=("mobile", "", i.id, "biotope", i.montype, ""))
                # tags=("",i.id,"artefact","daim","mobile"))

        # ajuster les choses vivantes dependantes de la partie (mais pas des joueurs)
        for j in self.modele.biotopes["eau"].keys():
            i = self.modele.biotopes["eau"][j]
            if i.sprite:
                self.canevas.create_image(i.x, i.y, image=self.gifs[i.sprite][i.spriteno],
                                          tags=("mobile", "", i.id, "biotope", type(i).__name__, ""))
                # tags=("",i.id,"artefact","eau","mobile"))

        # mettre les chat a jour si de nouveaux messages sont arrives
        if self.textchat and self.modele.joueurs[self.parent.nom_joueur_local].chatneuf:
            self.textchat.delete(0, END)
            self.textchat.insert(END, *self.modele.joueurs[self.parent.nom_joueur_local].monchat)
            if self.modele.joueurs[self.parent.nom_joueur_local].chatneuf and self.action.chaton == 0:
                self.btnchat.config(bg="orange")
            self.modele.joueurs[self.parent.nom_joueur_local].chatneuf = 0

    def supprimer_batiment(self, id_batiment):
        self.canevas.delete(id_batiment)

    def centrer_maison(self):
        self.root.update()
        cle = list(self.modele.joueurs[self.nom_joueur_local].batiments["maison"].keys())[0]
        x = self.modele.joueurs[self.nom_joueur_local].batiments["maison"][cle].x
        y = self.modele.joueurs[self.nom_joueur_local].batiments["maison"][cle].y

        x1 = self.canevas.winfo_width() / 2
        y1 = self.canevas.winfo_height() / 2

        pctx = (x - x1) / self.modele.aireX
        pcty = (y - y1) / self.modele.aireY

        self.canevas.xview_moveto(pctx)
        self.canevas.yview_moveto(pcty)

    ##### ACTIONS DU JOUEUR #######################################################################

    def annuler_action(self, evt):
        mestags = self.canevas.gettags(CURRENT)
        if not mestags:
            self.canevasaction.delete(self.action.widgetsactifs)
            if self.action.btnactif:
                self.action.btnactif.config(bg="SystemButtonFace")
            self.action = Action(self)

    def fermer_chat(self):
        self.textchat = None
        self.fenchat.destroy()

    def ajouter_selection(self, evt):
        mestags = self.canevas.gettags(CURRENT)
        print("MESTAGS", mestags)
        if self.parent.nom_joueur_local == mestags[1]:
            if "ouvrier" == mestags[4]:
                self.action.persochoisi.append(mestags[2])
                self.action.afficher_commande_perso()
            else:
                self.action.persochoisi.append(mestags[2])
        elif self.action.persochoisi != []:
            self.action.ciblechoisi = mestags
            self.action.attaquer()

    # Methodes pour multiselect
    def debuter_selection(self, evt):
        self.debutselect = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        x1, y1 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
        self.selecteuractif = self.canevas.create_rectangle(x1, y1, x1 + 1, y1 + 1, outline="red", width=2,
                                                            dash=(2, 2), tags=("", "selecteur", "", "artefact"))

    def afficher_selection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.canevas.coords(self.selecteuractif, x1, y1, x2, y2)

    def terminer_selection(self, evt):
        if self.debutselect:
            x1, y1 = self.debutselect
            x2, y2 = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.debutselect = []
            objchoisi = (list(self.canevas.find_enclosed(x1, y1, x2, y2)))
            for i in objchoisi:
                if self.parent.nom_joueur_local not in self.canevas.gettags(i):
                    objchoisi.remove(i)
                else:
                    self.action.persochoisi.append(self.canevas.gettags(i)[2])

            if self.action.persochoisi:
                self.action.afficher_commande_perso()
            self.canevas.delete("selecteur")

    ### FIN du multiselect

    def ramasser_ressource(self, evt):
        tag = self.canevas.gettags(CURRENT)
        if tag[1] == "" and self.action.persochoisi:
            self.action.ramasser_ressource(tag)
        else:
            print(tag[4])

    def chasser_ressource(self, evt):
        tag = self.canevas.gettags(CURRENT)
        if tag[1] == "" and self.action.persochoisi and tag[4] == "daim":
            self.action.chasser_ressource(tag)
        else:
            print(tag[3])

    def indiquer_position(self, evt):
        tag = self.canevas.gettags(CURRENT)
        if not tag:
            x, y = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.action.position = [x, y]
            self.action.deplacer()

    # Cette fonction permet se se deplacer via un click sur la minicarte
    def deplacer_carte(self, evt):
        x = evt.x
        y = evt.y

        pctx = x / self.tailleminicarte
        pcty = y / self.tailleminicarte

        xl = (self.canevas.winfo_width() / 2) / self.modele.aireX
        yl = (self.canevas.winfo_height() / 2) / self.modele.aireY

        self.canevas.xview_moveto(pctx - xl)
        self.canevas.yview_moveto(pcty - yl)
        xl = self.canevas.winfo_width()
        yl = self.canevas.winfo_height()

    def batir_artefact(self, evt):
        obj = evt.widget
        if self.action.btnactif:
            if self.action.btnactif != obj:
                self.action.btnactif.config(bg="SystemButtonFace")
        # test de cout a cet endroit
        nomsorte = obj.cget("text")
        self.action.btnactif = obj

        vals = self.parent.trouver_valeurs()
        print(vals)
        ok = 1
        for k, val in self.modele.joueurs[self.nom_joueur_local].ressources.items():
            if val <= vals[nomsorte][k]:
                ok = 0
                break
        if ok:
            self.action.prochaineaction = obj.cget("text")
            obj.config(bg="lightgreen")
        else:
            print("VOUS N'AVEZ PAS ASSEZ DE", k)

    def construire_batiment(self, evt):
        mestags = self.canevas.gettags(CURRENT)

        if not mestags:
            pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
            self.action.construire_batiment(pos)
        elif "SiteConstruction" in mestags:  # permet de continuer une constuction de site de construction
            pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y), mestags[2])
            self.action.prochaineaction = "siteconstruction"
            self.action.continuer_construction(pos)

    def creer_entite(self, evt):
        x, y = evt.x, evt.y
        mestags = self.canevas.gettags(CURRENT)
        if self.parent.nom_joueur_local in mestags:
            if "batiment" in mestags:
                if "maison" in mestags:
                    pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
                    action = [self.parent.nom_joueur_local, "creerperso", ["ouvrier", mestags[4], mestags[2], pos]]
                if "caserne" in mestags:
                    pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
                    action = [self.parent.nom_joueur_local, "creerperso", ["soldat", mestags[4], mestags[2], pos]]
                if "abri" in mestags:
                    pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
                    action = [self.parent.nom_joueur_local, "creerperso", ["druide", mestags[4], mestags[2], pos]]
                if "usineballiste" in mestags:
                    pos = (self.canevas.canvasx(evt.x), self.canevas.canvasy(evt.y))
                    action = [self.parent.nom_joueur_local, "creerperso", ["ballista", mestags[4], mestags[2], pos]]

            try:
                self.parent.actions_requises.append(action)
            except:
                print("action invalide")


        elif self.action.persochoisi != []:
            self.action.ciblechoisi = mestags
            self.action.attaquer()

    # Ajout pour affichage de fin

    def test(self, evt):
        # print("DANS TEST DE FIN")

        self.changer_cadre("fin")

    def unbind_joueur(self):
        # unbind tout ou juste le tick sur les joueur ?
        # test sur self

        self.canevas.tag_unbind("perso", "<Button-1>")

        # on attache (bind) desF événements soit aux objets eux même
        # self.canevas.bind("<Button-1>", self.annuler_action)
        # self.canevas.bind("<Button-3>", self.construire_batiment)
        # # faire une multiselection
        # self.canevas.bind("<Shift-Button-1>", self.debuter_selection)
        # self.canevas.bind("<Shift-B1-Motion>", self.afficher_selection)
        # self.canevas.bind("<Shift-ButtonRelease-1>", self.terminer_selection)
        #
        # self.canevas.bind("<Button-2>", self.indiquer_position)
        #
        # self.canevas.bind("<MouseWheel>", self.OnMouseWheel)
        # self.canevas.bind("<Control-MouseWheel>", self.OnCtrlMouseWheel)
        #
        # # soit aux dessins, en vertu de leur tag (propriétés des objets dessinés)
        # # ALL va réagir à n'importe quel dessin
        # # sinon on spécifie un tag particulier, exemple avec divers tag, attaché par divers événements
        # self.canevas.tag_bind("batiment", "<Button-1>", self.creer_entite)
        # self.canevas.tag_bind("perso", "<Button-1>", self.ajouter_selection)
        # self.canevas.tag_bind("arbre", "<Button-1>", self.ramasser_ressource)
        # self.canevas.tag_bind("aureus", "<Button-1>", self.ramasser_ressource)
        # self.canevas.tag_bind("roche", "<Button-1>", self.ramasser_ressource)
        # self.canevas.tag_bind("baie", "<Button-1>", self.ramasser_ressource)
        # self.canevas.tag_bind("eau", "<Button-1>", self.ramasser_ressource)
        # self.canevas.tag_bind("daim", "<Button-1>", self.chasser_ressource)


# Singleton (mais pas automatique) sert a conserver les manipulations du joueur
# pour demander une action
class Action():
    def __init__(self, parent):
        self.parent = parent
        self.persochoisi = []
        self.ciblechoisi = None
        self.position = []
        self.btnactif = None
        self.prochaineaction = None
        self.widgetsactifs = []
        self.chaton = 0
        self.aideon = 0

    def attaquer(self):
        if self.persochoisi:
            qui = self.ciblechoisi[1]
            cible = self.ciblechoisi[2]
            sorte = self.ciblechoisi[4]
            print("Vue attaquer, sorte, self.ciblechoisi", sorte, self.ciblechoisi[4])
            action = [self.parent.parent.nom_joueur_local, "attaquer", [self.persochoisi, [qui, cible, sorte]]]
            self.parent.parent.actions_requises.append(action)

    def deplacer(self):
        if self.persochoisi:
            action = [self.parent.parent.nom_joueur_local, "deplacer", [self.position, self.persochoisi]]
            self.parent.parent.actions_requises.append(action)

    def chasser_ressource(self, tag):
        if self.persochoisi:
            action = [self.parent.parent.nom_joueur_local, "chasserressource", [tag[4], tag[2], self.persochoisi]]
            self.parent.parent.actions_requises.append(action)

    def ramasser_ressource(self, tag):
        if self.persochoisi:
            action = [self.parent.parent.nom_joueur_local, "ramasserressource", [tag[4], tag[2], self.persochoisi]]
            self.parent.parent.actions_requises.append(action)

    def construire_batiment(self, pos):
        self.btnactif.config(bg="SystemButtonFace")
        self.btnactif = None
        action = [self.parent.nom_joueur_local, "construirebatiment", [self.persochoisi, self.prochaineaction, pos]]
        self.parent.parent.actions_requises.append(action)

    def continuer_construction(self, pos):
        action = [self.parent.nom_joueur_local, "construirebatiment", [self.persochoisi, self.prochaineaction, pos]]
        self.parent.parent.actions_requises.append(action)

    def afficher_commande_perso(self):
        self.widgetsactifs = self.parent.canevasaction.create_window(100, 60,
                                                                     window=self.parent.cadreouvrier,
                                                                     anchor=N)
        self.parent.root.update()
        fh = self.parent.cadreouvrier.winfo_height()
        ch = int(self.parent.canevasaction.cget("height"))
        if fh + 60 > ch:
            cl = int(self.parent.canevasaction.cget("width"))
            self.parent.canevasaction.config(scrollregion=(0, 0, cl, fh + 60))

    def envoyer_chat(self, evt):
        txt = self.parent.entreechat.get()
        joueur = self.parent.joueurs.get()
        if joueur:
            action = [self.parent.nom_joueur_local, "chatter",
                      [self.parent.nom_joueur_local + ": " + txt, self.parent.nom_joueur_local, joueur]]
            self.parent.parent.actions_requises.append(action)

    def chatter(self):
        if self.chaton == 0:
            x1, x2 = self.parent.scrollH.get()
            x3 = self.parent.modele.aireX * x1
            y1, y2 = self.parent.scrollV.get()
            y3 = self.parent.modele.aireY * y1
            self.parent.cadrechaton = self.parent.canevas.create_window(x3, y3,
                                                                        window=self.parent.cadrechat,
                                                                        anchor=N + W)
            self.parent.btnchat.config(bg="SystemButtonFace")
            self.chaton = 1
        else:
            self.parent.canevas.delete(self.parent.cadrechaton)
            self.parent.cadrechaton = 0
            self.chaton = 0

    def aider(self):
        if self.aideon == 0:
            x1, x2 = self.parent.scrollH.get()
            x3 = self.parent.modele.aireX * x2
            y1, y2 = self.parent.scrollV.get()
            y3 = self.parent.modele.aireY * y1
            self.aideon = self.parent.canevas.create_window(x3, y3,
                                                            window=self.parent.cadreaide,
                                                            anchor=N + E)
        else:
            self.parent.canevas.delete(self.aideon)
            self.aideon = 0

    # //changer aort
    def abandonner(self, param):
        pass

    ### FIN des methodes pour lancer la partie


# classe qui est une sous-classe d'une classe tkinter dont on change les proprietes
class Champ(Label):
    def __init__(self, master, *args, **kwargs):  # keyword arg = nom arg = certaine valeur. Comme un dict
        Label.__init__(self, master, *args, **kwargs)
        self.config(font=("arial", 13, "bold"))
        self.config(bg="goldenrod3")
