from graphe import Graphe

def main():
    test = Graphe.generer_graphe_aleatoire(10,0.2)
    test.coloration_greedy()
    test.affichage_simple()
    test.afficher_graphe_colore()
if __name__ == "__main__":
    main()
