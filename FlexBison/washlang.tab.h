/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_WASHLANG_TAB_H_INCLUDED
# define YY_YY_WASHLANG_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    SELECIONAR_PESADA = 258,       /* SELECIONAR_PESADA  */
    SELECIONAR_NORMAL = 259,       /* SELECIONAR_NORMAL  */
    SELECIONAR_RAPIDO = 260,       /* SELECIONAR_RAPIDO  */
    ATIVAR_ENXAGUE_EXTRA = 261,    /* ATIVAR_ENXAGUE_EXTRA  */
    ATIVAR_TURBO_PERFORMANCE = 262, /* ATIVAR_TURBO_PERFORMANCE  */
    NIVEL_AGUA_BAIXO = 263,        /* NIVEL_AGUA_BAIXO  */
    NIVEL_AGUA_MEDIO = 264,        /* NIVEL_AGUA_MEDIO  */
    NIVEL_AGUA_ALTO = 265,         /* NIVEL_AGUA_ALTO  */
    IDENTIFICADOR = 266,           /* IDENTIFICADOR  */
    TEXTO = 267,                   /* TEXTO  */
    NUMERO = 268,                  /* NUMERO  */
    DEFINIR = 269,                 /* DEFINIR  */
    COMO = 270,                    /* COMO  */
    SE = 271,                      /* SE  */
    ENTAO = 272,                   /* ENTAO  */
    SENAO = 273,                   /* SENAO  */
    FIM = 274,                     /* FIM  */
    ENQUANTO = 275,                /* ENQUANTO  */
    FACA = 276,                    /* FACA  */
    IGUAL = 277,                   /* IGUAL  */
    OU = 278,                      /* OU  */
    E = 279,                       /* E  */
    NAO = 280,                     /* NAO  */
    QUE = 281,                     /* QUE  */
    MENOR_OU_IGUAL_A = 282,        /* MENOR_OU_IGUAL_A  */
    MAIOR_OU_IGUAL_A = 283,        /* MAIOR_OU_IGUAL_A  */
    LAVAR = 284,                   /* LAVAR  */
    CENTRIFUGAR = 285,             /* CENTRIFUGAR  */
    ENXAGUAR = 286,                /* ENXAGUAR  */
    EXIBIR = 287,                  /* EXIBIR  */
    PONTO_E_VIRGULA = 288,         /* PONTO_E_VIRGULA  */
    MAIS = 289,                    /* MAIS  */
    MENOS = 290,                   /* MENOS  */
    VEZES = 291,                   /* VEZES  */
    DIVIDIDO_POR = 292,            /* DIVIDIDO_POR  */
    MAIOR_QUE = 293,               /* MAIOR_QUE  */
    MENOR_QUE = 294                /* MENOR_QUE  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 19 "washlang.y"

    char* str; // Use para armazenar strings

#line 107 "washlang.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_WASHLANG_TAB_H_INCLUDED  */
