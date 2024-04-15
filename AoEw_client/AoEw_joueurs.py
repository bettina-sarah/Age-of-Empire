import random
import math
from helper import Helper
from AoEw_divers import *
from AoEw_batiments import *
from AoEw_persos import *

class Joueur():
    valeurs = {"maison": {"nourriture": 10,
                          "arbre": 20,
                          "roche": 20,
                          "aureus": 2,
                          "delai": 50},
               "abri": {"nourriture": 10,
                        "arbre": 10,
                        "roche": 5,
                        "aureus": 1,
                        "delai": 30},
               "caserne": {"nourriture": 10,
                           "arbre": 10,
                           "roche": 5,
                           "aureus": 1,
                           "delai": 60},
               "usineballiste": {"nourriture": 10,
                                 "arbre": 10,
                                 "roche": 5,
                                 "aureus": 1,
                                 "delai": 80},
               "siteconstruction": {"nourriture": 0,
                                 "arbre": 0,
                                 "roche": 0,
                                 "aureus": 0,
                                 "delai": 0}
               }

    prix_unite = {"ouvrier": {"nourriture": 10,
                          "arbre": 10,
                          "roche": 10,
                          "aureus": 2,
                          "delai": 50},
               "soldat": {"nourriture": 10,
                        "arbre": 10,
                        "roche": 5,
                        "aureus": 1,
                        "delai": 30},
               "chevalier": {"nourriture": 10,
                           "arbre": 10,
                           "roche": 5,
                           "aureus": 1,
                           "delai": 60},
               "druide": {"nourriture": 10,
                                 "arbre": 10,
                                 "roche": 35,
                                 "aureus": 31,
                                 "delai": 80},
               "ballista": {"nourriture": 30,
                                 "arbre": 30,
                                 "roche": 30,
                                 "aureus": 30,
                                 "delai": 30},
               "ingenieur": {"nourriture": 30,
                            "arbre": 30,
                            "roche": 30,
                            "aureus": 30,
                            "delai": 30}
               }

    classespersos = {"ouvrier": Ouvrier,
                     "soldat": Soldat,
                     "archer": Archer,
                     "chevalier": Chevalier,
                     "druide": Druide,
                     "ballista": Ballista,
                     "ingenieur": Ingenieur}
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
        self.couleur = couleur
        self.monchat = []
        self.chatneuf = 0
        self.ressourcemorte = []
        self.ressources = {"nourriture": 200,
                           "arbre": 200,
                           "roche": 200,
                           "aureus": 200}
        self.persos = {"ouvrier": {},
                       "soldat": {},
                       "archer": {},
                       "chevalier": {},
                       "druide": {},
                       "ingenieur": {},
                       "ballista": {},
                       }


        self.batiments = {"maison": {},
                          "abri": {},
                          "caserne": {},
                          "usineballiste": {},
                          "siteconstruction": {}}

        self.actions = {"creerperso": self.creer_perso,
                        "deplacer": self.deplacer,
                        "ramasserressource": self.ramasser_ressource,
                        "chasserressource": self.chasser_ressource,
                        "construirebatiment": self.construire_batiment,
                        "attaquer": self.attaquer,
                        "chatter": self.chatter,
                        "abandonner": self.abandonner}
        # on va creer une maison comme centre pour le joueur
        self.creer_point_origine(x, y)

    def annoncer_mort(self, perso):
        print("==================pop suite a mort")
        self.persos[perso.montype].pop(perso.id)

    def annoncer_mort_batiment(self, perso):

        print("batiment mort!")
        # retirer de la minimap
        # placer les case à plaine
        # retirer de l'image de l'affichage
        self.batiments[perso.montype].pop(perso.id)
        self.parent.retirer_batiment_minimap(perso.id)
        self.parent.parent.supprimer_batiment(perso.id)
        self.parent.reset_case_batiment(perso.cartebatiment)



    def attaquer(self, param):
        print("PARAM", param)
        attaquants, attaque = param
        print("Joueurs attaquants et attaque",attaquants, attaque)

        nomjoueur, idperso, sorte = attaque

        if sorte in self.batiments.keys():
            ennemi = self.parent.joueurs[nomjoueur].batiments[sorte][idperso]
            print("ENNEMI BATIMENT: ", ennemi)
        else:
            ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]
            print("ENNEMI PERSO: ", ennemi)
        # print("Nom joueur, idperso, sorte", nomjoueur, idperso, sorte)

        # ennemi = self.parent.joueurs[nomjoueur].persos[sorte][idperso]
        for i in self.persos.keys():
            for j in attaquants:
                if j in self.persos[i]:
                    self.persos[i][j].attaquer(ennemi)
                    # j.attaquer(ennemi)

    def abandonner(self, param):
        # ajouter parametre nom de l'Abandonneux, et si c'est moi, envoyer une action
        # quitter au serveur et faire destroy
        msg = param[0]
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
        self.batiments["maison"][idmaison] = Maison(self, idmaison, self.couleur, x, y, "maison")

    def construire_batiment(self, param):
        perso, sorte, pos = param

        if sorte == "siteconstruction":
            siteconstruction = self.batiments["siteconstruction"][pos[2]]
        else:
            id = get_prochain_id()
            # payer batiment
            vals = Joueur.valeurs
            for k, val in self.ressources.items():
                self.ressources[k] = val - vals[sorte][k]

            siteconstruction = SiteConstruction(self, id, pos[0], pos[1], sorte,
                                                Joueur.valeurs[sorte]["delai"])
            self.batiments["siteconstruction"][id] = siteconstruction

        for i in perso:
            self.persos["ouvrier"][i].construire_site_construction(siteconstruction)

    def installer_batiment(self, batiment):
        self.parent.installer_batiment(self.nom, batiment)

    # transmet à tous ses persos de jouer
    def jouer_prochain_coup(self):
        for j in self.persos.keys():
            for i in self.persos[j].keys():
                self.persos[j][i].jouer_prochain_coup()

    def creer_perso(self, param):
        sorteperso, batimentsource, idbatiment, pos = param

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

            self.persos[sorteperso][id] = Joueur.classespersos[sorteperso](self, id, batiment, self.couleur, x, y,
                                                                           sorteperso)

