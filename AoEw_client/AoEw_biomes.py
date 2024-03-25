import random
from helper import Helper

class Biotope():
    def __init__(self, parent, id, monimg, x, y, montype, idregion=0, posid="0"):
        self.parent = parent
        self.id = id
        self.img = monimg
        self.x = x
        self.y = y
        self.montype = montype
        self.sprite = None
        self.spriteno = 0
        self.idregion = idregion
        self.idcaseregion = posid

class Baie(Biotope):
    typeressource = ['arbustebaiesgrand',
                     'arbustebaiespetit',
                     'arbustevert']

    def __init__(self, parent, id, monimg, x, y, montype):
        Biotope.__init__(self, parent, id, monimg, x, y, montype)
        self.valeur = 30

class Marais(Biotope):
    typeressource = ['marais1',
                     'marais2',
                     'marais3']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 100

class Eau(Biotope):
    typeressource = ['eaugrand1',
                     'eaugrand2',
                     'eaugrand3',
                     'eaujoncD',
                     'eaujoncG',
                     'eauquenouillesD',
                     'eauquenouillesG',
                     'eauquenouillesgrand',
                     'eautourbillon',
                     'eautroncs']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        n = random.randrange(50)
        if n == 6:
            self.spritelen = 6  # len(self.parent.parent.vue.gifs["poissons"])
            self.sprite = "poissons"
            self.spriteno = random.randrange(self.spritelen)
            self.valeur = 100
        else:
            self.valeur = 10

    def jouer_prochain_coup(self):
        if self.sprite:
            self.spriteno += 1
            if self.spriteno > self.spritelen - 1:
                self.spriteno = 0

class Aureus(Biotope):
    typeressource = ['aureusbrillant',
                     'aureusD_',
                     'aureusG',
                     'aureusrocgrand',
                     'aureusrocmoyen',
                     'aureusrocpetit']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 100

class Roche(Biotope):
    typeressource = ['roches1 grand',
                     'roches1petit',
                     'roches2grand',
                     'roches2petit',
                     'roches3grand',
                     'roches3petit',
                     'roches4grand',
                     'roches4petit',
                     'roches5grand']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 100

class Arbre(Biotope):
    typeressource = ['arbre0grand',
                     'arbre0petit',
                     'arbre1grand',
                     'arbre2grand',
                     'arbresapin0grand',
                     'arbresapin0petit']

    def __init__(self, parent, id, monimg, x, y, montype, cleregion, posid):
        Biotope.__init__(self, parent, id, monimg, x, y, montype, cleregion, posid)
        self.valeur = 30

class Daim():
    def __init__(self, parent, id, x, y, notyperegion=-1, idregion=None):
        self.parent = parent
        self.id = id
        self.etat = "vivant"
        self.nomimg = "daim"
        self.montype = "daim"
        self.idregion = idregion
        self.img = ""
        self.x = x
        self.y = y
        self.valeur = 40
        self.position_visee = None
        self.angle = None
        self.dir = "GB"
        self.img = self.nomimg + self.dir
        self.vitesse = random.randrange(3) + 3

    def mourir(self):
        self.etat = "mort"
        self.position_visee = None

    def deplacer(self):
        if self.position_visee:
            x = self.position_visee[0]
            y = self.position_visee[1]
            x1, y1 = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
            # probleme potentiel de depasser la bordure et de ne pas trouver la case suivante
            case = self.parent.trouver_case(x1, y1)
            # if case[0]>self.parent.taillecarte or case[0]<0:
            #    self.cible=None
            # elif case[1]>self.parent.taillecarte or case[1]<0:
            #    self.cible=None
            # else:
            if case.montype != "plaine":
                pass
                # print("marche dans ",self.parent.regionstypes[self.parent.cartecase[case[1]][case[0]]])
            # changer la vitesse tant qu'il est sur un terrain irregulier
            # FIN DE TEST POUR SURFACE MARCHEE
            self.x, self.y = x1, y1
            dist = Helper.calcDistance(self.x, self.y, x, y)
            if dist <= self.vitesse:
                self.cible = None
                self.position_visee = None
        else:
            if self.etat == "vivant":
                self.trouver_cible()

    def trouver_cible(self):
        n = 1
        while n:
            x = (random.randrange(100) - 50) + self.x
            y = (random.randrange(100) - 50) + self.y
            case = self.parent.trouver_case(x, y)
            # if case[0]>self.parent.taillecarte or case[0]<0:
            #    continue
            # if case[1]>self.parent.taillecarte or case[1]<0:
            #    continue

            if case.montype == "plaine":
                self.position_visee = [x, y]
                n = 0
        self.angle = Helper.calcAngle(self.x, self.y, self.position_visee[0], self.position_visee[1])
        if self.x < self.position_visee[0]:
            self.dir = "D"
        else:
            self.dir = "G"
        if self.y < self.position_visee[1]:
            self.dir = self.dir + "B"
        else:
            self.dir = self.dir + "H"
        self.img = self.nomimg + self.dir

