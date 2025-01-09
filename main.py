from graphe import Graphe


test1 = Graphe()
test1.ajouter_edge(edges=[('1','2'),('0','1'),('2','3'),('3','0')])
test1.affichage_simple()
test1.ajouter_edge(edges=[('1','2'),('0','2'),('4','1')])
test1.affichage_simple()
'''test1.ajouter_sommet(sommets=['2','4'])
test1.affichage_simple()
test2=Graphe(oriente=True,avec_poids=True)
test2.ajouter_edge(edges=[('1','2',3),('0','1'),('2','4',3),('3','0'),('2','1')])
#test2 = Graphe.generer_graphe_aleatoire(10,0.3,avec_poids=True,oriente=False)
test2.welsh_powell()
test2.analyser_coloration()
test2.affichage_simple()
test2.afficher_graphe_colore()'''
'''test1 = Graphe.construire_graphe_depuis_dimacs("DSJC1000.9.col", oriente=True)
test1.affichage_simple()
test1.welsh_powell()
test1.analyser_coloration()'''

