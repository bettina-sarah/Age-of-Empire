## - Encoding: UTF-8 -*-

import math
import random
import time
from AoEw_divers import *
from helper import Helper
from AoEw_biomes import *
from AoEw_batiments import *
from AoEw_persos import *
from AoEw_joueurs import *


class Region():
    def __init__(self, parent, id, x, y, taillex, tailley, montype):
        self.parent = parent
        self.id = id
        self.debutx = x
        self.taillex = taillex
        self.debuty = y
        self.tailley = tailley
        self.montype = montype
        self.dicocases = {}


class Caseregion():
    def __init__(self, parent, id, x, y):
        self.parent = parent
        self.id = id
        self.montype = "plaine"
        self.ressources = {}
        self.x = x
        self.y = y


#######################  LE MODELE est la partie #######################
class Partie():
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
                                 "delai": 80}
               }

    def __init__(self, parent, mondict):
        self.parent = parent
        self.mort = []
        self.actions_a_faire = {}
        self.debut = int(time.time())
        self.aireX = 4000
        self.aireY = 4000
        # Decoupage de la surface
        self.taillecase = 20
        self.taillecarte = int(self.aireX / self.taillecase)
        self.cartecase = []
        self.make_carte_case()

        self.delaiprochaineaction = 20

        self.joueurs = {}
        self.classesbatiments = {"maison": Usineballiste,  # change back maison
                                 "caserne": Caserne,
                                 "abri": Abri,
                                 "usineballiste": Maison}
        self.classespersos = {"ouvrier": Ouvrier,
                              "soldat": Soldat,
                              "archer": Archer,
                              "chevalier": Chevalier,
                              "druide": Druide}
        self.ressourcemorte = []
        self.msggeneral = None
        self.msggeneraldelai = 30
        self.msggeneralcompteur = 0
        self.listebiotopes = []
        self.biotopes = {"daim": {},
                         "ours": {},
                         "arbre": {},
                         "roche": {},
                         "aureus": {},
                         "eau": {},
                         "marais": {},
                         "baie": {}}
        self.regions = {}

        self.regionstypes = [["arbre", 50, 20, 5, "forest green"],
                             ["eau", 10, 20, 12, "light blue"],
                             ["marais", 3, 8, 8, "DarkSeaGreen3"],
                             ["roche", 8, 3, 6, "gray60"],
                             ["aureus", 12, 3, 4, "gold2"], ]
        self.creer_regions()
        self.creer_biotopes()
        self.creer_population(mondict)

        self.taillecase = 20
        self.demicase = self.taillecase / 2
        self.taillecarte = int(self.aireX / self.taillecase)

    def trouver_valeurs(self):
        vals = Partie.valeurs
        return vals

    def montrer_msg_general(self, txt):
        self.msggeneral = txt

    def installer_batiment(self, nomjoueur, batiment):
        x1, y1, x2, y2 = self.parent.installer_batiment(nomjoueur, batiment)

        cartebatiment = self.get_carte_bbox(x1, y1, x2, y2)
        for i in cartebatiment:
            #pour contournement avec retour de ressource
            if(batiment.montype == "maison"):
                self.cartecase[i[1]][i[0]].montype = "batiment-m"
            else:
                self.cartecase[i[1]][i[0]].montype = "batiment"
        batiment.cartebatiment = cartebatiment

    def creer_biotopes(self):
        # creer des daims éparpillés
        n = 20
        while n:
            x = random.randrange(self.aireX)
            y = random.randrange(self.aireY)
            case = self.trouver_case(x, y)
            if case.montype == "plaine":
                id = get_prochain_id()
                if n % 2 == 0:
                    monanimal = Daim(self, id, x, y)
                    self.biotopes["daim"][id] = monanimal
                else:
                    monanimal = Ours(self, id, x, y)
                    self.biotopes["ours"][id] = monanimal

                    # peut l'optimiser en callent la var monanimal.type dans biotope[][] voir abi

                self.listebiotopes.append(monanimal)
                n -= 1
        self.creer_biotope("arbre", "arbre", Arbre)
        self.creer_biotope("roche", "roche", Roche)
        self.creer_biotope("eau", "eau", Eau)
        self.creer_biotope("marais", "marais", Marais)
        self.creer_biotope("aureus", "aureus", Aureus)

    def creer_biotope(self, region, ressource, typeclasse):  # creation des forets
        typeressource = typeclasse.typeressource

        for cleregion in self.regions[region].keys():
            listecases = self.regions[region][cleregion].dicocases
            # for listecase in self.regions[region]:
            # nressource = random.randrange(int(len(listecases) / 3)) + int((len(listecases) / 5))
            nressource = int((random.randrange(len(listecases)) / 3) + 1)
            print("RESSOURCES N", nressource)
            while nressource:
                cases = list(listecases.keys())
                pos = listecases[random.choice(cases)]
                # pos=random.choice(listecases)
                x = random.randrange(self.taillecase)
                y = random.randrange(self.taillecase)
                xa = (pos.x * self.taillecase) + x
                ya = (pos.y * self.taillecase) + y

                styleress = random.choice(typeressource)
                id = get_prochain_id()
                objet = typeclasse(self, id, styleress, xa, ya, ressource, cleregion, pos.id)
                pos.ressources[id] = objet
                self.biotopes[ressource][id] = (objet)
                self.listebiotopes.append(objet)
                nressource -= 1

    def creer_regions(self):
        for reg in self.regionstypes:
            nomregion = reg[0]
            nbrreg = reg[1]
            minreg = reg[2]
            rndreg = reg[3]
            coulreg = reg[4]
            self.regions[nomregion] = {}
            for i in range(nbrreg):
                listecasereg = []
                # trouve une case dans la carte
                x = random.randrange(self.taillecarte)
                y = random.randrange(self.taillecarte)
                # calcule la largeur (x) et hauteur(y) de la regtion
                taillex = random.randrange(reg[3]) + reg[2]
                tailley = random.randrange(reg[3]) + reg[2]
                # verifie que la region de deborde pas vers l'exterieur du jeu
                # (ex: si le centre de la region est case 1,1
                # et on la veut 10 case de large, cette region debuterait a la case -5, qui n'existe pas
                x0 = x - int(taillex / 2)
                if x0 < 0:
                    x0 = 0

                x1 = x + int(taillex / 2)
                if x1 > self.taillecarte - 1:
                    x1 = self.taillecarte - 1

                y0 = y - int(tailley / 2)
                if y0 < 0:
                    y0 = 0

                y1 = y + int(tailley / 2)
                if y1 > self.taillecarte - 1:
                    y1 = self.taillecarte - 1

                taillex = x1 - x0
                tailley = y1 - y0

                id = get_prochain_id()
                newregion = Region(self, id, x0, y0, taillex, tailley, nomregion)

                dicoreg = {}
                for i in range(tailley):
                    for j in range(taillex):
                        self.cartecase[y0 + i][x0 + j].parent = newregion
                        self.cartecase[y0 + i][x0 + j].montype = nomregion
                        # listereg.append(self.cartecase[y0+i][x0+j])
                        casereg = self.cartecase[y0 + i][x0 + j]
                        casereg.parent = newregion
                        dicoreg[casereg.id] = casereg

                newregion.dicocases = dicoreg
                self.regions[nomregion][id] = newregion

    def creer_population(self, mondict):
        couleurs = [["O", "orange"], ["R", "red"], ["B", "blue"], ["J", "yellow"], ["V", "lightgreen"]]
        quadrants = [[[0, 0], [int(self.aireX / 2), int(self.aireY / 2)]],
                     [[int(self.aireX / 2), 0], [self.aireX, int(self.aireY / 2)]],
                     [[0, int(self.aireY / 2)], [int(self.aireX / 2), self.aireY]],
                     [[int(self.aireX / 2), int(self.aireY / 2)], [self.aireX, self.aireY]],
                     [[int(self.aireX / 2), int(self.aireY / 2)], [self.aireX, self.aireY]]]
        nquad = 5
        bord = 50
        for i in mondict:
            id = get_prochain_id()
            coul = couleurs.pop()
            # placer les joueurs dans des quandrants differents
            choixquad = random.choice(range(nquad))
            nquad -= 1
            quad = quadrants.pop(choixquad)

            n = 1
            while n:
                x = random.randrange(quad[0][0] + bord, quad[1][0] - bord)
                y = random.randrange(quad[0][1] + bord, quad[1][1] - bord)
                case = self.trouver_case(x, y)
                if case.montype == "plaine":
                    self.joueurs[i] = Joueur(self, id, i, coul, x, y)
                    n = 0

    def deplacer(self):
        for i in self.joueurs:
            self.joueurs[i].deplacer()

    def jouer_prochain_coup(self, cadrecourant):
        self.ressourcemorte = []
        ##################################################################
        # faire nouvelle action recu du serveur si on est au bon cadrecourant
        # ATTENTION : NE PAS TOUCHER 
        if cadrecourant in self.actions_a_faire:
            for i in self.actions_a_faire[cadrecourant]:
                print("i dans jouer prochain coup", i)
                self.joueurs[i[0]].actions[i[1]](i[2])

        ##################################################################

        # demander aux objets de s'activer
        for i in self.biotopes["daim"].keys():
            self.biotopes["daim"][i].deplacer()

        for i in self.biotopes["ours"].keys():
            self.biotopes["ours"][i].deplacer()
        # Ajouter une liste des trucs a deplacer ? puis fair eune function? maybe ? :D

        for i in self.biotopes["eau"].keys():
            self.biotopes["eau"][i].jouer_prochain_coup()

        # demander aux objets de s'activer
        for i in self.joueurs.keys():
            self.joueurs[i].jouer_prochain_coup()

        if self.msggeneral:
            self.msggeneralcompteur += 1
            if self.msggeneralcompteur == self.msggeneraldelai:
                self.msggeneral = ""
                self.msggeneralcompteur = 0

        self.faire_action_partie()
        t = int(time.time())
        msg = "cadre: " + str(cadrecourant) + " - secs: " + str(t - self.debut)
        self.msggeneral = msg

    def faire_action_partie(self):
        if self.delaiprochaineaction == 0:
            self.produire_action()
            self.delaiprochaineaction = random.randrange(20, 30)
        else:
            self.delaiprochaineaction -= 1

    def produire_action(self):
        typeressource = Baie.typeressource
        n = 1
        while n:
            x = random.randrange(self.aireX)
            y = random.randrange(self.aireY)
            case = self.trouver_case(x, y)
            if case.montype == "plaine":
                id = get_prochain_id()
                img = random.choice(typeressource)
                baie = Baie(self, id, img, x, y, "baie")
                self.biotopes["baie"][id] = baie
                n -= 1
                self.parent.afficher_bio(baie)

    # VERIFIER CES FONCTIONS SUR LA CARTECASE

    def make_carte_case(self):
        # NOTE: cette carte est carre
        taille = self.taillecarte
        self.cartecase = []
        for i in range(taille):
            t1 = []
            for j in range(taille):
                id = get_prochain_id()
                t1.append(Caseregion(None, id, j, i))
            self.cartecase.append(t1)

    # def trouver_case(self, x, y):
    #
    #     if x < 0:
    #         x = 0
    #     if y < 0:
    #         y = 0
    #
    #     if x > (self.aireX - 1):
    #         x = self.aireX - 1
    #     if y > (self.aireY - 1):
    #         y = self.aireY - 1
    #
    #     cx = int(x / self.taillecase)
    #     cy = int(y / self.taillecase)
    #     # if cx != 0 and x % self.taillecase > 0:
    #     #     cx += 1
    #     #
    #     # if cy != 0 and y % self.taillecase > 0:
    #     #     cy += 1
    #
    #     # possible d'etre dans une case trop loin
    #     if cx == self.taillecarte:
    #         cx -= 1
    #     if cy == self.taillecarte:
    #         cy -= 1
    #     # print("--> carte",self.cartecase[cy][cx])
    #     return self.cartecase[cy][cx]  # [cx,cy]

    def trouver_case(self, x, y, dir="none"):
        offsetX = 0
        offsetY = 0
        # if dir == "GH":
        #     offsetX = -1
        #     offsetY = -1
        # elif dir == "DH":
        #     offsetX = 1
        #     offsetY = -1
        # elif dir == "GB":
        #     offsetX = -1
        #     offsetY = 1
        # elif dir == "DB":
        #     offsetX = 1
        #     offsetY = 1

        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x > (self.aireX - 1):
            x = self.aireX - 1
        if y > (self.aireY - 1):
            y = self.aireY - 1

        cx = int(x / self.taillecase)
        cy = int(y / self.taillecase)
        # if cx != 0 and x % self.taillecase > 0:
        #     cx += 1
        #
        # if cy != 0 and y % self.taillecase > 0:
        #     cy += 1

        # possible d'etre dans une case trop loin
        if cx == self.taillecarte:
            cx -= 1
        if cy == self.taillecarte:
            cy -= 1
        # print(self.cartecase[cy][cx])
        return self.cartecase[cy+offsetY][cx+offsetX]  # [cx,cy]

    def get_carte_bbox(self, x1, y1, x2, y2):  # case d'origine en cx et cy,  pour position pixels x, y
        # case d'origine en cx et cy,  pour position pixels x, y
        if x1 < 0:
            x1 = 1
        if y1 < 0:
            y1 = 1
        if x2 >= self.aireX:
            x2 = self.aireX - 1
        if y2 >= self.aireY:
            y2 = self.aireY - 1

        cx1 = int(x1 / self.taillecase)
        cy1 = int(y1 / self.taillecase)

        cx2 = int(x2 / self.taillecase)
        cy2 = int(y2 / self.taillecase)
        t1 = []
        for i in range(cy1, cy2):
            for j in range(cx1, cx2):
                case = self.cartecase[i][j]
                t1.append([j, i])
        return t1

    # CORRECTION REQUISE : PAS SUR QUE CETTE FONCITON SOIT ENCORE REQUISE
    # VA DEPENDRE DE L'IMPLANTATION S'IL Y A TROP D'OBJETS À VÉRIFIER
    def get_subcarte(self, x, y, d):

        cx = int(x / self.taillecase)
        cy = int(y / self.taillecase)
        # possible d'etre dans une case trop loin
        if cx == self.taillecase:
            cx -= 1
        if cy == self.taillecase:
            cy -= 1

        # le centre en pixels de la case d'origine
        pxcentrex = (cx * self.taillecase) + self.demicase
        pxcentrey = (cy * self.taillecase) + self.demicase

        # la case superieur gauche de la case d'origine
        casecoinx1 = cx - d
        casecoiny1 = cy - d
        # assure qu'on deborde pas
        if casecoinx1 < 0:
            casecoinx1 = 0
        if casecoiny1 < 0:
            casecoiny1 = 0
        # la case inferieur droite
        casecoinx2 = cx + d
        casecoiny2 = cy + d
        # assure qu'on deborde pas
        # if casecoinx2 >= self.taillecase:
        #     casecoinx2 = self.taillecase - 1
        # if casecoiny2 >= self.taillecase:
        #     casecoiny2 = self.taillecase - 1

        distmax = (d * self.taillecase) + self.demicase

        t1 = []
        for i in range(casecoiny1, casecoiny2):
            for j in range(casecoinx1, casecoinx2):
                case = self.cartecase[i][j]
                pxcentrecasex = (j * self.taillecase) + self.demicase
                pxcentrecasey = (i * self.taillecase) + self.demicase
                distcase = Helper.calcDistance(pxcentrex, pxcentrey, pxcentrecasex, pxcentrecasey)
                if distcase <= distmax:
                    t1.append(case)
        return t1

    def get_carte_contournement(self, x, y, dx,dy):
        cx = int(x / self.taillecase)
        cy = int(y / self.taillecase)
        # possible d'etre dans une case trop loin
        if cx == self.taillecase:
            cx -= 1
        if cy == self.taillecase:
            cy -= 1

        # le centre en pixels de la case d'origine
        pxcentrex = (cx * self.taillecase) + self.demicase
        pxcentrey = (cy * self.taillecase) + self.demicase

        # la case superieur gauche de la case d'origine
        casecoinx1 = cx - dx
        casecoiny1 = cy - dy
        # assure qu'on deborde pas
        if casecoinx1 < 0:
            casecoinx1 = 0
        if casecoiny1 < 0:
            casecoiny1 = 0
        # la case inferieur droite
        casecoinx2 = cx + dx
        casecoiny2 = cy + dy


        distmax = (10 * self.taillecase) + self.demicase

        t1 = []
        for i in range(casecoiny1, casecoiny2):
            for j in range(casecoinx1, casecoinx2):
                case = self.cartecase[i][j]
                pxcentrecasex = (j * self.taillecase) + self.demicase
                pxcentrecasey = (i * self.taillecase) + self.demicase
                distcase = Helper.calcDistance(pxcentrex, pxcentrey, pxcentrecasex, pxcentrecasey)
                if distcase <= distmax:
                    t1.append(case)
        return t1
        pass


    def eliminer_ressource(self, type, ress):
        if ress.idregion:
            # self.regions[ress.montype][ress.idregion].listecases.pop(ress.id)
            cr = self.regions[ress.montype][ress.idregion].dicocases[ress.idcaseregion]
            if ress.id in cr.ressources.keys():
                cr.ressources.pop(ress.id)

        if ress.id in self.biotopes[type]:
            self.biotopes[type].pop(ress.id)
        if ress not in self.ressourcemorte:
            self.ressourcemorte.append(ress)

    #############################################################################
    # ATTENTION : NE PAS TOUCHER
    def ajouter_actions_a_faire(self, iteration, actionsrecues):
        for i in actionsrecues:
            iteration_cle = i[0]
            if (iteration - 1) > int(iteration_cle):
                print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            if i[1]:
                # action = json.loads(i[1])
                action = i[1]
            else:
                action = None
            if action:
                if iteration_cle not in self.actions_a_faire.keys():
                    self.actions_a_faire[iteration_cle] = action
                else:
                    for j in action:
                        self.actions_a_faire[iteration_cle].append(j)

    ##############################################################################

    ## Ajout Abi

    def delete_batim_joueurs(self, id_batim, joueur):
        print("JOEEUR LOCAL")
        print(self.parent.nom_joueur_local)
        print("joueur qui a etet delete")
        print(joueur)
        joueur = self.joueurs.get(joueur)
        print(joueur.batiments)

        for key, value_list in joueur.batiments.items():
            if id_batim in value_list:
                value_list.remove(id_batim)
        # joueur.batiments.pop(id_batim)

        self.eliminer_joueur()

    def eliminer_joueur(self):

        localaa = self.joueurs.get(self.parent.nom_joueur_local)

        for key in self.joueurs.keys():
            joueur = self.joueurs.get(key)
            batiement = joueur.batiments.values
            if joueur.batiments["maison"] == {} and joueur.batiments["abri"] == {} and joueur.batiments[
                "caserne"] == {} and joueur.batiments["usineballiste"] == {}:
                if joueur.id not in self.mort:
                    self.mort.append(joueur.id)
                    if joueur.id == localaa.id:
                        self.parent.tuer_joueur()
        self.fin_jeu()

    def fin_jeu(self):
        temp = []
        for key in self.joueurs.keys():
            j = self.joueurs.get(key)
            if j.id not in self.mort:
                temp.append(j.nom)

        if len(temp) == 1:
            self.parent.afficher_fin(temp[0])

    def retirer_batiment_minimap(self, id):
        self.parent.retirer_batiment_minimap(id)

    def reset_case_batiment(self, cartebatiment):
        print("click")
        for i in cartebatiment:
            self.cartecase[i[1]][i[0]].montype = "plaine"
        pass
