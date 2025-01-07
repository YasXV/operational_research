import random
import os 
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import json


class Graphe:
    #JEan paul delaye
    # montrer que la colo est bonne sans montrer la colo  
    GRAPHE_DIR = "graphes"
    COLORATION_DIR = "colorations"

    def __init__(self, avec_poids=False, oriente=False):
        self.liste_adjacence = {}
        self.couleurs = {}
        self.conflits = 0
        self.calcul_coloration = False
        self.avec_poids=avec_poids
        self.oriente = oriente

    def ajouter_sommet(self, un_sommet=None, sommets=[]):
        """
        Ajoute un sommet ou une liste de sommets passés en paramètre.
        """
        if un_sommet is not None:
            sommets = [un_sommet]
        
        for sommet in sommets:
            if sommet not in self.liste_adjacence:
                self.liste_adjacence[sommet] = {}
                # Dès qu'une modification est appliquée à mon graphe,
                # la coloration devient caduque et il faut donc refaire un algorithme.
                self.calcul_coloration = False
                # On réinitialise la coloration
                self.couleurs = {}
            else:
                raise ValueError(f"Le sommet {sommet} est déjà présent dans le graphe")


    def supprimer_sommet(self, un_sommet=None, sommets=[]):
        """
        Supprime un sommet ou une liste de sommets passés en paramètre.
        """
        if un_sommet is not None:
            sommets = [un_sommet]

        if not sommets:
            raise ValueError("Vous devez spécifier au moins un sommet à supprimer.")
        
        sommets_supprimes = set()  # Pour éviter les doublons dans la liste de suppression.

        for sommet in sommets:
            if sommet in self.liste_adjacence:
                # Supprimer les arêtes du sommet chez ses voisins
                for voisin in list(self.liste_adjacence[sommet].keys()):
                    self.liste_adjacence[voisin].pop(sommet, None)

                # Supprimer le sommet du graphe
                del self.liste_adjacence[sommet]
                sommets_supprimes.add(sommet)
            else:
                raise ValueError(f"Le sommet {sommet} que vous essayez de supprimer n'est pas dans le graphe.")

        if sommets_supprimes:
            # Dès qu'une modification est appliquée, la coloration devient caduque.
            self.calcul_coloration = False
            # Réinitialiser la coloration
            self.couleurs = {}



    def ajouter_edge(self, sommet1=None, sommet2=None, poids=1, edges=[]):
        """
        Ajoute une arête entre deux sommets passés en paramètres, ou une liste d'arêtes.
        Chaque arête peut être un tuple (sommet1, sommet2, poids).
        """
        print("WOUHOUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUu1111111111111111111111111111")
        if len(edges)>0:  # Si une liste d'arêtes est fournie
            print("WOUHOUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUu")
            for edge in edges:
                if len(edge) == 3:
                    s1, s2, p = edge
                elif len(edge) == 2:
                    print("JE SUIS LAAAAAAAAAa")
                    s1, s2 = edge
                    p = poids  # Utiliser le poids par défaut si non spécifié
                else:
                    raise ValueError(f"Format d'arête invalide : {edge}. Attendu : (sommet1, sommet2) ou (sommet1, sommet2, poids).")
                
                self.ajouter_edge(s1, s2, p)  # Appeler récursivement pour chaque arête
        else:  # Si aucun ensemble d'arêtes n'est fourni, traiter un seul edge
            if sommet1 is None or sommet2 is None:
                raise ValueError("Vous devez spécifier deux sommets ou fournir une liste d'arêtes.")
            
            # Ajouter les sommets s'ils n'existent pas déjà
            if sommet1 not in self.liste_adjacence:
                self.ajouter_sommet(sommet1)
            if sommet2 not in self.liste_adjacence:
                self.ajouter_sommet(sommet2)
            
            # Vérifier si l'arête existe déjà
            if sommet2 in self.liste_adjacence[sommet1]:
                raise ValueError(f"L'arête entre {sommet1} et {sommet2} existe déjà avec un poids de {self.liste_adjacence[sommet1][sommet2]}.")
            
            # Ajouter l'arête avec son poids
            self.liste_adjacence[sommet1][sommet2] = poids
            
            # Si le graphe n'est pas orienté, ajouter également l'arête dans l'autre sens
            if not self.oriente:
                self.liste_adjacence[sommet2][sommet1] = poids

            # Marquer la coloration comme non calculée car la structure du graphe a changé
            self.calcul_coloration = False
            self.couleurs = {}





    def supprimer_edge(self, sommet1=None, sommet2=None, edges=[]):
        """
        Supprime une arête entre deux sommets ou une liste d'arêtes.
        Chaque arête dans la liste peut être un tuple (sommet1, sommet2).
        """
        if edges:  # Si une liste d'arêtes est fournie
            for edge in edges:
                if len(edge) == 2:
                    sommet1, sommet2 = edge
                else:
                    raise ValueError(f"Format d'arête invalide : {edge}. Attendu : (sommet1, sommet2).")
                
                # Appeler récursivement pour chaque arête
                self.supprimer_edge(sommet1=sommet1, sommet2=sommet2)
        else:  # Si aucune liste n'est fournie, traiter une seule arête
            if sommet1 is None or sommet2 is None:
                raise ValueError("Vous devez spécifier deux sommets ou fournir une liste d'arêtes.")
            
            if sommet1 in self.liste_adjacence and sommet2 in self.liste_adjacence[sommet1]:
                # Supprimer l'arête entre sommet1 et sommet2
                del self.liste_adjacence[sommet1][sommet2]
                
                # Si le graphe n'est pas orienté, supprimer également dans l'autre sens
                if not self.oriente:
                    del self.liste_adjacence[sommet2][sommet1]
                
                # Marquer la coloration comme non calculée car la structure du graphe a changé
                self.calcul_coloration = False
                self.couleurs = {}
            else:
                raise ValueError(f"L'arête entre {sommet1} et {sommet2} que vous cherchez à supprimer n'existe pas dans ce graphe.")


    def nombre_edges(self):
        edges = set()
        for sommet, voisins in self.liste_adjacence.items():
            for voisin, poids in voisins.items():
                if not self.oriente:
                    edges.add(tuple(sorted([sommet, voisin])))
                else:
                    edges.add((sommet, voisin))
        return len(edges)


    def nombre_sommets(self):
        """
        Retourne le nombre de sommets dans le graphe.
        """
        return len(self.liste_adjacence.values())
    
    def nombre_couleurs(self):
        """
        retourne le nombre de couleurs de mon graphe
        """
        return len(set(np.array(list(self.couleurs.values()))))

    def affichage_simple(self):
        """
        Affiche une version simple du graphe 
        """
        print(f"Nombre de sommets : {self.nombre_sommets()}\tNombre d'edges : {self.nombre_edges()}")
        for sommet, voisins in self.liste_adjacence.items():
            print(f"{sommet}: {voisins}")

    def analyser_coloration(self):
        """
        ananlyse la coloration à travers divers paramétres
        """
        if(self.calcul_coloration):
            print(f"Nombre de sommets : {self.nombre_sommets()}\tNombre d'edges : {self.nombre_edges()}\n")
            print(f"Nombre de couleurs : {self.nombre_couleurs()}")
            print(f"Nombre de conflits :{self.conflits}")
        else :
            raise ValueError("Coloration pas encore appliqué au graphe ou graphe modifié!")


    def modifier_poids_edge(self, sommet1, sommet2, nouveau_poids):
        """
        Modifie le poids d'une edge de mon graphe  
        """
        if sommet1 in self.liste_adjacence and sommet2 in self.liste_adjacence[sommet1]:
            self.liste_adjacence[sommet1][sommet2] = nouveau_poids
            if not self.oriente:
                self.liste_adjacence[sommet2][sommet1] = nouveau_poids
        #Dés qu'une modification est appliqué à mon graphe la coloration devient quaduc et il faut donc refaire un algo !
            self.calcul_coloration=False

    def generer_graphe_aleatoire(nombre_sommets, densite=0.1, avec_poids=False, oriente=False):
        """
        Génére un graphe aléatoire, par défaut la densité sera de 0.1 et le graphe est sans poids et non orienté.
        """
        graphe = Graphe(avec_poids, oriente)
        for i in range(nombre_sommets):
            graphe.ajouter_sommet(str(i))

        nombre_edges = int(densite * nombre_sommets * (nombre_sommets - 1) / 2)
        sommets = list(graphe.liste_adjacence.keys())
        
        edges_ajoutees = set()  # Utiliser un ensemble pour garder trace des arêtes existantes

        while len(edges_ajoutees) < nombre_edges:
            sommet1, sommet2 = random.sample(sommets, 2)
            # Assurer que l'arête n'existe pas déjà
            if (sommet1, sommet2) not in edges_ajoutees and (sommet2, sommet1) not in edges_ajoutees:
                if avec_poids:
                    poids = random.randint(1, 10)
                    graphe.ajouter_edge(sommet1, sommet2, poids)
                else:
                    graphe.ajouter_edge(sommet1, sommet2)
                edges_ajoutees.add((sommet1, sommet2))  # Ajouter l'edge au suivi des edges

        return graphe


    def ecrire_graphe(self, chemin_fichier):
        """
        Ecris le graphe dans un fichier JSON
        """
        print("J4ECRIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIs")
        data = {"oriente": self.oriente, "avec_poids": self.avec_poids, "graphe": self.liste_adjacence}
        os.makedirs(self.GRAPHE_DIR, exist_ok=True)
        chemin_complet = os.path.join(self.GRAPHE_DIR, chemin_fichier)
        with open(chemin_complet, 'w') as fichier:
            json.dump(data, fichier, indent=4)


    def lire_graphe(self, chemin_fichier):
        """
        Lis un graphe depuis un fichier JSON 
        """
        chemin_complet = os.path.join(self.GRAPHE_DIR, chemin_fichier)
        try:
            with open(chemin_complet, 'w') as fichier:
                data = json.load(fichier)
            if 'oriente' not in data or 'avec_poids' not in data or 'graphe' not in data:
                raise ValueError("Le fichier JSON ne contient pas toutes les clés nécessaires.")
            self.oriente = data['oriente']
            self.avec_poids = data['avec_poids']
            self.liste_adjacence = data['graphe']
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Erreur lors de la lecture du fichier : {str(e)}")

    def ecrire_coloration(self, chemin_fichier):
        """
        Sauvegarde une coloration et le graphe lié à cette coloration dans un fichier JSON 
        """
        data = {"oriente": self.oriente, "avec_poids": self.avec_poids, "graphe": self.liste_adjacence, "coloration": self.couleurs}
        os.makedirs(self.COLORATION_DIR, exist_ok=True)
        chemin_complet = os.path.join(self.COLORATION_DIR, chemin_fichier)
        with open(chemin_complet, 'w') as fichier:
            json.dump(data, fichier, indent=4)

    def lire_coloration(self, chemin_fichier):
        """ 
        Lis une coloration et le graphe associé à cette coloration depuis un fichier JSON 
        """
        chemin_complet = os.path.join(self.COLORATION_DIR, chemin_fichier)
        try:
            with open(chemin_complet, 'w') as fichier:
                data = json.load(fichier)
            graphe_origine_oriente = data['oriente']
            graphe_origine_avec_poids = data["avec_poids"]
            graphe_origine = data["graphe"]
            coloration = data["coloration"]

            if not self.verifier_graphe_identiques(graphe_origine, graphe_origine_avec_poids, graphe_origine_oriente):
                raise ValueError("Le graphe actuel ne correspond pas au graphe associé à cette coloration.")

            self.couleurs = coloration
            self.calcul_coloration = True
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Erreur lors de la lecture de la coloration : {str(e)}")

    def verifier_graphe_identiques(self, graphe_dict, avec_poids=False, oriente=False):
        """
        Vérifie que le graphe courant est identique à un graphe représenté sous forme de dictionnaire,
        en tenant compte de l'orientation des arêtes.
        
        :param graphe_dict: Dictionnaire représentant le graphe à comparer.
        :param oriente: Booléen indiquant si le graphe est orienté ou non.
        :return: True si les graphes sont identiques, False sinon.
        """
        # Si le graphe d'origine n'a pas les mêmes propriétes que le graphe de comparaison 
        if self.oriente != oriente or self.avec_poids != avec_poids :
            return False
        # Vérifie les sommets
        if set(self.liste_adjacence.keys()) != set(graphe_dict.keys()):
            return False

        # Vérifie les arêtes
        for sommet, voisins in self.liste_adjacence.items():
            if self.oriente:
                # Vérification stricte des arêtes avec orientation
                if set(voisins.items()) != set(graphe_dict.get(sommet, {}).items()):
                    return False
            else:
                # Pour un graphe non orienté, traiter les arêtes comme des ensembles
                voisins_actuels = {frozenset([sommet, voisin]) for voisin in voisins.keys()}
                voisins_attendus = {
                    frozenset([sommet, voisin]) for voisin in graphe_dict.get(sommet, {}).keys()
                }

                # Vérifier la correspondance des arêtes
                if voisins_actuels != voisins_attendus:
                    return False

        return True


    def coloration_greedy(self):
        """
        Algorithme de coloration greedy classique sur le graphe actuel.
        """
        for sommet in self.liste_adjacence:
            # Obtenir les couleurs utilisées par les voisins
            couleurs_voisins = {self.couleurs[voisin] for voisin in self.liste_adjacence[sommet] if voisin in self.couleurs}

            # Trouver la première couleur disponible
            couleur = 0
            while couleur in couleurs_voisins:
                couleur += 1

            # Assigner la couleur au sommet
            self.couleurs[sommet] = couleur

            #On a appliqué une coloration
            self.calcul_coloration=True

            #on évalue les conflits 
            self.evaluation_conflits()

    def welsh_powell(self):
        """
        Implémentation de l'algorithme Welsh-Powell pour la coloration du graphe.
        Prend en compte l'orientation et les poids si définis.
        """
        # Étape 1 : Trier les sommets par un critère combinant le degré (ou rang) et le poids des arêtes
        def critere(sommet):
            if self.avec_poids:
                # Si le graphe a des poids, on calcule le poids total des voisins
                poids_total = sum(self.liste_adjacence[sommet].values())
            else:
                # Sinon, on ne prend en compte que le degré (nombre de voisins)
                poids_total = 0
            # Retourne une paire (degré, poids) pour trier d'abord par degré décroissant, puis par poids décroissant
            return (len(self.liste_adjacence[sommet]), poids_total)

        # Trier les sommets d'abord par degré décroissant et ensuite par poids décroissant si les poids existent
        sommets_tries = sorted(
            self.liste_adjacence.keys(),
            key=lambda sommet: critere(sommet),
            reverse=True
        )
        print("Sommets triés :", sommets_tries)
        print(self.liste_adjacence)

        # Étape 2 : Coloration des sommets
        for sommet in sommets_tries:
            # Ensemble des couleurs utilisées par les voisins (sortants ou les deux directions selon l'orientation)
            couleurs_voisins = set()

            if self.oriente:
                # Pour un graphe orienté, seuls les voisins sortants sont pris en compte
                couleurs_voisins = {self.couleurs[voisin] for voisin in self.liste_adjacence[sommet] if voisin in self.couleurs}
            else:
                # Pour un graphe non orienté, traiter les voisins dans les deux sens
                for voisin in self.liste_adjacence[sommet]:
                    if voisin in self.couleurs:
                        couleurs_voisins.add(self.couleurs[voisin])
                    if sommet in self.liste_adjacence.get(voisin, {}):
                        couleurs_voisins.add(self.couleurs.get(sommet))
            print(f"TEST : {couleurs_voisins}")
            # Trouver la première couleur disponible
            couleur = 0
            while couleur in couleurs_voisins:
                couleur += 1

            # Assigner la couleur au sommet
            self.couleurs[sommet] = couleur

        # Indiquer qu'une coloration a été effectuée
        self.calcul_coloration = True

        # Évaluer les conflits éventuels
        self.evaluation_conflits()




    def afficher_graphe_colore(self):
        """
        Afficke le graphe coloré 
        """
        G = nx.Graph()
        for sommet, voisins in self.liste_adjacence.items():
            for voisin, poids in voisins.items():
                G.add_edge(sommet, voisin, weight=poids)

        pos = nx.spring_layout(G)
        couleurs = [self.couleurs[s] if s in self.couleurs else 0 for s in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=couleurs, cmap=plt.cm.rainbow, node_size=500)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)})
        plt.show(block=False)
        plt.pause(20)


    def evaluation_conflits(self):
        """
        Evalue les conflits uniquement lorsqu'une coloration a été calculée
        """
        if self.calcul_coloration:
            self.conflits = 0  # On s'assure que le compteur de conflits commence à zéro
            edges_evalues = set()  # Pour éviter de compter deux fois les edges dans les graphes non orientés

            for sommet, voisins in self.liste_adjacence.items():
                for voisin in voisins:
                    # Dans le cas des graphes non orientés, vérifier si l'arête a déjà été évaluée
                    if not self.oriente:
                        # Créer une clé unique pour chaque arête
                        edge = tuple(sorted([sommet, voisin]))
                        if edge not in edges_evalues:
                            edges_evalues.add(edge)
                            if self.couleurs[sommet] == self.couleurs[voisin]:
                                self.conflits += 1
                    else:
                        if self.couleurs[sommet] == self.couleurs[voisin]:
                            self.conflits += 1

        else:
            raise ValueError("Pas de coloration pour laquelle on peut déterminer les conflits")
        
    def initialiser_coloration(self):
        """
        Initialiser la coloration du graphe de manière aléatoire.
        Chaque sommet reçoit une couleur aléatoire différente.
        """
        for sommet in self.sommets:
            self.couleurs[sommet] = random.randint(0, len(self.sommets) - 1)

    def conflit(self, sommet):
        """
        Calculer le nombre de conflits de coloration pour un sommet donné.
        Un conflit se produit si un voisin a la même couleur que le sommet.
        :param sommet: Le sommet pour lequel on évalue les conflits.
        :return: Le nombre de conflits.
        """
        conflicts = 0
        for voisin in self.liste_adjacence[sommet]:
            if self.couleurs[sommet] == self.couleurs.get(voisin, -1):
                conflicts += 1
        return conflicts

        

def hill_climbing(self, iterations=1000):
    # Initialisation aléatoire de la coloration
    self.initialiser_coloration()

    for _ in range(iterations):
        # Calcul des conflits pour chaque sommet
        conflits = {sommet: self.conflit(sommet) for sommet in self.liste_adjacence}

        # Si tous les sommets sont colorés sans conflit, on arrête
        if sum(conflits.values()) == 0:
            break

        # Sélectionner le sommet avec le plus de conflits
        sommet_a_modifier = max(conflits, key=conflits.get)

        # Sauvegarder la couleur actuelle pour pouvoir revenir en arrière si nécessaire
        couleur_actuelle = self.couleurs[sommet_a_modifier]

        # Appliquer une modification de couleur
        # On cherche un voisin qui pourrait donner une meilleure couleur
        sommet, couleur_nouvelle = self.voisin(sommet_a_modifier)

        # Calculer les conflits avant et après le changement de couleur
        conflits_avant = self.conflit(sommet_a_modifier)

        # Si la modification a amélioré la solution (réduit les conflits), on garde la couleur
        if self.conflit(sommet) < conflits_avant:
            # Appliquer la nouvelle couleur
            self.couleurs[sommet_a_modifier] = couleur_nouvelle
        else:
            # Sinon, on revient à la couleur initiale (pas d'amélioration)
            self.couleurs[sommet_a_modifier] = couleur_actuelle

    return self.couleurs




'''
def tester_plusieurs_graphes():
    configurations = [
        {"nombre_sommets": 10, "densite": 0.3},
        {"nombre_sommets": 50, "densite": 0.2},
        {"nombre_sommets": 100, "densite": 0.1},
        {"nombre_sommets": 200, "densite": 0.05},
    ]

    for config in configurations:
        graphe = Graphe.generer_graphe_aleatoire(config["nombre_sommets"], config["densite"])
        print(f"\nTest avec {config['nombre_sommets']} sommets et densité {config['densite']} :")

        debut = time.time()
        couleurs = coloration_greedy(graphe)
        fin = time.time()

        conflits = evaluation_coloration(graphe, couleurs)
        nombre_couleurs = max(couleurs.values()) + 1

        print(f" - Nombre de couleurs utilisées : {nombre_couleurs}")
        print(f" - Nombre de conflits : {conflits}")
        print(f" - Temps d'exécution : {fin - debut:.4f} secondes")
'''



