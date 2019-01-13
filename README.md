# Sass compiler

Here is a simple basic Sass compiler.

# Author

- [Lucas Bulloni](https://github.com/bull0n)
- [Wermeille Bastien](https://github.com/Ph0tonic/)

# Sass Documentation

- https://sass-lang.com/guide

# Download

git clone https://github.com/Ph0tonic/SassCompiler.git
cd SassCompiler

# Requirements

- Python3.6
- Ply
- Graphviz
- Pydot
- yacc

# To run our project

## Lex

To run lex, run the following command and specify an scss file.

```bash
python3 lex.py filename.scss
```

In the same folder a new text file was created : filename.txt. This file contains the corresponding lexems.

## Parser

To run parser, run the following command and specify an scss file.

```bash
python3 paser.py filename.scss
```

In the same folder a new pdf file was created : filename-ast.pdf. This file contains the AST tree.

## Compiler

```bash
python3 recCompiler.py filename.scss
```

In the folder *"generated"* a new css file has been created : filename.css. This file contains the compiled scss of input code.

## Tests

We've created a bunch of basic scss file for our tests in the folder "tests". We although made a script to compile all of them. To run those tests.

```bash
python3 tests.py
```

This script will generate all files located in the folder "tests" into the folder "generated".

# INPUT / OUPUT example

```scss
nav {
  ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  li { display: inline-block; }

  a {
    display: block;
    padding: 6px 12px;
    text-decoration: none;
  }
}```

```css
nav ul {
  margin: 0;
  padding: 0;
  list-style: none;
}
nav li {
  display: inline-block;
}
nav a {
  display: block;
  padding: 6px 12px;
  text-decoration: none;
}
```

# Fonctionnalities implemented

- [x] Nested
- [x] @if / @elseif
- [x] @while
- [x] @mixin / @include
- [x] @extend
- [x] Operators
- [x] Variables
- [x] @import

# TODO :
- [ ] Améliorer le graph afin d'afficher plus d'informations sur certains noeuds.