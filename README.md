# Projet de Recherche sur les Algorithmes de Coloration de Graphes

## Description
Ce projet a pour but de développer et d'implémenter divers algorithmes de coloration de graphes. La coloration de graphes est un domaine important en théorie des graphes et a de nombreuses applications pratiques, telles que l'allocation de registres en compilation, la planification de tâches, et bien d'autres.

## Structure du Projet
La structure du projet est la suivante :

```
/recherche_op_lib
├── src/
│   ├── main.py
│   ├── graph_coloring/
│   │   ├── __init__.py
│   │   ├── algorithm1.py
│   │   ├── algorithm2.py
│   └── ...
├── tests/
│   ├── test_algorithm1.py
│   ├── test_algorithm2.py
│   └── ...
├── Makefile
└── README.md
```

- `src/` : Contient le code source du projet.
    - `main.py` : Le point d'entrée principal du projet.
- `tests/` : Contient les tests unitaires pour les algorithmes.
- `Makefile` : Contient les commandes pour initialiser, installer et tester le projet.
- `README.md` : Ce fichier.

## Installation et Lancement du Projet

Pour initialiser, installer et tester le projet, vous pouvez utiliser les commandes suivantes :

1. **Initialisation du projet :**
     ```sh
     make init
     ```

2. **Installation des dépendances :**
     ```sh
     make install
     ```

3. **Exécution des tests :**
     ```sh
     make test
     ```

## Contribution
Les contributions sont les bienvenues. Veuillez soumettre une pull request pour toute amélioration ou ajout d'algorithmes.

## Licence
Ce projet est libre ! have fun <3