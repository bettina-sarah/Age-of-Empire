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
        print(" avant",self.mana)
        print("soin rececois",self.force)

        if self.mana + soin >= self.manaMax:
            self.mana = self.manaMax
        else:
            self.mana += soin

        print("soin recu",self.mana)
        return 1

    def update_type_carte_batiment(self, cartebatiment):
        self.cartebatiment = cartebatiment;
        # modele
        # print(self.parent.parent.parent)
        self.parent.parent.parent.set_background_case_batiment(self.cartebatiment)
        pass

    def set_coins(self, coin_x1,coin_y1,coin_x2,coin_y2):
        print("set coins")
        self.coin_gh = (coin_x1-20, coin_y2+20)
        self.coin_dh = (coin_x2+20, coin_y2+20)
        self.coin_bg = (coin_x1-20, coin_y1-20)
        self.coin_bd = (coin_x2+20, coin_y1-20)


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


    # def get_coins(self):
    #     # UN MUR N'A PAS DE COIN
    #     return []

class MurV(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0

    # def get_coins(self):
    #     # UN MUR N'A PAS DE COIN
    #     return []

class Tour(Batiment):
    def __init__(self, parent, id, couleur, x, y, montype):
        Batiment.__init__(self, parent, id, x, y)
        self.image = couleur[0] + "_" + montype
        self.montype = montype
        self.maxperso = 20
        self.perso = 0
        self.nbr_mur_v = 0
        self.nbr_mur_h = 0

