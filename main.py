from graphe import Graphe


test1 = Graphe.generer_graphe_aleatoire(10,0.2, oriente=False)
#test1.affichage_simple()
test1.welsh_powell()
print("whatt the aaaaaaa")

print("whatt the")
#test1.hill_climbing()
test1.analyser_coloration()
#test1.afficher_graphe_colore()
#test1.ajouter_edge(edges=[('10','1'),('9','1')])
test1.affichage_simple()
test1.analyser_coloration()
test1.welsh_powell()
test1.analyser_coloration()
#test1.ecrire_graphe("test1graphe")
#test1.ecrire_coloration("test1weird")