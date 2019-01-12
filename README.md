# Sass compiler

Here is a simple basic Sass compiler.

# Author

- [Lucas Bulloni](https://github.com/bull0n)
- [Wermeille Bastien](https://github.com/Ph0tonic/)

# Sass Documentation

- https://sass-lang.com/guide

# LEXEMES

- ADD_OP -> Opération + ou - arithmétique -> 2 + $salut
- MUL_OP -> Opération * ou / arithmétique -> 4 \* $salut
- NUMBER -> nombre avec ou sans une unité -> 5px, 5, 5cm
- SELECTOR -> un sélecteur HTML -> .salut, #salut, p
- SEPARATOR -> separateur de plusieurs element css -> '<', '>', ' ', ','
- VARIABLE -> Identifieur d'une variable -> $salut
- STRING_VALUE -> valeur css -> none, inherit


# PARSER

p // SELECTOR
{
  border-left: 1px solid left; // STR_VALUE : VALUE VALUE VALUE; -> RULE
} // STATEMENT

# INPUT / OUPUT

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

# Fonctionnalities to implement
- [x] Nested
- [x] @if / @elseif
- [x] @while
- [x] @mixin / @include
- [x] @extend
- [x] Operators
- [x] Variables
- [x] @import

# TODO :
- [ ] Create folder "compiled" in recCompiler.py