%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void yyerror(const char *s);
int yylex(void);

extern int yylineno;  // Adiciona essa linha
extern char *yytext;  // Adiciona essa linha

#ifndef YY_BUFFER_STATE
#define YY_BUFFER_STATE void*
#endif

extern YY_BUFFER_STATE yy_scan_string(const char *str);
extern void yy_delete_buffer(YY_BUFFER_STATE buffer);
%}

%union {
    char* str; // Use para armazenar strings
}

%left MENOR_QUE MAIOR_QUE MENOR_OU_IGUAL_A MAIOR_OU_IGUAL_A
%left IGUAL
%left MAIS MENOS
%left VEZES DIVIDIDO_POR

%token SELECIONAR_PESADA SELECIONAR_NORMAL SELECIONAR_RAPIDO ATIVAR_ENXAGUE_EXTRA ATIVAR_TURBO_PERFORMANCE NIVEL_AGUA_BAIXO NIVEL_AGUA_MEDIO NIVEL_AGUA_ALTO
%token <str> IDENTIFICADOR TEXTO NUMERO 
%token DEFINIR COMO SE ENTAO SENAO FIM ENQUANTO FACA IGUAL OU E NAO QUE MENOR_OU_IGUAL_A MAIOR_OU_IGUAL_A
%token LAVAR CENTRIFUGAR ENXAGUAR EXIBIR
%token PONTO_E_VIRGULA
%token <str> MAIS MENOS VEZES DIVIDIDO_POR
%token MAIOR_QUE MENOR_QUE


%type <str> expressao 

%%
programa
    : /* empty */
    | programa bloco
    ;

bloco
    : comando
    | declaracao
    | loop
    | condicional
    ;

declaracao
    : DEFINIR IDENTIFICADOR COMO expressao PONTO_E_VIRGULA // { printf("Definindo %s como %s.\n", $2, $4); free($4); }
    ;


comando
    : acao PONTO_E_VIRGULA
    | EXIBIR expressao PONTO_E_VIRGULA //{ printf("Exibindo: %s\n", $2); free($2); }
    ;

acao
    : LAVAR //{ printf("Lavando...\n"); }
    | CENTRIFUGAR //{ printf("Centrifugando...\n"); }
    | ENXAGUAR // { printf("Enxaguando...\n"); }
    | SELECIONAR_NORMAL
    | SELECIONAR_PESADA
    | SELECIONAR_RAPIDO
    | ATIVAR_ENXAGUE_EXTRA
    | ATIVAR_TURBO_PERFORMANCE
    | selecionar_nivel_agua
    ;

selecionar_nivel_agua
    : NIVEL_AGUA_BAIXO //{ printf("Nível de água baixo selecionado.\n"); }
    | NIVEL_AGUA_MEDIO //{ printf("Nível de água médio selecionado.\n"); }
    | NIVEL_AGUA_ALTO // { printf("Nível de água alto selecionado.\n"); }
    ;

expressao
    : expressao MAIS expressao %prec MAIS
    | expressao MENOS expressao %prec MENOS
    | expressao VEZES expressao %prec VEZES
    | expressao DIVIDIDO_POR expressao %prec DIVIDIDO_POR
    | expressao IGUAL expressao %prec IGUAL
    | expressao MAIOR_QUE expressao %prec MAIOR_QUE
    | expressao MENOR_QUE expressao %prec MENOR_QUE
    | expressao MAIOR_OU_IGUAL_A expressao %prec MAIOR_OU_IGUAL_A
    | expressao MENOR_OU_IGUAL_A expressao %prec MENOR_OU_IGUAL_A
    | IDENTIFICADOR
    | NUMERO
    | TEXTO
    ;

loop
    : ENQUANTO expressao FACA programa FIM PONTO_E_VIRGULA // { printf("Fim do loop.\n"); }
    ;

condicional
    : SE expressao ENTAO programa condicional_else FIM PONTO_E_VIRGULA // { printf("Fim da condição.\n"); }
    ;

condicional_else
    : /* empty */
    | SENAO programa
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro na linha %d: %s perto de '%s'\n", yylineno, s, yytext);
}

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            fprintf(stderr, "Não foi possível abrir o arquivo %s\n", argv[1]);
            return 1;
        }

        fseek(file, 0, SEEK_END);
        long fsize = ftell(file);
        fseek(file, 0, SEEK_SET);

        char *string = malloc(fsize + 1);
        fread(string, 1, fsize, file);
        fclose(file);

        string[fsize] = 0;
        YY_BUFFER_STATE bufferState = yy_scan_string(string);
        yyparse();
        yy_delete_buffer(bufferState);
        free(string);
    } else {
        fprintf(stderr, "Uso: %s <arquivo>\n", argv[0]);
        return 1;
    }
    return 0;
}
