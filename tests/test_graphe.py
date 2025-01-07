import pytest
from graphe import Graphe

def test_ajouter_sommet():
    g = Graphe()
    g.ajouter_sommet("1")
    assert "1" in g.liste_adjacence


def test_coloration_greedy():
    graphe = Graphe.generer_graphe_aleatoire(30, 0.5)
    graphe.coloration_greedy()

    # Vérifie qu'aucun sommet n'a la même couleur que ses voisins
    for sommet, voisins in graphe.liste_adjacence.items():
        for voisin in voisins:
            assert graphe.couleurs[sommet] != graphe.couleurs[voisin], "Les sommets voisins ne doivent pas avoir la même couleur."
