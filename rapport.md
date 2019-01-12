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

# But fixé
Comme expliqué plus haut, le but fixé était de réaliser un compilateur permettant de compiler du code SCSS. Les étapes de réalisation ont étés les suivantes :

- Etape 1 Validation de CSS Standard
- Etape 2 Ajout du nesting
- Etape 3 Mise en place des variables pour les propriétés
- Etape 4 Ajout de la gestion des branchements conditionnels tel que @if, @else if, @else et @while
- Etape 5 Ajout de la compilation des valeurs comportant des calculs
- Etape 6 Mise en place de l'héritage avec le mot clé @exted
- Etape 7 Ajout des mixins et des include avec @mixin et @include
- Etape 8 Possibilité d'inclure des fichiers externes avec @import

# Fonctionnalités implémentées
Nous avons réussi à réaliser toutes les fonctionnalités listées dans le point précédent. Ce chapitre présente les différentes fonctionnalités présentent dans notre compilateur dans l'ordre de leur implémentation.

## Parsing de css standard
Validation de la syntaxe de base d'un fichier scss, permet de valider la syntaxe basique d'un fichier css et de valider qu'il ne manque pas de point virgule ou de fermeture de parenthèses.

## Gestion du nesting
Le nesting permet d'imbriquer des sélecteurs css afin de représenter une hiérarchie de manière très simple ce que ne permet pas le css.

Voici un example de code scss:
```scss
nav {
  ul {
    margin: 0;
    list-style: none;
  }
  li { display: inline-block; }
  a {
    display: block;
    padding: 6px 12px;
  }
}

```

## Ajout de variables
Les variables scss se copmportent de la même manière que dans un language de programmation traditionnel. Elles permettent par exemple de changer une propriété couleur partout dans un projet. Les variables commencent par le symbole $ et voici un exemple de son utilisation.

```scss
$font-stack:    Helvetica, sans-serif;
$primary-color: #333;

body {
  font: 100% $font-stack;
  color: $primary-color;
}
```

## Branchements conditionnels
Les branchement conditionnels ou en d'autres thermes les "if", "else if", "else" et "while" permettent d'ajouter une dimension supplémentaire et de facilement adapter du code selon une ou plusieurs conditions.

Les branchements nécessitent l'évaluation d'une condition pour ce faire, les opérateurs de conditions suivants ont étés définis:
- ==
- !=
nous avons également ajouté les deux mots-clés "true" et "false" quipeuvent être combiné grâce aux opérateurs:
- or
- and
- not
Pour finir css défini déjà des type numérique par example "12px". Il est ainsi possible d'utiliser les comparateur numériques suivants:
- \>
- \>=
- <
- <=

Voici un example simple :

```scss
$other: single;

p {
  @if $other == single {
    color: blue;
  }
  @else if $other == double {
    color: red;
  }
  @else {
    color: green;
  }
}

$bool : true;
@if ($bool == true) or not (true != not false) {
  margin : 5px;
}
```

## Compilation des valeurs numériques
Le css standard ne permet pas de calcul numérique, nous avons ainsi remédier à ce manque ce qui permet de changer très facilement les proportions de certains éléments graphiques. Les opérateur numériques suivants oint étés implémentés:
- +
- -
- /
- \*

Voici un example:

```scss
$width : 500px;
nav {
  margin : 0 - 5px;
  padding : 2px / 4px + 5px;
  width: $width * 0.5;
}
```

## Système d'extend
Cette fonctionnalité est une des plus prisé de scss. Elle permet d'éviter le répétition de code et respecter le concept DRY.

TODO


```scss
%message-shared {
  border: 1px solid #ccc;
  padding: 10px;
  color: #333;
}

.message {
  @extend %message-shared;
}

.success {
  @extend %message-shared;
  border-color: green;
}

.error {
  @extend %message-shared;
  border-color: red;
}
```

Voici le code généré :
```scss
/* This CSS will print because %message-shared is extended. */
.message, .success, .error {
  border: 1px solid #ccc;
  padding: 10px;
  color: #333;
}

.success {
  border-color: green;
}

.error {
  border-color: red;
}
```

## Les mixin et include
TODO

## Composition de fichier scss
TODO import

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
