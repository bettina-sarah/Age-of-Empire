import random
from AoEw_persos import Boulet
from AoEw_divers import *


class SiteConstruction():
    def __init__(self, parent: object, id: str, x: int, y: int, sorte: str, delai: int):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.etat = "attente"
        self.sorte = sorte
        self.delai = delai  # artie.valeurs[self.sorte]["delai"]

    def decremente_delai(self):
        self.delai -= 1


class Batiment():
    def __init__(self, parent, id, x, y):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.image = None
        self.montype = None
        self.maxperso = 0
        self.perso = 0
        self.cartebatiment = []
        self.mana = 200
        self.coin_gh = None
        self.coin_dh = None
        self.coin_bg = None
        self.coin_bd = None

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch Batiment")
        if self.mana < 1:
            print("MORTS")
            try:
                self.parent.parent.annoncer_mort_batiment(self)
            except:
                try:
                    print("MAISON PRINCIPALE")
                    self.parent.annoncer_mort_batiment(self)
                except:
                    print("plusieur unité cant")

            return 1

    def recevoir_soin(self, soin):
        print(" avant", self.mana)
        print("soin rececois", self.force)

        if self.mana + soin >= self.manaMax:
            self.mana = self.manaMax
        else:
            self.mana += soin

        print("soin recu", self.mana)
        return 1

    def update_type_carte_batiment(self, cartebatiment):
        self.cartebatiment = cartebatiment;
        # modele
        # print(self.parent.parent.parent)
        self.parent.parent.parent.set_background_case_batiment(self.cartebatiment)
        pass

    def set_coins(self, coin_x1, coin_y1, coin_x2, coin_y2):
        self.coin_gh = (coin_x1 - 20, coin_y2 + 20)
        self.coin_dh = (coin_x2 + 20, coin_y2 + 20)
        self.coin_bg = (coin_x1 - 20, coin_y1 - 20)
        self.coin_bd = (coin_x2 + 20, coin_y1 - 20)

    def get_coins(self):
        return self.coin_gh, self.coin_dh, self.coin_bg, self.coin_bd


class Usineballiste(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 10
        self.perso = 0


class Maison(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 10
        self.perso = 0


class Abri(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0


class Caserne(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0


class Champstir(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0


class MurH(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0



    def get_coins(self, y_perso):
        # si l'unité à un 'y' plus bas, il est donc physiquement du coté nord du mur, donc les coins possibles
        # sont les coins supérieurs, sinon on inverse
        print(y_perso, " < ", self.y, " = ", (y_perso > self.y))
        if y_perso > self.y:
            print("coins: gh ",self.coin_gh)
            print("coins: dh ",self.coin_dh)
            return self.coin_gh, self.coin_dh
        else:
            print("coins: bg ",self.coin_bg)
            print("coins: bd ",self.coin_bd)
            return self.coin_bg, self.coin_bd


class MurV(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0

    def get_coins(self, y_perso):
        # si l'unité à un 'y' plus bas, il est donc physiquement du coté nord du mur, donc les coins possibles
        # sont les coins supérieurs, sinon on inverse
        print(y_perso, " < ", self.y, " = ", (y_perso > self.y))
        if y_perso > self.y:
            print("coins: gh ",self.coin_gh)
            print("coins: dh ",self.coin_dh)
            return self.coin_gh, self.coin_dh
        else:
            print("coins: bg ",self.coin_bg)
            print("coins: bd ",self.coin_bd)
            return self.coin_bg, self.coin_bd

class Tour(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        # Archer.__init__(self, parent, id, couleur, x, y, montype)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0
        self.nbr_mur_gb = 0
        self.nbr_mur_db = 0
        self.nbr_mur_gh = 0
        self.nbr_mur_dh = 0

        # de ARCHER
        self.cibleennemi = None
        self.distancefeumax = 200
        self.delai_verifier_champ = 5
        self.vision_cases = 10
        self.distancefeu = 200
        self.delaifeu = 2
        self.delaifeumax = 10
        self.boulets = []

        self.etats_et_actions = {
            "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
            "verifierchampvision": self.verifier
        }

        self.actioncourante = "verifierchampvision"

    def jouer_prochain_coup(self):
        if self.actioncourante:
            reponse = self.etats_et_actions[self.actioncourante]()

    def attaquerennemi(self):
        print("Aattaque cible")
        # self.cibleennemi=cible
        self.delaifeu = self.delaifeu - 1
        print(self.delaifeu)
        if self.delaifeu == 0:
            try:
                id = get_prochain_id()
                print("AVNT creer fleche")
                boulet = Boulet(self, id, self.cibleennemi)  # avant cetait ciblennemi
                self.boulets.append(boulet)
                self.delaifeu = self.delaifeumax
            except:
                print("mort cible")
                # self.actioncourante= "verifierchampvision"


        if len(self.boulets) > 0:
            for i in self.boulets:
                rep = i.bouger()
            # if rep:
            # self.cibleennemi.recevoir_coup(self.force)
            # self.fleches.remove(rep)

    def verifier(self):
        self.verifier_champ_vision(self.x, self.y, self.vision_cases)

    def verifier_champ_vision(self, x, y, radius):
        self.delai_verifier_champ -= 1
        if self.delai_verifier_champ == 0:
            cases = self.parent.parent.parent.get_subcarte(x, y, radius)
            for i in cases:  # chaque case
                cles = i.persos.values()  # 'objet'
                for j in list(cles):  # pour chaque objet
                    if j.parent.nom != self.parent.parent.nom:
                        print("DANS TOUR")
                        print("============== DETECTION ENNEMI============")
                        self.cibleennemi = j
                        self.actioncourante = "attaquerennemi"
                        self.attaquerennemi()
            self.delai_verifier_champ = 30
