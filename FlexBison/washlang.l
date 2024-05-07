%{
#include "washlang.tab.h"  // Inclui o cabeçalho gerado pelo Bison
%}

%option noyywrap

/* Lista de Tokens */
%%
"definir"               { return DEFINIR; }
"como"                  { return COMO; }
"se"                    { return SE; }
"entao"                 { return ENTAO; }
"senao"                 { return SENAO; }
"fim"                   { return FIM; }
"enquanto"              { return ENQUANTO; }
"faca"                  { return FACA; }
"maior que"             { return MAIOR_QUE; }
"menor que"             { return MENOR_QUE; }
"que"                   { return QUE; }
"igual a"                 { return IGUAL; }
"maior ou igual a"      {return MAIOR_OU_IGUAL_A; }
"menor ou igual a"      {return MENOR_OU_IGUAL_A; }
"ou"                    { return OU; }
"e"                     { return E; }
"nao"                   { return NAO; }
"lavar"                 { return LAVAR; }
"centrifugar"           { return CENTRIFUGAR; }
"enxaguar"              { return ENXAGUAR; }
"exibir"                { return EXIBIR; }
";"                     { return PONTO_E_VIRGULA; }
"mais"                  { return MAIS; }
"menos"                 { return MENOS; }
"vezes"                 { return VEZES; }
"dividido por"          { return DIVIDIDO_POR; }
"selecionar programa de lavagem pesada"  { return SELECIONAR_PESADA; }
"selecionar programa de lavagem normal"  { return SELECIONAR_NORMAL; }
"selecionar programa de lavagem rápido"  { return SELECIONAR_RAPIDO; }
"ativar enxague extra"                  { return ATIVAR_ENXAGUE_EXTRA; }
"ativar turbo performance"              { return ATIVAR_TURBO_PERFORMANCE; }
"selecionar nivel de agua baixo"    { return NIVEL_AGUA_BAIXO; }
"selecionar nivel de agua medio"    { return NIVEL_AGUA_MEDIO; }
"selecionar nivel de agua alto"     { return NIVEL_AGUA_ALTO; }



[0-9]+                  { yylval.str = strdup(yytext); return NUMERO; }  // Números
\"[^"]*\"               { yylval.str = strdup(yytext); return TEXTO; }  // Texto entre aspas

[a-zA-Z_][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); return IDENTIFICADOR; }  // Identificadores

[ \t]+                  ;  // Ignora espaços e tabs
[\n\r]+                 { ++yylineno; }  // Conta as linhas

.                       { return yytext[0]; }  // Qualquer outro caractere é retornado como está

%%
