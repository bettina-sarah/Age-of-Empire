import random
import math
from tkinter import CURRENT

from helper import Helper
from AoEw_divers import *
from AoEw_batiments import *
from AoEw_persos import *


class Joueur():
    valeurs = {"maison": {"nourriture": 10,
                          "arbre": 20,
                          "roche": 20,
                          "aureus": 2,
                          "delai": 50,
                          "objet": 0},
               "abri": {"nourriture": 10,
                        "arbre": 10,
                        "roche": 5,
                        "aureus": 1,
                        "delai": 30,
                        "objet": 0},
               "caserne": {"nourriture": 10,
                           "arbre": 10,
                           "roche": 5,
                           "aureus": 1,
                           "delai": 60,
                           "objet": 0},
               "usineballiste": {"nourriture": 10,
                                 "arbre": 10,
                                 "roche": 5,
                                 "aureus": 1,
                                 "delai": 80,
                                 "objet": 0},
               "siteconstruction": {"nourriture": 0,
                                    "arbre": 0,
                                    "roche": 0,
                                    "aureus": 0,

                                    "delai": 0,
                                    "objet": 0},
               "champstir": {"nourriture": 10,
                             "arbre": 10,
                             "roche": 10,
                             "aureus": 10,
                             "delai": 20,
                             "objet": 0},
               "mur_dh": {"nourriture": 5,
                         "arbre": 5,
                         "roche": 5,
                         "aureus": 5,
                         "delai": 5,
                         "objet": 0},
               "mur_db": {"nourriture": 5,
                         "arbre": 5,
                         "roche": 5,
                         "aureus": 5,
                         "delai": 5,
                         "objet": 0},
               "mur_gh": {"nourriture": 5,
                          "arbre": 5,
                          "roche": 5,
                          "aureus": 5,
                          "delai": 5,
                          "objet": 0},
               "mur_gb": {"nourriture": 5,
                          "arbre": 5,
                          "roche": 5,
                          "aureus": 5,
                          "delai": 5,
                          "objet": 0},
               "tour": {"nourriture": 25,
                        "arbre": 25,
                        "roche": 25,
                        "aureus": 25,
                        "delai": 15,
                        "objet": 0},
               }

    prix_unite = {"ouvrier": {"nourriture": 10,
                              "arbre": 10,
                              "roche": 10,
                              "aureus": 2,
                              "delai": 50,
                              "objet": 0
                              },

                  "soldat": {"nourriture": 10,
                             "arbre": 10,
                             "roche": 5,
                             "aureus": 2,
                             "delai": 30,
                             "objet": 0
                             },

                  "chevalier": {"nourriture": 10,
                                "arbre": 10,
                                "roche": 5,
                                "aureus": 1,
                                "delai": 60,
                                "objet": 0
                                },

                  "druide": {"nourriture": 10,
                             "arbre": 10,
                             "roche": 35,
                             "aureus": 31,
                             "delai": 80,
                             "objet": 2
                             },

                  "druideOurs": {"nourriture": 15,
                                 "arbre": 12,
                                 "roche": 35,
                                 "aureus": 34,
                                 "delai": 80,
                                 "objet": 5
                                 },

                  "ballista": {"nourriture": 30,
                               "arbre": 30,
                               "roche": 30,
                               "aureus": 30,

                               "delai": 30,
                               "objet": 0},
                  
                  "catapulte": {"nourriture": 30,
                               "arbre": 30,
                               "roche": 30,
                               "aureus": 30,

                               "delai": 30,
                               "objet": 0},

                  "ingenieur": {"nourriture": 30,
                                "arbre": 30,
                                "roche": 30,
                                "aureus": 2,
                                "delai": 30,
                                "objet": 5},

                  "archer": {"nourriture": 35,
                             "arbre": 35,
                             "roche": 35,
                             "aureus": 30,
                             "delai": 30,
                             "objet": 0},

                  "cavalierarcher": {"nourriture": 35,
                             "arbre": 35,
                             "roche": 35,
                             "aureus": 30,
                             "delai": 30,
                             "objet": 0}

                  }

    classespersos = {"ouvrier": Ouvrier,
                     "soldat": Soldat,
                     "archer": Archer,
                     "chevalier": Chevalier,
                     "druide": Druide,
                     "ballista": Ballista,
                     "ingenieur": Ingenieur,
                     "druideOurs": DruideOurs,
                     "cavalierarcher": CavalierArcher,
                     "catapulte": Catapulte}

    ressources = {"Azteque": {"nourriture": 999,
                              "arbre": 200,
                              "roche": 200,
                              "aureus": 200},
                  "Congolaise": {"nourriture": 10,
                                 "arbre": 200,
                                 "roche": 200,
                                 "aureus": 888888888},
                  }

    def __init__(self, parent, id, nom, couleur, x, y):
        self.parent = parent
        self.nom = nom
        self.id = id
        self.x = x
        self.y = y
        self.event = None
        self.couleur = couleur
        self.monchat = []
        self.chatneuf = 0
        self.ressourcemorte = []
        self.delai_max = 50

        self.delai_perso = {"ouvrier": 0,
                            "soldat": 0,
                            "archer": 0,
                            "chevalier": 0,
                            "cavalierarcher":0,
                            "druide": 0,
                            "ballista": 0,
                            "ingenieur": 0,
                            "druideOurs": 0}

        self.ressources = {"nourriture": 500,
                           "arbre": 500,
                           "roche": 500,
                           "aureus": 500,
                           "objet": 10}

        self.persos = {"ouvrier": {},
                       "soldat": {},
                       "archer": {},
                       "chevalier": {},
                       "druide": {},
                       "druideOurs": {},
                       "ingenieur": {},
                       "ballista": {},
                       "cavalierarcher": {},
                       "catapulte":{}
                       }

        self.batiments = {"maison": {},
                          "abri": {},
                          "caserne": {},
                          "usineballiste": {},
                          "siteconstruction": {},
                          "champstir": {},
                          "mur_db": {},
                          "mur_dh": {},
                          "mur_gb": {},
                          "mur_gh": {},
                          "tour": {}}

        self.actions = {"creerperso": self.creer_perso,
                        "deplacer": self.deplacer,
                        "ramasserressource": self.ramasser_ressource,
                        "chasserressource": self.chasser_ressource,
                        "construirebatiment": self.construire_batiment,
                        "attaquer": self.attaquer,
                        "soigner": self.soigner,
                        "chatter": self.chatter,
                        "abandonner": self.abandonner}
        # on va creer une maison comme centre pour le joueur
        self.creer_point_origine(x, y)

    def annoncer_mort(self, perso):
        try:
            self.persos[perso.montype].pop(perso.id)
            self.parent.trouver_case(perso.x, perso.y).persos.pop(perso.id)
        except:
            print("Deja Mort")

    def annoncer_mort_batiment(self, perso):
        # retirer de la minimap
        # placer les case à plaine
        # retirer de l'image de l'affichage
        self.batiments[perso.montype].pop(perso.id)
        self.parent.retirer_batiment_minimap(perso.id)
        self.parent.parent.supprimer_batiment(perso.id, self.nom)
        self.parent.reset_case_batiment(perso.cartebatiment)

    ##mourir handled par le joueur
    def eliminer_joueur(self):
        self.parent.eliminer_joueur()

    def attaquer(self, param):
        attaquants, attaque = param
        # Joueurs attaquants et attaque['id_44859', 'id_44925']['JAJA_512', 'id_44868', 'ballista']
        nomjoueur, idperso, sorte = attaque

        if sorte in self.batiments.keys():
            ennemi = self.parent.joueurs[nomjoueur].batiments[sorte][idperso]
        else:
            ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]
            
        for i in self.persos.keys():
            for j in attaquants:
                if j in self.persos[i]:
                    self.persos[i][j].attaquer(ennemi)
                    # j.attaquer(ennemi)

    def soigner(self, param):
        soigneur, cible = param

        nomjoueur, idperso, sorte = cible

        if sorte in self.batiments.keys():
            cible = self.parent.joueurs[nomjoueur].batiments[sorte][idperso]
        else:
            cible = self.parent.joueurs[nomjoueur].persos[sorte][idperso]


        # ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]
        try:

            temp = self.persos["druide"].get(soigneur[0])
            if temp == None:
                temp = self.persos["druideOurs"].get(soigneur[0])

            temp.soigner(cible)
        except AttributeError:
            print("error")
            # trouver next ?

    # changer a mort
    def abandonner(self, param):
        # ajouter parametre nom de l'Abandonneux, et si c'est moi, envoyer une action
        # quitter au serveur et faire destroy
        msg = param[0]

        self.parent.mort = param[1]
        # update everyone`s list

        self.parent.montrer_msg_general(msg)

    def chatter(self, param):
        txt, envoyeur, receveur = param
        self.parent.joueurs[envoyeur].monchat.append(txt)
        self.parent.joueurs[receveur].monchat.append(txt)
        self.parent.joueurs[envoyeur].chatneuf = 1
        self.parent.joueurs[receveur].chatneuf = 1

    def avertir_ressource_mort(self, type, ress):
        for i in self.persos["ouvrier"]:
            self.persos["ouvrier"][i].abandonner_ressource(ress)  # ajouer libereressource
        self.parent.eliminer_ressource(type, ress)

    def chasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "ouvrier":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerproie")

    def ramasser_ressource(self, param):
        typeress, idress, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if j == "ouvrier":
                    if i in self.persos[j]:
                        self.persos[j][i].chasser_ramasser(self.parent.biotopes[typeress][idress],
                                                           typeress, "ciblerressource")

    def deplacer(self, param):
        pos, troupe = param
        for i in troupe:
            for j in self.persos.keys():
                if i in self.persos[j]:
                    self.persos[j][i].deplacer(pos)

    def creer_point_origine(self, x, y):
        idmaison = get_prochain_id()
        batiment = Maison(self, idmaison, self.couleur, x, y, "maison")
        self.batiments["maison"][idmaison] = batiment


        #TOUJOURS PREND SET COINS
        # batiment.set_coins(x1 * self.taillecase, y1* self.taillecase , x4* self.taillecase, y4* self.taillecase)
        # batiment.cartebatiment = cartebatiment

    def construire_batiment(self, param):
        siteconstruction = None

        if len(param) == 3:
            perso, sorte, pos = param
        else:
            sorte, pos = param

        if sorte == "siteconstruction":
            try:
                siteconstruction = self.batiments["siteconstruction"][pos[2]]
            except:
                siteconstruction = None
        else:
            id = get_prochain_id()
            # payer batiment
            vals = Joueur.valeurs
            for k, val in self.ressources.items():
                if k != "objet":
                    self.ressources[k] = val - vals[sorte][k]
                    self.ressources[k] = val - vals[sorte][k]

            siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte,
                                                Joueur.valeurs[sorte]["delai"])
            self.batiments["siteconstruction"][id] = siteconstruction

        if siteconstruction:
            if perso:
                for i in perso:
                    try:
                        self.persos["ouvrier"][i].construire_site_construction(siteconstruction)
                    except:
                        print("must be the wind")

    def installer_batiment(self, batiment):
        self.parent.installer_batiment(self.nom, batiment)

    # transmet à tous ses persos de jouer
    def jouer_prochain_coup(self):
        for j in list(self.persos.keys()):
            for i in list(self.persos[j].keys()):
                self.persos[j][i].jouer_prochain_coup()

        for i in list(self.batiments["tour"].keys()):
            self.batiments["tour"][i].jouer_prochain_coup()

    def creer_perso(self, param):
        sorteperso, batimentsource, idbatiment, pos = param
        # if idbatiment in self.batiments[batimentsource].keys():
        # le joueur a-t-il les ressources pour creer l'unité
        prix_perso = Joueur.prix_unite
        possede_les_ressources = True

        for k, val in self.ressources.items():
            if self.ressources[k] - prix_perso[sorteperso][k] < 0:
                    possede_les_ressources = False

        if possede_les_ressources:
                # paye les ressources
            for k, val in self.ressources.items():
                    self.ressources[k] = val - prix_perso[sorteperso][k]

            id = get_prochain_id()
            batiment = self.batiments[batimentsource][idbatiment]
            x = batiment.x + 100 + (random.randrange(50) - 15)
            y = batiment.y + (random.randrange(50) - 15)
            self.delai_perso[sorteperso] = self.delai_max
            self.persos[sorteperso][id] = Joueur.classespersos[sorteperso](self, id, batiment, self.couleur, x, y,
                                                                               sorteperso)
    def delai_boucle(self):

        for sorte, value in self.delai_perso.items():

            if value > 0:
                self.delai_perso[sorte] -= 1
            else:
                self.delai_perso[sorte] = 0
