import random

class SiteConstruction():
    def __init__(self, parent: object, id: str, x: int, y: int, sorte: str, delai: int):
        self.parent = parent
        self.id = id
        self.x = x
        self.y = y
        self.etat = "attente"
        self.sorte = sorte
        self.delai = delai #artie.valeurs[self.sorte]["delai"]

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

    def recevoir_coup(self, force):
        self.mana -= force
        print("Ouch Batiment")
        if self.mana < 1:
            print("MORTS")
            try:
                self.parent.parent.annoncer_mort_batiment(self)
            except:
                print("MAISON PRINCIPALE")
                self.parent.annoncer_mort_batiment(self)
            return 1

    def recevoir_soin(self, soin):
        print(" avant",self.mana)
        print("soin rececois",self.force)

        if self.mana + soin >= self.manaMax:
            self.mana = self.manaMax
        else:
            self.mana += soin

        print("soin recu",self.mana)
        return 1


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

class MurV(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0

class Tour(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0

