## -*- Encoding: UTF-8 -*-

import requests  # garde la meme sessin pour continuer denvoyer les requetes
from AoEw_vue import *
from AoEw_modele import *


class Controleur():

    def __init__(self):
        self.type = None
        self.t = True
        self.ego_serveur = 0  # 1 si le joueur a creer la partie (seul lui peut 'lancer' la partie)
        self.iteration_boucle_jeu = 0
        self.actions_requises = []
        self.nom_joueur_local = self.generer_nom()
        self.partie = None  # cest le modele
        # liste des noms de joueurs
        self.joueurs = []
        self.prochain_splash = None  # requis pour sortir du splash et passer au lobby # splash screen est la premiere fenetre
        self.on_joue = 1  # si 0, indique qu'on saute un tour dans la boucle de jeu
        self.delai_de_boucle_de_jeu = 40
        # frequence des appels vers le serveur
        self.modulo_appeler_serveur = 4  # environ 5-6 fois par seconde
        # adresses du URL du serveur de jeu, adresse 127.0.0.1 est pour des tests avec un serveur local... utile pour tester
        # self.url_serveur = "http://jmdeschamps.pythonanywhere.com"
        self.url_serveur = "http://127.0.0.1:8000"
        self.session = None
        self.vue = Vue(self, self.url_serveur, self.nom_joueur_local)
        self.vue.root.mainloop()

    def test(self):

        self.iteration_boucle_jeu=0
        self.boucler_sur_lobby()

    # methode speciale pour remettre les parametres du serveur a leurs valeurs par defaut
    def reset_partie(self):  # car le serveur ne gere quune partie a la fois
        le_url = self.url_serveur + "/reset_jeu"
        rep_text = self.appeler_serveur(le_url, 0)
        self.vue.update_splash(rep_text[0][0])
        return rep_text

    # a partir du splash, permet de creer une partie (lance le lobby pour permettre a d'autres joueurs de se connecter)
    def creer_partie(self,
                     nom_joueur_local):  # permet aux autres de sinscrire a cette partie la. Pour recevoir dautres inscriptions
        if self.prochain_splash:
            self.vue.root.after_cancel(self.prochain_splash)
            self.prochain_splash = None
        self.nom_joueur_local = nom_joueur_local
        url = self.url_serveur + "/creer_partie"
        data = {'nom': self.nom_joueur_local
                }
        reptext = self.appeler_serveur(url, data, "POST")
        self.ego_serveur = True  # je suis la personne qui a demarrer une nouvelle partie
        self.vue.root.title("je suis " + self.nom_joueur_local)
        self.vue.changer_cadre("lobby")
        self.boucler_sur_lobby()

    def inscrire_joueur(self, nom, urljeu):  # une fois une partie cree et en attente de joueur
        if self.prochain_splash:
            self.vue.root.after_cancel(self.prochain_splash)
            self.prochain_splash = None
        if nom:
            self.nom_joueur_local = nom
        url = self.url_serveur + "/inscrire_joueur"
        params = {"nom": self.nom_joueur_local}
        reptext = self.appeler_serveur(url, params, "POST")
        self.vue.root.title("je suis " + self.nom_joueur_local)
        self.vue.changer_cadre("lobby")
        self.boucler_sur_lobby()

    def lancer_partie(
            self):  # active par le createur. Change letat du jewu sur le serveur, comme quoi la partie est lancee, on passe la boucle de jeu
        url = self.url_serveur + "/lancer_partie"
        params = {"nom": self.nom_joueur_local}
        reptext = self.appeler_serveur(url, params, "POST")

    # methode de demarrage local de la boucle de jeu (partie demarre ainsi)
    def initialiser_partie(self, mondict):
        # on recoit les divers parametres d'initialisation du serveur
        initaleatoire = mondict[1][0][0]
        # ment, decommenter un ligne et commenter l'autre
        # mais pour tester c'est bien de toujours avoir la meme suite de random
        # random ALEATOIRE fourni par le serveur
        # random.seed(int(initaleatoire))
        # random FIXE pour test
        random.seed(2546)  # essayer de trouver un seed avec les maisons pas loin
        # on recoit la derniere liste des joueurs pour la partie
        listejoueurs = []
        for i in self.joueurs:
            listejoueurs.append(i[0])

        print(listejoueurs)
        set(listejoueurs)
        print(listejoueurs)
        self.type = len(listejoueurs)
        # on cree le modele (la partie)
        self.partie = Partie(self, listejoueurs)
        # on passe le modele a la vue puisqu'elle trouvera toutes le sinfos a dessiner
        self.vue.modele = self.partie
        # on met la vue a jour avec les infos de partie
        self.vue.initialiser_avec_modele()
        # on change le cadre la fenetre pour passer dans l'interface de jeu
        self.vue.changer_cadre("jeu")
        self.vue.centrer_maison()
        # on lance la boucle de jeu
        self.boucler_sur_jeu()

    # APRES AVOIR OBTENU UNE CONNECTION AU SERVEUR
    def initialiser_splash_post_connection(self,
                                           url_serveur):  # permet a nimporte qui de se connecter sur un serveuer a une adresse nouvelle
        self.session = requests.Session()
        self.url_serveur = url_serveur
        self.boucler_sur_splash()

    # boucle de communication initiale avec le serveur pour creer ou s'inscrire a la partie
    def boucler_sur_splash(self):
        url = self.url_serveur + "/tester_jeu"
        params = {"nom": self.nom_joueur_local}
        mondict = self.appeler_serveur(url, params)
        # print(self.nom_joueur_local, mondict)
        if mondict:
            self.vue.update_splash(mondict[0])
        self.prochain_splash = self.vue.root.after(50, self.boucler_sur_splash)

    # on boucle sur le lobby en attendant l'inscription de tous les joueurs attendus
    def boucler_sur_lobby(self):
        url = self.url_serveur + "/boucler_sur_lobby"
        params = {"nom": self.nom_joueur_local}
        mondict = self.appeler_serveur(url, params, "POST")
        # si l'etat est courant, c'est que la partie vient d'etre lancer
        if "courante" in mondict[0]:
            self.initialiser_partie(mondict)
        else:
            self.joueurs = mondict
            self.vue.update_lobby(mondict)
            self.vue.root.after(50, self.boucler_sur_lobby)

    # La boucle principale pour jouer une partie
    def boucler_sur_jeu(self):  #
        self.iteration_boucle_jeu += 1

        # test pour communiquer avec le serveur periodiquement
        if self.iteration_boucle_jeu % self.modulo_appeler_serveur == 0:
            actions = []
            if self.actions_requises:
                actions = self.actions_requises
                self.actions_requises = []
            url = self.url_serveur + "/boucler_sur_jeu"
            if actions == []:
                actions = ''
            data = {"nom": self.nom_joueur_local,
                    "iteration_boucle_jeu": self.iteration_boucle_jeu,
                    "actions_requises": actions}
            try:
                mondict = self.appeler_serveur(url, data, method="POST")
                print(mondict)
                # verifie pour requete d'attente d'un joueur plus lent
                if "ATTENTION" in mondict:
                    self.on_joue = 0
                elif mondict:
                    self.partie.ajouter_actions_a_faire(self.iteration_boucle_jeu, mondict)

            except requests.exceptions.RequestException as e:
                print("An error occurred:", e)
                self.on_joue = 0

        if self.on_joue:
            # envoyer les messages au modele et a la vue de faire leur job
            self.partie.jouer_prochain_coup(self.iteration_boucle_jeu)
            self.vue.afficher_jeu()
        else:
            self.iteration_boucle_jeu -= 1
            self.on_joue = 1

        self.vue.root.after(self.delai_de_boucle_de_jeu, self.boucler_sur_jeu)

    ###################################################################
    # fonction qui fait les appels au serveur
    def appeler_serveur(self, url, paramsjm, method="GET"):
        if method == "GET":
            response = self.session.get(url, params=paramsjm)
        elif method == "POST":
            response = self.session.post(url, json=paramsjm)
        response.raise_for_status()
        return response.json()

    ###################################################################
    # generateur de nouveau nom (erreur possible si doublon)
    def generer_nom(self):
        nom_joueur_local = "JAJA_" + str(random.randrange(100, 1000))
        return nom_joueur_local

    def abandonner(self):  # pas fini dimplanter
        action = [self.nom_joueur_local, "abandonner", [self.nom_joueur_local + ": J'ABANDONNE !"]]
        self.actionsrequises = action
        self.vue.root.after(500, self.vue.root.destroy)

    ###############################################################################
    ### Placez vos fonctions ici
    def afficher_batiment(self, nom, batiment):  # ca devient un elem permanent du jeu alors on le met ici
        self.vue.afficher_batiment(nom, batiment)

    def supprimer_batiment(self, id_batiment, id_joueur):
        self.vue.supprimer_batiment(id_batiment)
        self.partie.delete_batim_joueurs(id_batiment, id_joueur)
        # self.partie.eliminer_joueur()

    def afficher_bio(self, bio):
        self.vue.afficher_bio(bio)

    def installer_batiment(self, nomjoueur, batiment):
        x1, y1, x2, y2 = self.vue.afficher_batiment(nomjoueur, batiment)
        return [x1, y1, x2, y2]

    def trouver_valeurs(self):
        vals = self.partie.trouver_valeurs()
        return vals

    def afficher_fin(self, gagnant):
        self.vue.afficher_fin(gagnant)

    # ajoute Abi AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHH
    def tuer_joueur(self):
        self.vue.unbind_joueur()
        self.vue.test_HUD()

    def retirer_batiment_minimap(self, id):
        self.vue.minicarte.delete(id)


if __name__ == '__main__':
    c = Controleur()

