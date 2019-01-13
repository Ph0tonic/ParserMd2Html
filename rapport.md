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


# Projet Sass compiler

## Autheurs

- [Lucas Bulloni](https://github.com/bull0n)
- [Wermeille Bastien](https://github.com/Ph0tonic/)

# Introduction

Dans le cadre du cours "Compilateurs", il nous a été demandé de réaliser un projet par équipe de deux en utilisant la bibliothèque python PLY. Le but de notre projet est de faire un compilateur SCSS. qui consiste à compiler SCSS en CSS.

Le langage source sera donc le SCSS et le langage cible CSS.

## Qu'est-ce que le SCSS

SCSS, pour Sassy CSS. Et Sassy, pour SASS qui était l'ancien nom de SCSS. SASS est l'acronyme de Syntactically Awesome Style Sheets. C'est un langage de qui permet de faire du CSS amélioré afin de faciliter le développement. Ce langage n'étant pas supporté par les navigateurs il faut le compiler en CSS.

# But fixé

Comme expliqué plus haut, le but fixé était de réaliser un compilateur permettant de compiler du code SCSS. Les étapes de réalisation ont été les suivantes :

- Etape 1 Validation de CSS Standard
- Etape 2 Ajout du nesting
- Etape 3 Mise en place des variables pour les propriétés
- Etape 4 Ajout de la gestion des branchements conditionnels tels que \@if, \@else if, \@else et \@while
- Etape 5 Ajout de la compilation des valeurs comportant des calculs
- Etape 6 Mise en place de l'héritage avec le mot clé \@extend
- Etape 7 Ajout des mixins et des include avec \@mixin et \@include
- Etape 8 Possibilités d'inclure des fichiers externes avec \@import
- Etape 9 Commentaires avec `//` et `/* */`

# Fonctionnalités implémentées

Nous avons réussi à réaliser toutes les fonctionnalités listées dans le point précédent. Ce chapitre présente les différentes fonctionnalités présentent dans notre compilateur dans l'ordre de leur implémentation.

## Parsing de CSS standard

Validation de la syntaxe de base d'un fichier SCSS, permet de valider la syntaxe basique d'un fichier CSS et de valider qu'il ne manque pas de point virgule ou de fermeture de parenthèses.

## Gestion du nesting

Le nesting permet d'imbriquer des sélecteurs CSS afin de représenter une hiérarchie de manière très simple ce que ne permet pas le CSS.

Voici un exemple de code SCSS:

```SCSS
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
padding: 12px;
}
```

Et voici la sortie qui sera générée:

```css
nav {
padding: 12px;
}
nav ul {
margin: 0;
list-style: none;
}
nav li { display: inline-block; }
nav a {
display: block;
padding: 6px 12px;
}
```

## Ajout de variables

Les variables SCSS se comportent de la même manière que dans un langage de programmation traditionnel. Elles permettent par exemple de changer une propriété couleur partout dans un projet. Les variables commencent par le symbole $ et voici un exemple de leurs utilisations.

Dans le cadre d'un framework scss il est très courant d'avoir en début de fichier une liste de variables permettant de configurer de nombreux paramètres pour la génération du fichier CSS. Un exemple typique est la couleur mais également la police ou encore les dimensions pour n'en citer que quelques-uns.


```scss
$font-stack: Helvetica, sans-serif;
$primary-color: #333;

body {
font: 100% $font-stack;
color: $primary-color;
}

div {
border-color: $primary-color;
}
```

Sortie:

```css
body {
font: 100% Helvetica, sans-serif;
color: #333;
}

div {
border-color: #333;
}
```

## Compilation des valeurs numériques

Le CSS standard ne permet pas de calcul numérique. Nous avons ainsi remédié à ce manque ce qui permet maintenant de changer très facilement les proportions de certains éléments graphiques. Les opérateurs numériques suivants ont été implémentés:

- +
- -
- /
- \*

Voici un exemple:

```SASS
$width : 500px;
nav {
margin : 0 - 5px;
padding : 2px / 4px + 5px;
width: $width * 0.5;
}
```

avec comme sortie:

```css
$width : 500px;
nav {
margin : -5px;
padding : 5.5px;
width: 250px;
}
```


## Branchements conditionnels

Les branchement conditionnels ou en d'autres thermes les mots clés "if", "else if", "else" et "while" permettent d'ajouter une dimension supplémentaire et de facilement adapter du code selon une ou plusieurs conditions.

Les branchements nécessitent l'évaluation d'une condition pour ce faire, les opérateurs de conditions suivants ont étés définis:
- ==
- !=
nous avons également ajouté les deux mots-clés "true" et "false" quipeuvent être combiné grâce aux opérateurs:
- or
- and
- not
Pour finir css défini déjà des type numérique par exemple "12px". Il est ainsi possible d'utiliser les comparateur numériques suivants:
- \>
- \>=
- <
- <=

### If, else if, else

Voici un exemple simple du if, else if et else :

```scss
$mode: SCREEN; // PRINT | SCREEN | BIG
$size: 12px;

p {
@if $mode == PRINT {
background-color: blue;
}
@else if $mode == SCREEN {
display: flex;
}
@else {
font-size; 50em;
}

// La priorité des opérateurs est respectée
$bool : false;
@if ($bool == true) or not (true != not false) { //true
margin : 5px;
}
}
```

Voici ce que produira le code précédent:

```css
p {
display: flex;
margin: 5px;
}
```

### While

Le while n'a pas beaucoup d'intérêt sans la possibilité d'effectuer des opérations numériques

## Système d'extend
Cette fonctionnalité est une des plus prisé de scss. Elle permet d'éviter le répétition de code et respecter le concept DRY.

Dans un code html concret on a souvent ce genre de code:
```html
<button class="btn btn-warning"/>
```

Grace à l'héritage on peut simplifier ce code de la manière suivante:
```html
<button class="btn-warning">
```

```scss
%btn {
border: 1px solid #ccc;
padding: 10px;
color: #333;
}

.btn-warning {
@extend %btn;
color: yellow;
}

.btn-success {
@extend %btn;
color: green;
}

```

Voici le code généré :
```scss
/* This CSS will print because %message-shared is extended. */
.btn-warning, .btn-success {
border: 1px solid #ccc;
padding: 10px;
color: #333;
}

.btn-warning {
color: yellow;
}

.btn-success {
color: green;
}
```

Le code devient ainsi plus simple à généraliser.

## Les mixin et include

Une mixin est l'équivalent d'une fonction mais en scss. Elle va permettre de ne pas recopier du code redondant.

Pour déclarer une mixin il faut utilisation l'annotation `@mixin` comme ceci :

```scss
@mixin transform($property) {
transform: $property;
}
```

On peut ensuite inclure ce code avec l'annotation `@include` comme ceci:

```scss
@include margin(hello, hello);
```

Et la compilation va se charcher de copier le code compilé de la mixins aux divers include. Voir exemple ci-dessous :

```scss
@mixin margin($side, $topbottom) {
margin: $topbottom $side;
}

.box {
display: block;
@include margin(3px, 12px);
}
```

**Code compilé** :

```scss
.box {
display : block;
margin : 12px 3px;
}
```

## Composition de fichier scss

En SCSS il est possible d'inclure un fichier dans un autre via `@import`. Pour cela il faut deux fichiers.

`file1.scss`

```SCSS
@import "file2";

body {
color: black;
}
```

`file2.scss`

```scss
p {
color: blue;
}
```

L'import va simplement copier le contenu du fichier file2 à la place de la déclaration `@import`. Et le résultat sera le suivant :

```css
p {
color : blue;
}

body {
color : black;
}
```

## Cas non gerés

Certains cas d'utilisation ne seront pas gerés par notre compilateur par manque des temps. Ces cas sont présentés ci-dessous

### Media query

```css
@media screen and (max-width: 992px) {
body {
background-color: blue;
}
}
```

Les media queries ressembles beaucoup à de la syntaxe SCSS mais sont du code CSS standart. Nous ne gérerons pas ce cas spécial.

### Valeurs sous-formes de fonctions

```scss
.box { @include transform(rotate(30deg)); }
```

En CSS, il est possible qu'une propriété soit sous-forme de fonction. Ci-dessus `rotate(30deg)`.

# Paramètres de mixins avec plusieurs "mots"

```scss
@include margin($hello, 12px 5px);
```

Il est possible en SCSS standard de passer à une mixins (explications plus tard dans le document) plusieurs mots comme paramètre.

# Prise en main
Ce document démontre une utilisation basique des différentes fonctionnalités du programme. Pour
une meilleure prise en main, n’oubliez pas de lire les exemples !

Pour générer un fichier css à l’aide de notre compilateur, il suffit d’exécuter la commande suivante :

```sh
python recCompiler.py CHEMIN_DU_FICHIER
```

# Guide utilisateur

## Bibliothèques requises

- Python3.6
- Ply
- yacc
- Graphviz
- Pydot

## Lexème

Afin de vérifier l'analyse lexicale, notre programme se lance comme tel :

```sh
python3 lex.py filename.scss
```

Cela va afficher les différents lexèmes reconnus par l'application

## Parsage

Il est possible de parser le document avec la commande

```bash
python3 paser.py filename.scss
```

Cela va générer un fichier PDF avec l'arbre. Ce fichier PDF se trouve dans le même dossier que le fichier parsé.

## Compilation

Il est possible de compiler un fichier avec cette commande :

```bash
python3 recCompiler.py filename.scss
```

Cela va générer un fichier CSS dans le dossier `compiled/`. Si ce dossier n'existe pas, il sera créé.

## Tester le compilateur

Il est possible de lancer tous les tests que nous avons réalisés en lançant le fichier tests.py

```bash
python3 tests.py
```

Ce script va ouvrir tous les fichiers SCSS dans le dossier `tests/` et les compiler

## Instalation des Bibliothèques

Notre compilateur ne requiert pas d'installation particulière autre que les Bibliothèques python spécifié ci-dessous.

Cette commande permet d'installer ces Bibliothèques sur un système Linux.

```bash
python3 -m pip install ply bison graphviz pydot
```

# Difficultés rencontrées

## Parsage

Le parsage nous a posé beaucoup de problèmes, car la structure des fichiers SCSS est relativement complexe.
Certains symboles tels que ">" peuvent avoir plusieurs rôles, en l'occurrence il peut représenter un sélecteur CSS , mais également un opérateur de comparaison de valeurs numériques.

Notre première version du parsec fonctionnait, mais de nombreux shift/reduce étaient présents et malgré plusieurs heures à tenter de les résoudre en analysant les fichiers "parser.out" et "parsetab.py". La seule solution a été de repartir de zéro ce qui nous a permis de mieux comprendre la fonction d'un parseur LALR notamment le système des précédences.

Une autre problématique que nous avons rencontrée concerne les strings, en effet celles-ci se trouvent à de nombreux endroits comme dans les sélecteurs CSS, mais également dans les propriétés et valeurs CSS. Celles-ci peuvent également être séparées par des virgules lors d'appels de fonctions ou dans les selectors. Une propriété CSS peut contenir une valeur, mais également une liste de valeurs telle que des valeurs numériques, des variables et des strings ou encore des expressions numériques.

Nous avons également valider que la déclaration d'une mixin soit possible avec le nombre de paramètres voulu et en incluant la simplification syntaxique telle:
```scss
@mixin transform() { ... }
@mixin empty { ... } //no parenthesis needed
@mixin margin($side, $topbottom) { ... }

@include transform; //no parenthesis needed
@include empty();
@include margin($test, 12px);
```

# Compilation

Pour la partie compilation, nous avons décidé de compiler de manière récursive afin de ne pas avoir à nous soucier de l'arbre cousu. Bien que notre projet soit un compilateur. Certaines fonctionnalités comme les opérations et les conditions n'étant pas supportées en CSS standard. Le compilateur va exécuter certaines parties de code comme un interpréteur.

Nous avons suivi la structure des TP du cours. Nous avons donc ajouter une fonction `compile(self)` à tous nous noeuds via le décorateur `addToClass(object)`. Les noeuds nécessitant une opération exécutée ont également une fonction `execute(self)`.

Pendant la compilation nous vérifions également que les mixins et variables soient bien déclarées avant utilisation et que les fichiers inclus existent.

# Améliorations

Notre compilateur possède quelques restrictions que nous n'avons pas corrigées par manque de temps.
- Media queries -> nous avons décidé de nous concentré sur les fonctionnalités de SCSS et avons mis de côté les media queries
- Fonctions CSS -> Il existe des fonctions CSS telles que "rgb, url, element" nous avons décidé de ne pas gérer ces cas, car il est nécessaire d'avoir un index de toutes ces fonctions existantes pour les implémenter.
- L'appel de mixin nécessite de spécifier le nombre exact de paramètres demandés. Il n'est actuellement pas possible de passer une liste de valeurs pour un paramètre. Cela est dû à notre implémentation de recCompiler voici un exemple de code problématique :

```scss
@include onparamfunction(25px 12px);
```

Le langage SCSS étant très vaste, nous avons uniquement implémenté les fonctionnalités principales. Voici quelques-unes des améliorations qu'il serait intéressant d'implémenter en plus de la suppression des limitations précédemment citées.
- Ajout du mot clé \@each
- Ajout du mot clé \@for
- Valeurs par défaut pour les paramètres d'une mixin
- Possibilité de concaténer des variables pour générer des noms de classes

# Conclusion

Ce projet nous a permis de mieux comprendre les concepts du cours de compilateur et de les mettre en pratique. Le déroulement du projet s'est plutôt bien passé et toutes les fonctionnalités que nous avions planifiées ont pu être implémentées.

Cependant, notre compilateur n'est pas parfait, ne gérant pas toutes les fonctionnalités SCSS. De plus nous ne sommes pas des experts CSS et nous ne pouvons garantir que tous les cas sauf ceux spécifiés fonctionnent.

Malgré cela nous sommes satisfaits du résultat final de notre travail.

# Annexes

## Code source

- Un fichier codesource.zip contenant l'application et ses tests
- dans ce fichier :
- un fichier README.md résumant comment utiliser notre application
- le code source

## Sass Documentation

- https://sass-lang.com/guide

