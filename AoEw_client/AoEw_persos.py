import random
import math
from helper import Helper
from AoEw_divers import *


class Fleche():
    def __init__(self, parent, id, proie):
        self.parent = parent
        self.id = id
        self.vitesse = 18
        self.taille = 20

        self.force = 25  ##A REMMETTRE A 10

        self.proie = proie
        self.proiex = self.proie.x
        self.proiey = self.proie.y
        self.x = self.parent.x
        self.y = self.parent.y
        self.ang = Helper.calcAngle(self.x, self.y, self.proiex, self.proiey)
        angquad = math.degrees(self.ang)
        dir = "DB"
        if 0 <= angquad <= 89:
            dir = "DB"
        elif -90 <= angquad <= -1:
            dir = "DH"
        if 90 <= angquad <= 179:
            dir = "GB"
        elif -180 <= angquad <= -91:
            dir = "GH"
        self.image = "javelot" + dir

    def bouger(self):
        if not self.proie:
            self.parent.fleches = []
        self.x, self.y, = Helper.getAngledPoint(self.ang, self.vitesse, self.x, self.y)
        dist = Helper.calcDistance(self.x, self.y, self.proie.x, self.proie.y)
        if dist <= self.taille:
            rep = self.proie.recevoir_coup(self.force)
            self.parent.fleches.remove(self)
            if rep == 1:
                self.parent.fleches.clear()
                try:
                    self.parent.parent.parent.trouver_case(self.parent.cibleennemi.x, self.parent.cibleennemi.y).persos.pop(self.parent.cibleennemi.id)
                except:
                    pass
                self.parent.cibleennemi = None;
                self.parent.actioncourante = "verifierchampvision"

            # return self





class Boulet():
    def __init__(self, parent, id, proie):
        self.parent = parent
        self.id = id
        self.vitesse = 18
        self.taille = 20

        self.force = 25  ##A REMMETTRE A 10

        self.proie = proie
        self.proiex = self.proie.x
        self.proiey = self.proie.y
        self.x = self.parent.x
        self.y = self.parent.y
        self.ang = Helper.calcAngle(self.x, self.y, self.proiex, self.proiey)
        angquad = math.degrees(self.ang)
        dir = "DB"
        if 0 <= angquad <= 89:
            dir = "DB"
        elif -90 <= angquad <= -1:
            dir = "DH"
        if 90 <= angquad <= 179:
            dir = "GB"
        elif -180 <= angquad <= -91:
            dir = "GH"
        self.image = "boulet" + dir

    def bouger(self):
        if not self.proie:
            self.parent.boulets = []
        self.x, self.y, = Helper.getAngledPoint(self.ang, self.vitesse, self.x, self.y)
        dist = Helper.calcDistance(self.x, self.y, self.proie.x, self.proie.y)
        if dist <= self.taille:
            rep = self.proie.recevoir_coup(self.force)
            self.parent.boulets.remove(self)
            if rep == 1:
                self.parent.boulets.clear()
                try:
                    self.parent.parent.parent.trouver_case(self.parent.cibleennemi.x, self.parent.cibleennemi.y).persos.pop(self.parent.cibleennemi.id)
                except:
                    pass
                self.parent.cibleennemi = None;
                self.parent.actioncourante = "verifierchampvision"

            # return self



class Javelot():
    def __init__(self, parent, id, proie):
        self.parent = parent
        self.id = id
        self.vitesse = 18
        self.distance = 150
        self.taille = 20
        self.demitaille = 10
        self.proie = proie
        self.proiex = self.proie.x
        self.proiey = self.proie.y
        self.dommage = 2
        self.x = self.parent.x
        self.y = self.parent.y
        self.ang = Helper.calcAngle(self.x, self.y, self.proiex, self.proiey)
        angquad = math.degrees(self.ang)
        dir = "DB"
        if 0 <= angquad <= 89:
            dir = "DB"
        elif -90 <= angquad <= -1:
            dir = "DH"
        if 90 <= angquad <= 179:
            dir = "GB"
        elif -180 <= angquad <= -91:
            dir = "GH"
        self.image = "javelot" + dir

    def bouger(self):
        self.x, self.y, = Helper.getAngledPoint(self.ang, self.vitesse, self.x, self.y)
        dist = Helper.calcDistance(self.x, self.y, self.proie.x, self.proie.y)
        if dist <= self.demitaille:
            # tue daim
            self.parent.javelots.remove(self)
            if self.proie.recevoir_coup(self.dommage, self.parent) == 1:
                self.parent.actioncourante = "ciblerressource"


        else:
            dist = Helper.calcDistance(self.x, self.y, self.proiex, self.proiey)
            if dist < self.vitesse:
                self.proie.recevoir_coup(self.dommage, self.parent)
                self.parent.javelots.remove(self)
                self.parent.actioncourante = "ciblerproie"


class Perso():
    def __init__(self, parent, id, batiment, couleur, x, y, montype):
        self.parent = parent
        self.id = id
        self.actioncourante = None
        self.batimentmere = batiment
        self.dir = "D"
        self.image = couleur[0] + "_" + montype + self.dir
        self.x = x
        self.y = y
        self.case = self.parent.parent.trouver_case(self.x, self.y)
        self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self
        self.montype = montype
        self.cible = None
        self.position_visee = None
        self.cibleennemi = None
        self.manaMax = 100
        self.mana = 100
        self.force = 25
        self.champvision = 100
        self.vitesse = 30
        self.angle = None
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": None,  # caller la bonne fctn attaquer
                                 "ciblerennemi": None,
                                 "contourne": self.contourne,
                                 "soignercible":None}

        # contournement
        self.action_precedente = None
        self.cible_contournement = None
        self.cibles_contournement_precedentes = []
        self.contournements = 0
        self.contournement_range = 5
        self.case_coutournement = None


    def attaquer(self, ennemi):
        self.cibleennemi = ennemi[0]
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        pos_cible = x, y
        self.cibler(ennemi)
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.vitesse:
            self.actioncourante = "attaquerennemi"
        else:
            self.actioncourante = "ciblerennemi"

    # perso
    def attaquer_ennemi(self):
        rep = self.cibleennemi.recevoir_coup(self.force, self)
        if rep == 1:
            self.cibleennemi = None
            self.cible = None

            self.actioncourante = "deplacer"

    def recevoir_coup(self, force):
        self.mana -= force
        print("----------------------------TU MA FRAPPE!!!!!!")
        if self.mana < 1:
            self.parent.annoncer_mort(self)
            return 1

    def recevoir_soin(self, soin):
        print(" avant",self.mana)
        print("soin rececois",self.force)

        if self.mana + soin >= self.manaMax:
            self.mana = self.manaMax
            print("soin recu", self.mana)
            return 1
        else:
            self.mana += soin
            print("soin recu", self.mana)
            return 0



    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def deplacer(self, pos):
        self.position_visee = pos
        self.actioncourante = "bouger"

    def bouger(self):
        if self.position_visee:
            # le if sert à savoir si on doit repositionner notre visee pour un objet
            # dynamique comme le daim
            x = self.position_visee[0]
            y = self.position_visee[1]
            ang = Helper.calcAngle(self.x, self.y, x, y)
            x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
            ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
            # print("avant : ", self.x,"/", self.y )
            # self.x, self.y = self.test_etat_du_sol(x1, y1)
            case_mur = self.test_etat_du_sol(x1, y1)
            self.update_cases(x1,y1)
            if case_mur:
                self.nouveau_contournement(case_mur)
                return "contourne"

            ######## FIN DE TEST POUR SURFACE MARCHEE
            # si tout ba bien on continue avec la nouvelle valeur
            # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
            dist = Helper.calcDistance(self.x, self.y, x, y)

            if dist <= self.vitesse:
                if self.actioncourante == "bouger":
                    if not self.montype == "ouvrier":
                        self.actioncourante = "verifierchampvision"
                    else :
                        self.actioncourante = None
                self.contournements = 0
                self.cibles_contournement_precedentes = []
                self.cible_contournement = None
                return "rendu"
            else:
                return dist


    def nouveau_contournement(self, case):
        self.action_precedente = self.actioncourante
        self.actioncourante = "contourne"
        self.contournements += 1
        self.case_coutournement = case
        # print("contournement #:", self.contournements)

    def bouger_vers_ennemi(self):
        if self.cibleennemi:
            # le if sert à savoir si on doit repositionner notre visee pour un objet
            # dynamique comme le daim
            x = self.cibleennemi.x
            y = self.cibleennemi.y
            ang = Helper.calcAngle(self.x, self.y, x, y)
            x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
            ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
            self.get_directon_vers_position_visee()
            # print("avant : ", self.x,"/", self.y )
            # self.x, self.y = self.test_etat_du_sol(x1, y1)
            case_mur = self.test_etat_du_sol(x1, y1)
            self.update_cases(x1, y1)
            if case_mur:
                self.nouveau_contournement(case_mur)
                return "contourne"
            ######## FIN DE TEST POUR SURFACE MARCHEE
            # si tout ba bien on continue avec la nouvelle valeur
            # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
            dist = Helper.calcDistance(self.x, self.y, x, y)

            if dist <= self.distancefeumax:
                if self.actioncourante == "bougerversennemi":
                    self.actioncourante = "ciblerennemi"
                return "rendu"
            else:
                return dist

    def update_cases(self, x1, y1):
        self.parent.parent.trouver_case(self.x, self.y).persos.pop(self.id)
        self.x, self.y = x1, y1
        self.case = self.parent.parent.trouver_case(self.x, self.y)
        self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self

    def get_directon_vers_position_visee(self):
        if self.position_visee:
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"

            if self.y < self.position_visee[1]:
                self.dir += "B"
            else:
                self.dir += "H"

    def get_directon_contournement(self, x1, y1):
        # suis-je plus près de ma cible sur l'axe des x ou y
        cases = self.parent.parent.get_carte_contournement(x1, y1, 1, 4)
        # retourn vrai pour un mouvement vertical
        if cases[3].montype == "batiment" and cases[5].montype == "batiment":
            return False
        if cases[4].montype == "batiment" and cases[6].montype == "batiment":
            return False
        if cases[-3].montype == "batiment" and cases[-5].montype == "batiment":
            return False
        if cases[-4].montype == "batiment" and cases[-6].montype == "batiment":
            return False
        else:
            return True

            # print("bad vertical")

        # cases = self.parent.parent.get_carte_contournement(x1, y1, 4, 1)
        # if cases[0].montype == "batiment" or cases[-1].montype == "batiment":
        #     print("bad vertical")

        # return  self.get_directon_contournement()

    def get_directon_vers_position_visee(self):
        if self.position_visee:
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"

            if self.y < self.position_visee[1]:
                self.dir += "B"
            else:
                self.dir += "H"

    def cibler(self, obj):
        self.cible = obj
        if obj:
            self.position_visee = [self.cible.x, self.cible.y]
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
            self.image = self.image[:-1] + self.dir
        else:
            self.position_visee = None




    def test_etat_du_sol(self, x1, y1):

        casex = x1 / self.parent.parent.taillecase
        if casex != int(casex):
            casex = int(casex) + 1
        casey = y1 / self.parent.parent.taillecase
        if casey != int(casey):
            casey = int(casey) + 1

        case = self.parent.parent.trouver_case(x1, y1, self.dir)

        # affichage --------------------------------------------------------------------------------------------------
        # taille = self.parent.parent.taillecase

        # xa, ya, xb, yb = case.x * taille, case.y * taille, case.x * taille + taille, case.y * taille + taille
        # self.parent.parent.parent.vue.canevas.create_rectangle(xa, ya, xb, yb, fill="magenta", tags=("statique",))
        # affichage --------------------------------------------------------------------------------------------------

        # si je un ouvrier déplace des ressources, retourne la case seulement si la case est batiment (ignore batiment-m)

        case_avec_collision = self.parent.parent.get_case_batiment()


        if self.actioncourante == "bougerversennemi" or self.actioncourante == "ciblerennemi" or self.actioncourante == "attaquerennemi":
            print(self.actioncourante)
            if case.batiment and self.cibleennemi:
                print("meurt batiment?")
                print(case.batiment.id)
                print(self.cibleennemi.id)
                if self.cibleennemi.id == case.batiment.id:
                    print("pas collision")
                    return None

        if self.actioncourante == "retourbatimentmere" or self.actioncourante == "ciblerressource":
            if case.montype != "batiment-maison" and case.montype in case_avec_collision:
                return case
            else:
                return None

        if self.actioncourante == "ciblersiteconstruction":
            if case.montype != "batiment-mur" and case.montype in case_avec_collision:
                return case
            else:
                return None

        # retourne la case si c'est un batiment ou batiment-m
        if case.montype in case_avec_collision:
            return case

        # retourne rien si la case n'est pas un batiment




    def contourne(self):
        # trouve les coins non-visités
        if not self.cible_contournement:
            self.get_cible_contournement()

        #déplace vers la cible de contournement
        # if not self.cible_contournement:
        #     return
        print("cible: ",self.cible_contournement)
        if not self.cible_contournement:
            print("contoure")
            self.cible_contournement = None
            self.actioncourante = self.action_precedente
            return

        x,y = self.cible_contournement[1]
        ang = Helper.calcAngle(self.x, self.y, x, y)

        self.parent.parent.trouver_case(self.x, self.y).persos.pop(self.id)
        # print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
        self.x, self.y = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
        dist = Helper.calcDistance(self.x, self.y, x, y)
        self.case = self.parent.parent.trouver_case(self.x, self.y)
        self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self
        # print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)


        if dist <= self.vitesse:
            self.cible_contournement = None
            self.actioncourante = self.action_precedente

    def get_cible_contournement(self):

        cible_possibles = []
        for coin in self.case_coutournement.batiment.get_coins():
            if coin not in self.cibles_contournement_precedentes:
                cible_possibles.append(coin)

        # trouve le coin le plus proche
        distance_coin = []
        for coin in cible_possibles:
            distance = ((coin[0] - self.x) ** 2 + (coin[1] - self.y) ** 2) ** 0.5
            distance_coin.append((distance, coin))

        # trouve le coin avec la plus petite distance avec le perso
        print(cible_possibles)
        print(distance_coin)
        print(len(distance_coin))

        if len(distance_coin) > 0:
            self.cible_contournement = None
            self.actioncourante = self.action_precedente

            smallest_dist = distance_coin[0]
            for d in distance_coin:
                if smallest_dist[0] > d[0]:
                    smallest_dist = d

            # ce coin devient la cible de contournement, on l'ajoute au cible précédente pour éviter un repeat
            self.cible_contournement = smallest_dist
            self.cibles_contournement_precedentes.append(smallest_dist[1])


class Soldat(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 25
        self.distancefeumax = 50
        self.delai_verifier_champ = 30
        self.vision_cases = 10
        self.delaifeu = 20
        self.delaifeumax = 20
        self.champvision = 100
        self.vitesse = 5
        self.mana = 100
        self.cibleennemi = None
        self.position_visee = None
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi": self.bouger_vers_ennemi,
                                 "verifierchampvision": self.verifier
                                 }
        self.actioncourante = "verifierchampvision"

    # def bouger(self):
    #     if self.position_visee:
    #         # le if sert à savoir si on doit repositionner notre visee pour un objet
    #         # dynamique comme le daim
    #         x = self.position_visee[0]
    #         y = self.position_visee[1]
    #         ang = Helper.calcAngle(self.x, self.y, x, y)
    #         x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
    #         ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
    #         self.get_directon_vers_position_visee()
    #         # print("avant : ", self.x,"/", self.y )
    #         # self.x, self.y = self.test_etat_du_sol(x1, y1)
    #         if self.test_etat_du_sol(x1, y1):
    #             self.action_precedente = self.actioncourante
    #             self.actioncourante = "contourne"
    #             return "contourne"
    #         self.parent.parent.trouver_case(self.x, self.y).persos.pop(self.id)
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         self.x, self.y = x1, y1
    #         self.case = self.parent.parent.trouver_case(self.x, self.y)
    #         self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         ######## FIN DE TEST POUR SURFACE MARCHEE
    #         # si tout ba bien on continue avec la nouvelle valeur
    #         # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
    #         dist = Helper.calcDistance(self.x, self.y, x, y)
    #
    #         if dist <= self.vitesse:
    #             if self.actioncourante == "bouger":
    #                 self.actioncourante = "verifierchampvision"
    #             return "rendu"
    #         else:
    #             return dist

    def cibler(self):
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"

        self.image = self.image[:-1] + self.dir
        self.actioncourante = "attaquerennemi"

    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.position_visee = [x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)
        print("DISTANCE CALCULEE", dist)

        if dist <= self.distancefeumax:  # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "attaquerennemi"
            print("self.actioncourante = attaquerennemi")
        else:  # si la distance est trop grande ca fait juste le cibler et ca arrete la
            self.actioncourante = "bougerversennemi"
            print("self.actioncourante = ciblerennemi")

    def attaquerennemi(self):
        if self.cibleennemi:
            self.delaifeu = self.delaifeu - 1
            print("KAWABUNGA BABY")
            print(" DELAI FEU : ", self.delaifeu)
            if not self.image[-1] == "A":
                self.image = self.image + "A"
            if self.delaifeu == 0:
                self.image = self.image[:-1]
                rep = self.cibleennemi.recevoir_coup(self.force)
                self.delaifeu = self.delaifeumax
                if rep:
                    self.actioncourante = "verifierchampvision"
                    try:
                        self.parent.parent.trouver_case(self.cibleennemi.x, self.cibleennemi.y).persos.pop(self.cibleennemi.id)
                    except:
                        pass

                # self.cibleennemi.recevoir_coup(self.force)
                # self.fleches.remove(rep)

    def verifier(self):
        self.verifier_champ_vision(self.x, self.y, self.vision_cases)

    def verifier_champ_vision(self, x, y, radius):
        self.delai_verifier_champ -= 1
        if self.delai_verifier_champ == 0:
            cases = self.parent.parent.get_subcarte(x, y, radius)
            print("CASES", cases)
            for i in cases:  # chaque case
                cles = i.persos.values()  # 'objet'
                for j in cles:  # pour chaque objet
                    print(j.parent.nom)
                    if j.parent.nom != self.parent.nom:
                        print("============== DETECTION ENNEMI============")
                        self.attaquer(j)
            self.delai_verifier_champ = 30


class Archer(Perso):
    def __init__(self, parent, id, couleur, x, y, montype,  maison=None):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)

        self.dir = "D"
        # self.cible = None
        # self.angle = None
        self.distancefeumax = 200
        self.delai_verifier_champ = 30
        self.vision_cases = 10
        self.distancefeu = 200
        self.delaifeu = 25
        self.delaifeumax = 25
        self.champvision = 300
        self.vitesse = 5
        self.mana = 80
        self.fleches = []
        self.cibleennemi = None
        self.position_visee = None
        # self.nomimg="ballista"
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi": self.bouger_vers_ennemi,
                                 "verifierchampvision": self.verifier
                                 }

        self.actioncourante = "verifierchampvision"

    # def bouger(self):
    #     if self.position_visee:
    #         # le if sert à savoir si on doit repositionner notre visee pour un objet
    #         # dynamique comme le daim
    #         x = self.position_visee[0]
    #         y = self.position_visee[1]
    #         ang = Helper.calcAngle(self.x, self.y, x, y)
    #         x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
    #         ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
    #         self.get_directon_vers_position_visee()
    #         # print("avant : ", self.x,"/", self.y )
    #         # self.x, self.y = self.test_etat_du_sol(x1, y1)
    #         if self.test_etat_du_sol(x1, y1):
    #             self.action_precedente = self.actioncourante
    #             self.actioncourante = "contourne"
    #             return "contourne"
    #         self.parent.parent.trouver_case(self.x, self.y).persos.pop(self.id)
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         self.x, self.y = x1, y1
    #         self.case = self.parent.parent.trouver_case(self.x, self.y)
    #         self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         ######## FIN DE TEST POUR SURFACE MARCHEE
    #         # si tout ba bien on continue avec la nouvelle valeur
    #         # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
    #         dist = Helper.calcDistance(self.x, self.y, x, y)
    #
    #         if dist <= self.vitesse:
    #             if self.actioncourante == "bouger":
    #                 self.actioncourante = "verifierchampvision"
    #             return "rendu"
    #         else:
    #             return dist

    def cibler(self):
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"
        # if self.y < self.position_visee[1]:
        #     self.dir = self.dir + "B"
        # else:
        #     self.dir = self.dir + "H"

        self.image = self.image[:-1] + self.dir
        self.actioncourante = "attaquerennemi"

    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.position_visee = [x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.distancefeu:  # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "ciblerennemi"
        else:  # si la distance est trop grande ca fait juste le cibler et ca arrete la
            self.actioncourante = "bougerversennemi"

    def attaquerennemi(self):
        if self.cibleennemi:
            self.delaifeu = self.delaifeu - 1
            if self.delaifeu == 0:
                id = get_prochain_id()
                fleche = Fleche(self, id, self.cibleennemi)  # avant cetait ciblennemi
                self.fleches.append(fleche)
                self.delaifeu = self.delaifeumax
            if len(self.fleches) > 0:
                for i in self.fleches:
                    rep = i.bouger()
                # if rep:
                # self.cibleennemi.recevoir_coup(self.force)
                # self.fleches.remove(rep)

    def verifier(self):
        self.verifier_champ_vision(self.x, self.y, self.vision_cases)
    def verifier_champ_vision(self, x, y, radius):
        self.delai_verifier_champ -= 1
        if self.delai_verifier_champ == 0:
            cases = self.parent.parent.get_subcarte(x, y, radius)
            print("CASES", cases)
            for i in cases: # chaque case
                cles = i.persos.values() #'objet'
                for j in cles: # pour chaque objet
                    print(j.parent.nom)
                    if j.parent.nom != self.parent.nom:
                        print("============== DETECTION ENNEMI============")
                        self.attaquer(j)
            self.delai_verifier_champ = 30


class CavalierArcher(Archer):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Archer.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.distancefeumax = 250
        self.delai_verifier_champ = 30
        self.distancefeu = 250
        self.champvision = 350
        self.vitesse = 35
        self.mana = 120



class Chevalier(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 20
        self.distancefeumax = 50
        self.delaifeu = 20
        self.delaifeumax = 20
        self.delai_verifier_champ = 30
        self.vision_cases = 10
        self.champvision = 150
        self.vitesse = 10
        self.mana = 150
        self.cibleennemi = None
        self.position_visee = None
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi": self.bouger_vers_ennemi,
                                 "verifierchampvision": self.verifier
                                 }
        self.actioncourante = "verifierchampvision"

    # def bouger(self):
    #     if self.position_visee:
    #         # le if sert à savoir si on doit repositionner notre visee pour un objet
    #         # dynamique comme le daim
    #         x = self.position_visee[0]
    #         y = self.position_visee[1]
    #         ang = Helper.calcAngle(self.x, self.y, x, y)
    #         x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
    #         ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
    #         self.get_directon_vers_position_visee()
    #         # print("avant : ", self.x,"/", self.y )
    #         # self.x, self.y = self.test_etat_du_sol(x1, y1)
    #         if self.test_etat_du_sol(x1, y1):
    #             self.action_precedente = self.actioncourante
    #             self.actioncourante = "contourne"
    #             return "contourne"
    #         self.parent.parent.trouver_case(self.x, self.y).persos.pop(self.id)
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         self.x, self.y = x1, y1
    #         self.case = self.parent.parent.trouver_case(self.x, self.y)
    #         self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         ######## FIN DE TEST POUR SURFACE MARCHEE
    #         # si tout ba bien on continue avec la nouvelle valeur
    #         # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
    #         dist = Helper.calcDistance(self.x, self.y, x, y)
    #
    #         if dist <= self.vitesse:
    #             if self.actioncourante == "bouger":
    #                 self.actioncourante = "verifierchampvision"
    #             return "rendu"
    #         else:
    #             return dist

    def cibler(self):
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"

        self.image = self.image[:-1] + self.dir
        self.actioncourante = "attaquerennemi"

    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.position_visee = [x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)
        print("DISTANCE CALCULEE", dist)

        if dist <= self.distancefeumax:  # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "attaquerennemi"
            print("self.actioncourante = attaquerennemi")
        else:  # si la distance est trop grande ca fait juste le cibler et ca arrete la
            self.actioncourante = "bougerversennemi"
            print("self.actioncourante = ciblerennemi")

    def attaquerennemi(self):
        if self.cibleennemi:
            self.delaifeu = self.delaifeu - 1
            print("KAWABUNGA BABY")
            print(" DELAI FEU : ", self.delaifeu)

            if self.delaifeu == 0:
                rep = self.cibleennemi.recevoir_coup(self.force)
                self.delaifeu = self.delaifeumax
                if rep:
                    self.actioncourante = "verifierchampvision"
                    try:
                        self.parent.parent.trouver_case(self.cibleennemi.x, self.cibleennemi.y).persos.pop(self.cibleennemi.id)
                    except:
                        pass
                # self.cibleennemi.recevoir_coup(self.force)
                # self.fleches.remove(rep)

    def verifier(self):
        self.verifier_champ_vision(self.x, self.y, self.vision_cases)

    def verifier_champ_vision(self, x, y, radius):
        self.delai_verifier_champ -= 1
        if self.delai_verifier_champ == 0:
            cases = self.parent.parent.get_subcarte(x, y, radius)
            print("CASES", cases)
            for i in cases:  # chaque case
                cles = i.persos.values()  # 'objet'
                for j in cles:  # pour chaque objet
                    print(j.parent.nom)
                    if j.parent.nom != self.parent.nom:
                        print("============== DETECTION ENNEMI============")
                        self.attaquer(j)
            self.delai_verifier_champ = 30


class Druide(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 20
        self.distancefeumax = 50
        self.soin_mana = 1
        self.distancefeumax = 10
        self.delaifeu = 20
        self.delaifeumax = 20

        self.delaisoin = 5
        self.delaisoinmax = 5
        self.cibleennemi = None
        self.cible_soin = None
        self.position_visee = None
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi": self.bouger_vers_ennemi,
                                 "soignercible": self.soignercible
                                 }

    def cibler(self):
        ###?????????????????????????????????????
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"

        self.image = self.image[:-1] + self.dir
        self.actioncourante = "soignercible"

    def soigner(self, blesse):
        print("dans soigne")
        self.cible_soin = blesse
        self.cibleennemi=blesse
        x = self.cible_soin.x
        y = self.cible_soin.y
        self.position_visee = [x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)
        print("DISTANCE CALCULEE", dist)

        if dist <= self.distancefeumax:  # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "soignercible"
            print(self.actioncourante)
        else:  # si la distance est trop grande ca fait juste le cibler et ca arrete la
            self.actioncourante = "bougerversennemi"
            print(self.actioncourante)

    def attaquerennemi(self):
        if self.cibleennemi:
            self.delaifeu = self.delaifeu - 1
            if self.delaifeu == 0:
                rep = self.cibleennemi.recevoir_coup(self.force)
                self.delaifeu = self.delaifeumax
                if rep:
                    self.actioncourante = None
                # self.cibleennemi.recevoir_coup(self.force)
                # self.fleches.remove(rep)

    def soignercible(self):
        if self.cible_soin:
            self.delaisoin = self.delaisoin - 1
            print("dans soincible")
            print("delais soin:", self.delaisoin)
            if self.delaisoin == 0:
                rep = self.cible_soin.recevoir_soin(self.soin_mana)
                self.delaisoin = self.delaisoinmax
                if rep:
                    self.actioncourante = None


class DruideOurs(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 30
        self.soin_mana = 4
        self.distancefeumax = 10
        self.delaifeu = 20
        self.delaifeumax = 20
        self.delaisoin = 5
        self.delaisoinmax = 5
        self.delai_verifier_champ = 30
        self.vision_cases = 10
        self.cibleennemi = None
        self.cible_soin = None
        self.position_visee = None
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi": self.bouger_vers_ennemi,

                                 "soignercible": self.soignercible,

                                 "verifierchampvision": self.verifier
                                 }
        self.actioncourante = "verifierchampvision"

    # def bouger(self):
    #     if self.position_visee:
    #         # le if sert à savoir si on doit repositionner notre visee pour un objet
    #         # dynamique comme le daim
    #         x = self.position_visee[0]
    #         y = self.position_visee[1]
    #         ang = Helper.calcAngle(self.x, self.y, x, y)
    #         x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
    #         ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
    #         self.get_directon_vers_position_visee()
    #         # print("avant : ", self.x,"/", self.y )
    #         # self.x, self.y = self.test_etat_du_sol(x1, y1)
    #         if self.test_etat_du_sol(x1, y1):
    #             self.action_precedente = self.actioncourante
    #             self.actioncourante = "contourne"
    #             return "contourne"
    #         self.parent.parent.trouver_case(self.x, self.y).persos.pop(self.id)
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         self.x, self.y = x1, y1
    #         self.case = self.parent.parent.trouver_case(self.x, self.y)
    #         self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         ######## FIN DE TEST POUR SURFACE MARCHEE
    #         # si tout ba bien on continue avec la nouvelle valeur
    #         # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
    #         dist = Helper.calcDistance(self.x, self.y, x, y)
    #
    #         if dist <= self.vitesse:
    #             if self.actioncourante == "bouger":
    #                 self.actioncourante = "verifierchampvision"
    #             return "rendu"
    #         else:
    #             return dist

    def cibler(self):
        ###?????????????????????????????????????
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"

        self.image = self.image[:-1] + self.dir
        self.actioncourante = "soignercible"

    def soigner(self, blesse):
        print("dans soigne")
        self.cible_soin = blesse
        self.cibleennemi=blesse
        x = self.cible_soin.x
        y = self.cible_soin.y
        self.position_visee = [x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)
        print("DISTANCE CALCULEE", dist)

        if dist <= self.distancefeumax:  # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "soignercible"
            print(self.actioncourante)
        else:  # si la distance est trop grande ca fait juste le cibler et ca arrete la
            self.actioncourante = "bougerversennemi"
            print(self.actioncourante)

    def attaquerennemi(self):
        if self.cibleennemi:
            self.delaifeu = self.delaifeu - 1
            if self.delaifeu == 0:
                rep = self.cibleennemi.recevoir_coup(self.force)
                self.delaifeu = self.delaifeumax
                if rep:
                    self.actioncourante = "verifierchampvision"
                    try:
                        self.parent.parent.trouver_case(self.cibleennemi.x, self.cibleennemi.y).persos.pop(self.cibleennemi.id)
                    except:
                        pass
                # self.cibleennemi.recevoir_coup(self.force)
                # self.fleches.remove(rep)

    def soignercible(self):
        if self.cible_soin:
            self.delaisoin = self.delaisoin - 1
            print("dans soincible")
            print("delais soin:", self.delaisoin)
            if self.delaisoin == 0:
                rep = self.cible_soin.recevoir_soin(self.soin_mana)
                self.delaisoin = self.delaisoinmax
                if rep:
                    self.actioncourante = None


    def verifier(self):
        self.verifier_champ_vision(self.x, self.y, self.vision_cases)

    def verifier_champ_vision(self, x, y, radius):
        self.delai_verifier_champ -= 1
        if self.delai_verifier_champ == 0:
            cases = self.parent.parent.get_subcarte(x, y, radius)
            print("CASES", cases)
            for i in cases:  # chaque case
                cles = i.persos.values()  # 'objet'
                for j in cles:  # pour chaque objet
                    print(j.parent.nom)
                    if j.parent.nom != self.parent.nom:
                        print("============== DETECTION ENNEMI============")
                        self.attaquer(j)
            self.delai_verifier_champ = 30
#
# class DruideOurs(Perso):
#     def __init__(self, parent, id, maison, couleur, x, y, montype):
#         Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
#         self.force = 20
#         self.distancefeumax = 50
#         self.delaifeu = 20
#         self.delaifeumax = 20
#         self.delai_verifier_champ = 30
#         self.vision_cases = 10
#         self.cibleennemi = None
#         self.position_visee = None
#         self.etats_et_actions = {"bouger": self.bouger,
#                                  "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
#                                  "ciblerennemi": self.cibler,
#                                  "contourne": self.contourne,
#                                  "bougerversennemi": self.bouger_vers_ennemi,
#                                  "verifierchampvision": self.verifier
#                                  }
#         self.actioncourante = "verifierchampvision"
#
#     # def bouger(self):
#     #     if self.position_visee:
#     #         # le if sert à savoir si on doit repositionner notre visee pour un objet
#     #         # dynamique comme le daim
#     #         x = self.position_visee[0]
#     #         y = self.position_visee[1]
#     #         ang = Helper.calcAngle(self.x, self.y, x, y)
#     #         x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
#     #         ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
#     #         self.get_directon_vers_position_visee()
#     #         # print("avant : ", self.x,"/", self.y )
#     #         # self.x, self.y = self.test_etat_du_sol(x1, y1)
#     #         if self.test_etat_du_sol(x1, y1):
#     #             self.action_precedente = self.actioncourante
#     #             self.actioncourante = "contourne"
#     #             return "contourne"
#     #         self.parent.parent.trouver_case(self.x, self.y).persos.pop(self.id)
#     #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
#     #         self.x, self.y = x1, y1
#     #         self.case = self.parent.parent.trouver_case(self.x, self.y)
#     #         self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self
#     #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
#     #         ######## FIN DE TEST POUR SURFACE MARCHEE
#     #         # si tout ba bien on continue avec la nouvelle valeur
#     #         # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
#     #         dist = Helper.calcDistance(self.x, self.y, x, y)
#     #
#     #         if dist <= self.vitesse:
#     #             if self.actioncourante == "bouger":
#     #                 self.actioncourante = "verifierchampvision"
#     #             return "rendu"
#     #         else:
#     #             return dist
#
#     def cibler(self):
#         self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
#         if self.x < self.position_visee[0]:
#             self.dir = "D"
#         else:
#             self.dir = "G"
#
#         self.image = self.image[:-1] + self.dir
#         self.actioncourante = "attaquerennemi"
#
#     def attaquer(self, ennemi):
#         self.cibleennemi = ennemi
#         x = self.cibleennemi.x
#         y = self.cibleennemi.y
#         self.position_visee = [x, y]
#         dist = Helper.calcDistance(self.x, self.y, x, y)
#         print("DISTANCE CALCULEE", dist)
#
#         if dist <= self.distancefeumax:  # la distance fonctionne, mais augmenter la distancefeu
#             self.actioncourante = "attaquerennemi"
#             print("self.actioncourante = attaquerennemi")
#         else:  # si la distance est trop grande ca fait juste le cibler et ca arrete la
#             self.actioncourante = "bougerversennemi"
#             print("self.actioncourante = ciblerennemi")
#
#     def attaquerennemi(self):
#         if self.cibleennemi:
#             self.delaifeu = self.delaifeu - 1
#             print("KAWABUNGA BABY")
#             print(" DELAI FEU : ", self.delaifeu)
#
#             if self.delaifeu == 0:
#                 rep = self.cibleennemi.recevoir_coup(self.force)
#                 self.delaifeu = self.delaifeumax
#                 if rep:
#                     self.actioncourante = "verifierchampvision"
#                     try:
#                         self.parent.parent.trouver_case(self.cibleennemi.x, self.cibleennemi.y).persos.pop(self.cibleennemi.id)
#                     except:
#                         pass
#                 # self.cibleennemi.recevoir_coup(self.force)
#                 # self.fleches.remove(rep)
#
#     def verifier(self):
#         self.verifier_champ_vision(self.x, self.y, self.vision_cases)
#
#     def verifier_champ_vision(self, x, y, radius):
#         self.delai_verifier_champ -= 1
#         if self.delai_verifier_champ == 0:
#             cases = self.parent.parent.get_subcarte(x, y, radius)
#             print("CASES", cases)
#             for i in cases:  # chaque case
#                 cles = i.persos.values()  # 'objet'
#                 for j in cles:  # pour chaque objet
#                     print(j.parent.nom)
#                     if j.parent.nom != self.parent.nom:
#                         print("============== DETECTION ENNEMI============")
#                         self.attaquer(j)
#             self.delai_verifier_champ = 30


class Ingenieur(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)


class Ballista(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)

        self.dir = "DH"
        self.image = couleur[0] + "_" + montype + self.dir
        self.cible = None
        self.angle = None
        self.distancefeumax = 360
        self.distancefeu = 360
        self.delai_verifier_champ = 30
        self.vision_cases = 10
        self.delaifeu = 90
        self.force = 80
        self.champvision = 100
        self.vitesse = 25
        self.mana = 200
        self.delaifeumax = 90
        self.fleches = []
        self.cibleennemi = None
        self.position_visee = None
        # self.nomimg="ballista"
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi": self.bouger_vers_ennemi,
                                 "verifierchampvision": self.verifier,
                                 "bougerversennemi": self.bouger_vers_ennemi
                                 }
        self.actioncourante = "verifierchampvision"

    # def bouger(self):
    #     if self.position_visee:
    #         # le if sert à savoir si on doit repositionner notre visee pour un objet
    #         # dynamique comme le daim
    #         x = self.position_visee[0]
    #         y = self.position_visee[1]
    #         ang = Helper.calcAngle(self.x, self.y, x, y)
    #         x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
    #         ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
    #         self.get_directon_vers_position_visee()
    #         # print("avant : ", self.x,"/", self.y )
    #         # self.x, self.y = self.test_etat_du_sol(x1, y1)
    #         if self.test_etat_du_sol(x1, y1):
    #             self.action_precedente = self.actioncourante
    #             self.actioncourante = "contourne"
    #             return "contourne"
    #         self.parent.parent.trouver_case(self.x, self.y).persos.pop(self.id)
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         self.x, self.y = x1, y1
    #         self.case = self.parent.parent.trouver_case(self.x, self.y)
    #         self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self
    #         print("Dans perso cases: ", self.parent.parent.trouver_case(self.x, self.y).persos)
    #         ######## FIN DE TEST POUR SURFACE MARCHEE
    #         # si tout ba bien on continue avec la nouvelle valeur
    #         # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
    #         dist = Helper.calcDistance(self.x, self.y, x, y)
    #
    #         if dist <= self.vitesse:
    #             if self.actioncourante == "bouger":
    #                 self.actioncourante = "verifierchampvision"
    #             return "rendu"
    #         else:
    #             return dist

    def cibler(self):
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"
        if self.y < self.position_visee[1]:
            self.dir = self.dir + "B"
        else:
            self.dir = self.dir + "H"

        self.image = self.image[:-2] + self.dir
        self.actioncourante = "attaquerennemi"

    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.position_visee = [x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)

        if dist <= self.distancefeu:  # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "ciblerennemi"
        else:  # si la distance est trop grande ca fait juste le cibler et ca arrete la
            self.actioncourante = "bougerversennemi"

    def attaquerennemi(self):
        if self.cibleennemi:
            self.delaifeu = self.delaifeu - 1
            if self.delaifeu == 0:
                id = get_prochain_id()
                fleche = Fleche(self, id, self.cibleennemi)  # avant cetait ciblennemi
                self.fleches.append(fleche)
                self.delaifeu = self.delaifeumax
            if len(self.fleches) > 0:
                for i in self.fleches:
                    rep = i.bouger()
            # if rep:
            # self.cibleennemi.recevoir_coup(self.force)
            # self.fleches.remove(rep)

    def verifier(self):
        self.verifier_champ_vision(self.x, self.y, self.vision_cases)

    def verifier_champ_vision(self, x, y, radius):
        self.delai_verifier_champ -= 1
        if self.delai_verifier_champ == 0:
            cases = self.parent.parent.get_subcarte(x, y, radius)
            print("CASES", cases)
            for i in cases:  # chaque case
                cles = i.persos.values()  # 'objet'
                for j in cles:  # pour chaque objet
                    print(j.parent.nom)
                    if j.parent.nom != self.parent.nom:
                        print("============== DETECTION ENNEMI============")
                        self.attaquer(j)
            self.delai_verifier_champ = 30

class Catapulte(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)

        self.dir = "DH"
        self.image = couleur[0] + "_" + montype + self.dir
        self.cible = None
        self.angle = None
        self.distancefeumax = 360
        self.distancefeu = 360
        self.delai_verifier_champ = 30
        self.vision_cases = 10
        self.delaifeu = 90
        self.force = 80
        self.champvision = 100
        self.vitesse = 3
        self.mana = 200
        self.delaifeumax = 90
        self.fleches = []
        self.cibleennemi = None
        self.position_visee = None
        # self.nomimg="ballista"
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi": self.bouger_vers_ennemi,
                                 "verifierchampvision": self.verifier,
                                 "bougerversennemi": self.bouger_vers_ennemi
                                 }
        self.actioncourante = "verifierchampvision"

    def cibler(self):
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"
        if self.y < self.position_visee[1]:
            self.dir = self.dir + "B"
        else:
            self.dir = self.dir + "H"

        self.image = self.image[:-2] + self.dir
        self.actioncourante = "attaquerennemi"

    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        self.position_visee = [x, y]
        dist = Helper.calcDistance(self.x, self.y, x, y)

        if dist <= self.distancefeu:  # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "ciblerennemi"
        else:  # si la distance est trop grande ca fait juste le cibler et ca arrete la
            self.actioncourante = "bougerversennemi"

    def attaquerennemi(self):
        if self.cibleennemi:
            self.delaifeu = self.delaifeu - 1
            if self.delaifeu == 0:
                id = get_prochain_id()
                fleche = Fleche(self, id, self.cibleennemi)  # avant cetait ciblennemi
                self.fleches.append(fleche)
                self.delaifeu = self.delaifeumax
            if len(self.fleches) > 0:
                for i in self.fleches:
                    rep = i.bouger()
            # if rep:
            # self.cibleennemi.recevoir_coup(self.force)
            # self.fleches.remove(rep)

    def verifier(self):
        self.verifier_champ_vision(self.x, self.y, self.vision_cases)

    def verifier_champ_vision(self, x, y, radius):
        self.delai_verifier_champ -= 1
        if self.delai_verifier_champ == 0:
            cases = self.parent.parent.get_subcarte(x, y, radius)
            print("CASES", cases)
            for i in cases:  # chaque case
                cles = i.persos.values()  # 'objet'
                for j in cles:  # pour chaque objet
                    print(j.parent.nom)
                    if j.parent.nom != self.parent.nom:
                        print("============== DETECTION ENNEMI============")
                        self.attaquer(j)
            self.delai_verifier_champ = 30



class Ouvrier(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.activite = None  # sedeplacer, cueillir, chasser, pecher, construire, reparer, attaquer, fuir, promener,explorer,chercher
        self.typeressource = None
        self.quota = 20
        self.ramassage = 0
        self.cibletemp = None
        self.dejavisite = []
        self.champvision = random.randrange(100) + 300
        self.champchasse = 120
        self.javelots = []
        self.vitesse = random.randrange(5) + 5
        self.etats_et_actions = {"bouger": self.bouger,
                                 "ciblersiteconstruction": self.cibler_site_construction,
                                 "ciblerproie": self.cibler_proie,
                                 "ciblerennemi": None,
                                 "attaquerennemi": None,
                                 "construirebatiment": self.construire_batiment,
                                 "ramasserressource": self.ramasser,
                                 "ciblerressource": self.cibler_ressource,
                                 "retourbatimentmere": self.retour_batiment_mere,
                                 "validerjavelot": self.valider_javelot,
                                 "contourne": self.contourne
                                  }

    def chasser_ramasser(self, objetcible, sontype, actiontype):
        self.cible = objetcible
        self.typeressource = sontype
        self.position_visee = [self.cible.x, self.cible.y]
        self.actioncourante = actiontype

    def retour_batiment_mere(self):
        reponse = self.bouger()
        if reponse == "rendu":
            if self.cible:
                if self.typeressource == "baie" or self.typeressource == "daim" or self.typeressource == "eau" or self.typeressource == "ours":
                    self.parent.ressources["nourriture"] += self.ramassage
                else:
                    self.parent.ressources[self.typeressource] += self.ramassage
                self.ramassage = 0
                if self.cible.valeur < 1:
                    rep = self.chercher_nouvelle_ressource(self.cible.montype, self.cible.idregion)
                    self.cibler(rep)
                if self.cible:
                    self.cibler(self.cible)
                    if self.cible.montype == "daim" or self.cible.montype == "ours":
                        self.actioncourante = "ciblerproie"
                    else:
                        self.actioncourante = "ciblerressource"
                else:
                    self.actioncourante = None
        else:
            pass

    def cibler_ressource(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "ramasserressource"

    def cibler_site_construction(self):
        reponse = self.bouger()
        if reponse == "rendu":
            self.actioncourante = "construirebatiment"

    def cibler_proie(self):
        self.position_visee = [self.cible.x, self.cible.y]
        reponse = self.bouger()
        print("reponse de bouger dans cibler proie", reponse)
        if reponse == "contourne":
            return "contourne"
        if reponse == "rendu":
            if self.typeressource == "daim" or self.typeressource == "eau" or self.typeressource == "ours":
                self.actioncourante = "ramasserressource"
        elif reponse <= self.champchasse and self.cible.en_vie:
            self.actioncourante = "validerjavelot"

    def valider_javelot(self):
        self.lancer_javelot(self.cible)
        for i in self.javelots:
            i.bouger()

    def ramasser(self):
        self.ramassage += 1
        self.cible.valeur -= 1
        if self.cible.valeur == 0 or self.ramassage == self.quota:
            self.actioncourante = "retourbatimentmere"
            self.position_visee = [self.batimentmere.x, self.batimentmere.y]
            if self.cible.valeur == 0:
                self.parent.avertir_ressource_mort(self.typeressource, self.cible)
                # rep = self.chercher_nouvelle_ressource(self.cible.montype, self.cible.idregion)
                # if rep:
                #     if self.id != rep.id:
                #         self.cible=rep
        else:
            self.parent.parent.trouver_case(self.x,self.y).persos.pop(self.id)
            self.x = self.x + random.randrange(4) - 2
            self.y = self.y + random.randrange(4) - 2
            self.parent.parent.trouver_case(self.x, self.y).persos[self.id] = self

    def construire_batiment(self):
        self.cible.decremente_delai()

        if self.cible.sorte == "siteconstruction":
            return

        if self.cible.delai < 1:
            try:
                batiment = self.parent.parent.classesbatiments[self.cible.sorte](self, self.cible.id, self.parent.couleur,
                                                                             self.cible.x, self.cible.y,
                                                                             self.cible.sorte)
                self.parent.batiments[self.cible.sorte][self.cible.id] = batiment


                sitecons = self.parent.batiments['siteconstruction'].pop(batiment.id)
                self.parent.installer_batiment(batiment)
            except:
                print("batiment deja terminer")

            if self.cible.sorte == "maison":
                self.batimentmere = batiment

            self.cible = None
            self.actioncourante = None

    def construire_site_construction(self, site_construction):
        self.cibler(site_construction)
        self.actioncourante = "ciblersiteconstruction"
        # pass #monte le batiment par etapes on pourrait montrer l'anavancement de la construciton

    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()
            # print("REPONSE==========================================================", type(reponse))
            # lors dune attaque, ca fait un NonType not callable, mais tous les coups autre quune attaque donne NoneType et sont callés

    def lancer_javelot(self, proie):
        if self.javelots == []:
            id = get_prochain_id()
            self.javelots.append(Javelot(self, id, proie))

    def chercher_nouvelle_ressource(self, typ, idreg):
        if typ != "baie" and typ != "daim" and typ != "ours":
            reg = self.parent.parent.regions[typ]
            if idreg in reg:
                regspec = self.parent.parent.regions[typ][idreg]
                n = len(regspec.dicocases)
                while n > 0:
                    clecase = list(regspec.dicocases.keys())
                    case = regspec.dicocases[random.choice(clecase)]
                    n -= 1
                    if case.ressources:
                        clecase2 = list(case.ressources.keys())
                        newress = case.ressources[random.choice(clecase2)]
                        if newress.montype == typ:
                            return newress
                return None
        else:
            nb = len(self.parent.parent.biotopes[typ])
            for i in range(nb):
                rep = random.choice(list(self.parent.parent.biotopes[typ].keys()))
                obj = self.parent.parent.biotopes[typ][rep]
                if obj != self.cible:
                    distance = Helper.calcDistance(self.x, self.y, obj.x, obj.y)
                    if distance <= self.champvision:
                        return obj
            return None

    # def deplacer(self,pos):
    #     self.position_visee = pos
    #     self.actioncourante = "bouger"
    #
    # def bouger(self):
    #     if self.position_visee:
    #         # le if sert à savoir si on doit repositionner notre visee pour un objet
    #         # dynamique comme le daim
    #         x = self.position_visee[0]
    #         y = self.position_visee[1]
    #         ang = Helper.calcAngle(self.x, self.y, x, y)
    #         x1, y1 = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
    #         ######## ICI METTRE TEST PROCHAIN PAS POUR VOIR SI ON PEUT AVANCER
    #         self.test_etat_du_sol(x1, y1)
    #         ######## FIN DE TEST POUR SURFACE MARCHEE
    #         # si tout ba bien on continue avec la nouvelle valeur
    #         self.x, self.y = x1, y1
    #         # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
    #         dist = Helper.calcDistance(self.x, self.y, x, y)
    #         if dist <= self.vitesse:
    #             if self.actioncourante=="bouger":
    #                 self.actioncourante=None
    #             return "rendu"
    #         else:
    #             return dist

    # def test_etat_du_sol(self,x1, y1):
    #     ######## SINON TROUVER VOIE DE CONTOURNEMENT
    #     # ici oncalcule sur quelle case on circule
    #     casex = x1 / self.parent.parent.taillecase
    #     if casex != int(casex):
    #         casex = int(casex) + 1
    #     casey = y1 / self.parent.parent.taillecase
    #     if casey != int(casey):
    #         casey = int(casey) + 1
    #     #####AJOUTER TEST DE LIMITE
    #     # test si different de 0 (0=plaine), voir Partie pour attribution des valeurs
    #     if self.parent.parent.cartecase[int(casey)][int(casex)].montype != "plaine":
    #         # test pour être sur que de n'est 9 (9=batiment)
    #         if self.parent.parent.cartecase[int(casey)][int(casex)].montype != "batiment":
    #             print("marche dans ", )
    #         else:
    #             print("marche dans batiment")

    def abandonner_ressource(self, ressource):
        if ressource == self.cible:
            if self.actioncourante == "ciblerressource" or self.actioncourante == "retourbatimentmere" or self.actioncourante == "ramasserresource":
                self.actioncourante = "retourbatimentmere"
            else:
                self.actioncourante = "retourbatimentmere"
                self.position_visee = [self.batimentmere.x, self.batimentmere.y]

    ## PAS UTILISER POUR LE MOMENT
    def scanner_alentour(self):
        dicojoueurs = self.parent.parent.joueurs
        for i in dicojoueurs.values():
            for j in i.ouvriers.values():
                if j != self:
                    if Helper.calcDistance(self.x, self.y, j.x, j.y) <= self.champvision:
                        pass
        return 0

    # def trouver_cible(self, joueurs):
    #     c = None
    #     while c == None:
    #         listeclesj = list(joueurs.keys())
    #         c = random.choice(listeclesj)
    #         if joueurs[c].nom != self.parent.nom:
    #             listeclesm = list(joueurs[c].maisons.keys())
    #             maisoncible = random.choice(listeclesm)
    #             self.cible = joueurs[c].maisons[maisoncible]
    #         else:
    #             c = None
    #     self.angle = Helper.calcAngle(self.x, self.y, self.cible.x, self.cible.y)







    # LEGACY COLLiSION

    # def get_directon_vers_position_visee(self):
    #     # utilisé pour collision, demander permission avant DE BRISER MON CODE
    #     if self.position_visee:
    #         if self.x < self.position_visee[0]:
    #             self.dir = "D"
    #         else:
    #             self.dir = "G"
    #
    #         if self.y < self.position_visee[1]:
    #             self.dir += "B"
    #         else:
    #             self.dir += "H"

    # def contourne(self):
    #     if not self.cible_contournement:
    #         self.get_cible_contournement()
    #
    #     try:
    #         x = self.cible_contournement[0]
    #         y = self.cible_contournement[1]
    #     except:
    #         self.actioncourante = None
    #         self.cibles_contournement_precedentes = []
    #         return
    #
    #     ang = Helper.calcAngle(self.x, self.y, x, y)
    #     self.x, self.y  = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
    #     dist = Helper.calcDistance(self.x, self.y, x, y)
    #
    #     if dist <= self.vitesse:
    #         self.cible_contournement = None
    #         self.actioncourante = self.action_precedente

    # def get_cible_contournement(self):
    #     cases = self.get_map_contournement()
    #     #choisi la direction une seule fois
    #     # if self.contournements == 1:
    #     self.get_directon_vers_position_visee()
    #
    #     taille = self.parent.parent.taillecase
    #     if cases:
    #         if self.dir == "GH":
    #             self.cible_contournement = cases[0].x*taille, cases[0].y*taille
    #         elif self.dir == "DH":
    #             self.cible_contournement = cases[-1].x*taille, cases[-1].y*taille
    #         elif self.dir == "GB":
    #             self.cible_contournement = cases[0].x*taille, cases[0].y*taille
    #         elif self.dir == "DB":
    #             self.cible_contournement = cases[-1].x*taille, cases[-1].y*taille

    # def get_map_contournement(self):
    #     x1, y1 = self.x, self.y
    #
    #     casex = x1 / self.parent.parent.taillecase
    #     if casex != int(casex):
    #         casex = int(casex) + 1
    #     casey = y1 / self.parent.parent.taillecase
    #     if casey != int(casey):
    #         casey = int(casey) + 1
    #
    #     taille = self.parent.parent.taillecase
    #
    #     cases_cibles = []
    #     # trouve si on frappe un mur à l'horinzontal ou vertial
    #     if self.get_directon_contournement(x1,y1): #horizontal
    #         cases = self.parent.parent.get_carte_contournement(x1, y1, 1,self.contournement_range)
    #     else: #vertical
    #         cases = self.parent.parent.get_carte_contournement(x1, y1, self.contournement_range,1)
    #
    #     for i in cases:
    #         if i.montype == "batiment":
    #             # AFFICHAGE POUR DEBUG ---------------------------------------------------------------------------------
    #             xa, ya, xb, yb = i.x * taille, i.y * taille, i.x * taille + taille, i.y * taille + taille
    #             self.parent.parent.parent.vue.canevas.create_rectangle(xa, ya, xb, yb, fill="red", tags=("statique",))
    #             # AFFICHAGE POUR DEBUG ---------------------------------------------------------------------------------
    #         elif i.montype == "batiment-back":
    #             xa, ya, xb, yb = i.x * taille, i.y * taille, i.x * taille + taille, i.y * taille + taille
    #             self.parent.parent.parent.vue.canevas.create_rectangle(xa, ya, xb, yb, fill="crimson", tags=("statique",))
    #         elif i.montype == "coin":
    #             xa, ya, xb, yb = i.x * taille, i.y * taille, i.x * taille + taille, i.y * taille + taille
    #             self.parent.parent.parent.vue.canevas.create_rectangle(xa, ya, xb, yb, fill="yellow", tags=("statique",))
    #         elif i.montype == "batiment-m":
    #             xa, ya, xb, yb = i.x * taille, i.y * taille, i.x * taille + taille, i.y * taille + taille
    #             self.parent.parent.parent.vue.canevas.create_rectangle(xa, ya, xb, yb, fill="goldenrod", tags=("statique",))
    #         else:
    #             cases_cibles.append(i)
    #             # AFFICHAGE POUR DEBUG ---------------------------------------------------------------------------------
    #             # xa, ya, xb, yb = i.x * taille, i.y * taille, i.x * taille + taille, i.y * taille + taille
    #             # self.parent.parent.parent.vue.canevas.create_rectangle(xa, ya, xb, yb, fill="green", tags=("statique",))
    #             # AFFICHAGE POUR DEBUG ---------------------------------------------------------------------------------
    #     # print("new map: ", len(cases_cibles))
    #     return cases_cibles

    # def get_directon_contournement(self, x1, y1):
    #     # suis-je plus près de ma cible sur l'axe des x ou y
    #     cases = self.parent.parent.get_carte_contournement(x1, y1, 1, 4)
    #     # retourn vrai pour un mouvement vertical
    #     if cases[3].montype == "batiment" and cases[5].montype == "batiment":
    #         return False
    #     if cases[4].montype == "batiment" and cases[6].montype == "batiment":
    #         return False
    #     if cases[-3].montype == "batiment" and cases[-5].montype == "batiment":
    #         return False
    #     if cases[-4].montype == "batiment" and cases[-6].montype == "batiment":
    #         return False
    #     else:
    #         return True

            # print("bad vertical")

        # cases = self.parent.parent.get_carte_contournement(x1, y1, 4, 1)
        # if cases[0].montype == "batiment" or cases[-1].montype == "batiment":
        #     print("bad vertical")

        # return  self.get_directon_contournement()
