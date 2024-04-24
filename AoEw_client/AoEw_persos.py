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
        self.force = 30 ##A REMMETTRE A 10
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
                self.parent.cibleennemi = None;

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
            self.parent.actioncourante = "ciblerressource"
            self.parent.javelots.remove(self)
            self.proie.mourir()
        else:
            dist = Helper.calcDistance(self.x, self.y, self.proiex, self.proiey)
            if dist < self.vitesse:
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
        self.montype = montype
        self.cible = None
        self.position_visee = None
        self.cibleennemi = None
        self.mana = 100
        self.force = 100
        self.champvision = 100
        self.vitesse = 5
        self.angle = None
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": None,  # caller la bonne fctn attaquer
                                 "ciblerennemi": None,
                                 "contourne": self.contourne}

        #contournement
        self.action_precedente = None
        self.cible_contournement = None
        self.cibles_contournement_precedentes = []
        self.contournements = 0
        self.contournement_range_base = 5
        self.contournement_range_offset = 0
        self.contournement_range = 5

        # 08 avril rendu a delai feu ballista. attaquer_ennemi dans etat et actions de ballista doit etre call


    def attaquer(self, ennemi):
        self.cibleennemi = ennemi
        x = self.cibleennemi.x
        y = self.cibleennemi.y
        pos_cible = x, y
        self.cibler(ennemi)
        dist = Helper.calcDistance(self.x, self.y, x, y)
        if dist <= self.vitesse:
            self.actioncourante = "attaquerennemi"
        else:
            self.actioncourante = "ciblerennemi"


#perso
    def attaquer_ennemi(self):
        rep = self.cibleennemi.recevoir_coup(self.force)
        if rep == 1:
            self.cibleennemi = None
            self.cible = None

            self.actioncourante = "deplacer"

    def recevoir_coup(self, force):
        self.mana -= force
        if self.mana < 1:
            self.parent.annoncer_mort(self)
            return 1

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
            self.get_directon_vers_position_visee()
            # print("avant : ", self.x,"/", self.y )
            # self.x, self.y = self.test_etat_du_sol(x1, y1)
            if self.test_etat_du_sol(x1, y1):
                self.action_precedente = self.actioncourante
                self.actioncourante = "contourne"
                return "contourne"
            self.x, self.y = x1,y1
            ######## FIN DE TEST POUR SURFACE MARCHEE
            # si tout ba bien on continue avec la nouvelle valeur
            # ici on test pour vori si nous rendu a la cible (en deca de la longueur de notre pas)
            dist = Helper.calcDistance(self.x, self.y, x, y)

            if dist <= self.vitesse:
                if self.actioncourante == "bouger":
                    self.actioncourante = None
                return "rendu"
            else:
                return dist

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
            if self.test_etat_du_sol(x1, y1):
                self.action_precedente = self.actioncourante
                self.actioncourante = "contourne"
                return "contourne"
            self.x, self.y = x1, y1
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


    def get_map_contournement(self):
        x1, y1 = self.x, self.y

        casex = x1 / self.parent.parent.taillecase
        if casex != int(casex):
            casex = int(casex) + 1
        casey = y1 / self.parent.parent.taillecase
        if casey != int(casey):
            casey = int(casey) + 1

        taille = self.parent.parent.taillecase

        cases_cibles = []
        # trouve si on frappe un mur à l'horinzontal ou vertial
        if self.get_directon_contournement(x1,y1): #horizontal
            cases = self.parent.parent.get_carte_contournement(x1, y1, 1,self.contournement_range)
        else: #vertical
            cases = self.parent.parent.get_carte_contournement(x1, y1, self.contournement_range,1)

        for i in cases:
            if i.montype == "batiment":
                # AFFICHAGE POUR DEBUG ---------------------------------------------------------------------------------
                xa, ya, xb, yb = i.x * taille, i.y * taille, i.x * taille + taille, i.y * taille + taille
                self.parent.parent.parent.vue.canevas.create_rectangle(xa, ya, xb, yb, fill="red", tags=("statique",))
                # AFFICHAGE POUR DEBUG ---------------------------------------------------------------------------------
            else:
                cases_cibles.append(i)
                # AFFICHAGE POUR DEBUG ---------------------------------------------------------------------------------
                # xa, ya, xb, yb = i.x * taille, i.y * taille, i.x * taille + taille, i.y * taille + taille
                # self.parent.parent.parent.vue.canevas.create_rectangle(xa, ya, xb, yb, fill="green", tags=("statique",))
                # AFFICHAGE POUR DEBUG ---------------------------------------------------------------------------------
        # print("new map: ", len(cases_cibles))
        return cases_cibles

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
        return case.montype == "batiment"

    def contourne(self):
        if not self.cible_contournement:
            self.get_cible_contournement()

        try:
            x = self.cible_contournement[0]
            y = self.cible_contournement[1]
        except:
            self.actioncourante = None
            self.cibles_contournement_precedentes = []
            return

        ang = Helper.calcAngle(self.x, self.y, x, y)
        self.x, self.y  = Helper.getAngledPoint(ang, self.vitesse, self.x, self.y)
        dist = Helper.calcDistance(self.x, self.y, x, y)

        if dist <= self.vitesse:
            self.cible_contournement = None
            self.actioncourante = self.action_precedente


    def get_cible_contournement(self):
        cases = self.get_map_contournement()
        self.get_directon_vers_position_visee()
        taille = self.parent.parent.taillecase
        if cases:
            if self.dir == "GH":
                self.cible_contournement = cases[0].x*taille, cases[0].y*taille
            elif self.dir == "DH":
                self.cible_contournement = cases[-1].x*taille, cases[-1].y*taille
            elif self.dir == "GB":
                self.cible_contournement = cases[0].x*taille, cases[0].y*taille
            elif self.dir == "DB":
                self.cible_contournement = cases[-1].x*taille, cases[-1].y*taille



class Soldat(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        self.force = 20


class Archer(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)

        self.dir = "D"
        # self.cible = None
        # self.angle = None
        self.distancefeumax = 360
        self.distancefeu = 360
        self.delaifeu = 30
        self.delaifeumax = 30
        self.fleches = []
        self.cibleennemi = None
        self.position_visee = None
        # self.nomimg="ballista"
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi": self.bouger_vers_ennemi
                                 }

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

        if dist <= self.distancefeu: # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "ciblerennemi"
        else: # si la distance est trop grande ca fait juste le cibler et ca arrete la
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


class Chevalier(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)


class Druide(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)
        
class DruideOurs(Perso):
    def __init__(self, parent, id, maison, couleur, x, y, montype):
        Perso.__init__(self, parent, id, maison, couleur, x, y, montype)


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
        self.delaifeu = 30
        self.delaifeumax = 30
        self.fleches = []
        self.cibleennemi = None
        self.position_visee = None
        # self.nomimg="ballista"
        self.etats_et_actions = {"bouger": self.bouger,
                                 "attaquerennemi": self.attaquerennemi,  # caller la bonne fctn attaquer
                                 "ciblerennemi": self.cibler,
                                 "contourne": self.contourne,
                                 "bougerversennemi":self.bouger_vers_ennemi
                                 }

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

        if dist <= self.distancefeu: # la distance fonctionne, mais augmenter la distancefeu
            self.actioncourante = "ciblerennemi"
        else: # si la distance est trop grande ca fait juste le cibler et ca arrete la
            self.actioncourante = "bougerversennemi"


    def attaquerennemi(self):
        if self.cibleennemi:
            self.delaifeu = self.delaifeu -1
            if self.delaifeu == 0:

                id = get_prochain_id()
                fleche = Fleche(self, id, self.cibleennemi) # avant cetait ciblennemi
                self.fleches.append(fleche)
                self.delaifeu = self.delaifeumax
            if len(self.fleches) > 0:
                for i in self.fleches:
                    rep = i.bouger()
            # if rep:
                # self.cibleennemi.recevoir_coup(self.force)
                # self.fleches.remove(rep)


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
                                 "contourne": self.contourne}

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
        if reponse == "contourne":
            return "contourne"
        if reponse == "rendu":
            if self.typeressource == "daim" or self.typeressource == "eau" or self.typeressource == "ours":
                self.actioncourante = "ramasserressource"
        elif reponse <= self.champchasse and self.cible.etat == "vivant":
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
            self.x = self.x + random.randrange(4) - 2
            self.y = self.y + random.randrange(4) - 2

    def construire_batiment(self):
        self.cible.decremente_delai()
        if self.cible.delai < 1:
            batiment = self.parent.parent.classesbatiments[self.cible.sorte](self, self.cible.id, self.parent.couleur,
                                                                             self.cible.x, self.cible.y,
                                                                             self.cible.sorte)
            self.parent.batiments[self.cible.sorte][self.cible.id] = batiment

            try:
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
