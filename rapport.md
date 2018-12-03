---
title: SCSS Compiler
subtitle: Rapport
lang: fr
author:
- Bulloni Lucas <lucas.bulloni@he-arc.ch>
- Wermeille Bastien <bastien.wermeille@he-arc.ch>
date: \today
pagesize: A4
numbersections: true
geometry: margin=2.5cm
header-includes: |
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhead[R]{Lucas Bulloni \& Bastien Wermeille}
---

\newpage

\tableofcontents

\newpage


# Project Sass compiler

Here is a simple basic Sass compiler.

## Author
- [Lucas Bulloni](https://github.com/bull0n)
- [Wermeille Bastien](https://github.com/Ph0tonic/)


# Introduction
Dans le cadre du cours "Compilateurs", il nous a été demandé de réaliser un projet par équipe de deux en utilisat la librairire python PLY.

Il

# But fixé
Comme expliqué plus haut, le but fixé était de réaliser un compilateur permettant de compiler du code SCSS.

- Etape 1 Validation de CSS Standard
- Etape 2 Ajout du nesting
- Etape 3 Mise en place des variables pour les propriétés
- Etape 4 Ajout de la gestion des branchements conditionnels tel que @if et @while
- Etape 5 Ajout de la compilation des valeurs comportant des calculs
- Etpoa 6 Mise en place de extend
- Etape 7 Ajout des mixins et des include
- etape 8 Possibilité d'inclure des fichiers externes avec @import

# Fonctionnalités implémentées
Ce chapitre liste les fonctionnalités présentes dans notre coimpilateur, dans leur ordre d'implémentation.

- Validation de la syntaxe de base d'un scss
- Gestion du nesting afin de générer du code css valide
- Ajout de variables
- Mise en place de branchements coindiutionnels tel que le @if, le @else et le @while
- Compilation des valeurs  nuériques calculées
- Mise en place de la gestion des extends permettant d'inclure du code facilement à l'intérieur d'un sélector
- ...

# Prise en main
Ce document démontre une utilisation basique des différentes fonctionnalités du programme. Pour
une meilleure prise en main, n’oubliez pas de lire les exemples !

Pour générer un fichier css à l’aide de notre compilateur, il suffit d’exécuter la commande suivante :

```sh
python Compiler.py CHEMIN_DU_FICHIER
```




# Grammaire
TODO

# Explications et exemples
TODO

# Guide utilisateur
TODO

# Difficultés rencontrés
TODO

# Améliorations
TODO

# Conclusion
TODO


# Sass Documentation

- https://sass-lang.com/guide

# Exemples
