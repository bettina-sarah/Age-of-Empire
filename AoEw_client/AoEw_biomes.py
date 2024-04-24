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






class Animal():
    def __init__(self, parent, id, x, y, imgdep, valeur, vie, notyperegion=-1, idregion=None):
        self.parent = parent
        self.id = id
        self.idregion = idregion
        self.x = x
        self.y = y
        self.etat = "neutre"
        self.position_visee = None
        self.angle = None
        self.dir = "GB"
        self.nomimg = imgdep
        self.img = self.nomimg + self.dir
        self.vitesse = random.randrange(3) + 3
        self.montype = imgdep
        self.vie = vie
        self.valeur = valeur
        self.en_vie = True

    def mourir(self):
        #self.etat = "mort"
        self.en_vie = False
        print("MORT!!!")
        self.position_visee = None

    def recevoir_coup(self,dommage):
        self.vie -= dommage
        print("Ouch")
        if self.vie < 1:
            print("MORT")
            self.mourir()
            return 1

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
            if self.en_vie:
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


class Ours(Animal):
    def __init__(self, parent, id, x, y, tem='ours'):
        Animal.__init__(self, parent, id, x, y, tem, 10000, 20000)
        self.force=10



    def recevoir_coup(self, dommage, ennemi):
        self.vie -= dommage
        self.etat == "aggressif"
        self.attaquer(ennemi)
        print("Ouch ours!")
        if self.vie < 1:
            print("MORT")
            self.mourir()
            return 1

    # verifier range fonction qui va dans

    # ***** FONCTIONS PERSO:

    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        pos_cible = x, y
        self.cibler(ennemi)
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.vitesse:
            self.attaquer_ennemi()
        else:
            self.cibler(ennemi)

    def cibler(self, ennemi):
        self.cible = ennemi
        if self.cible:
            self.position_visee = [self.cible.x, self.cible.y]
            if self.x < self.position_visee[0]:
                self.dir = "D"
            else:
                self.dir = "G"
        else:
            self.position_visee = None


    def attaquer_ennemi(self):
        print("attquer de lours !!!")
        rep = self.cibleennemi.recevoir_coup(self.force)
        if rep == 1:
            self.cibleennemi = None
            self.cible = None

            self.deplacer()




    #***** FONCTIONS OUVRIER

    # def chasser_ramasser(self, objetcible, sontype, actiontype):
    #     self.cible = objetcible
    #     self.typeressource = sontype
    #     self.position_visee = [self.cible.x, self.cible.y]
    #     self.actioncourante = actiontype
    #
    # def cibler_proie(self):
    #     self.position_visee = [self.cible.x, self.cible.y]
    #     reponse = self.bouger()
    #     print("reponse de bouger dans cibler proie", reponse)
    #     if reponse == "contourne":
    #         return "contourne"
    #     if reponse == "rendu":
    #         if self.typeressource == "daim" or self.typeressource == "eau" or self.typeressource == "ours":
    #             self.actioncourante = "ramasserressource"
    #     elif reponse <= self.champchasse and self.cible.en_vie:
    #         self.actioncourante = "validerjavelot"




class Daim(Animal):
    def __init__(self, parent, id, x, y, tem='daim'):
        Animal.__init__(self, parent, id, x, y, tem, 40, 10)

# a ajouter etat neutre/aggresif ! maintenant vivant mort...

