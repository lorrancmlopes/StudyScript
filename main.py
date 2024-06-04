import sys
import re

# Palavras reservadas
RESERVED_KEYWORDS = ['definir', 'como', 'lavar', 'centrifugar', 'enxaguar', 'ativar', 'enxague', 'extra', 
                     'turbo', 'performance', 'selecionar', 'programa',  'de', 'lavagem', 'pesada', 
                     'normal', 'rápido', 
                     'nivel', 'agua', 'baixo', 'medio', 'alto',
                     'enquanto', 'faca', 'fim', 'se', 'entao', 'senao', 'exibir',
                     'menos', 'mais', 'vezes', 'dividido', 'por', 'e', 'ou', 'igual', 'menor', 'maior', 'que' , 'a']
class PrePro:
    @staticmethod
    def filter(code):
        # Remove comentários e linhas em branco
        code = re.sub(r'\s*--.*', '', code)
        code = re.sub(r'\n\s*\n', '\n', code)
        # Remove espaços em branco no final de cada linha com rstrip()
        code = '\n'.join([line.rstrip() for line in code.split('\n')])
        #print(f"code: {code}")
        return code


class SymbolTable:
    def __init__(self):
        self.symbol_table = {}

    def create_entry(self, identifier):
        self.symbol_table[identifier] = (None, None)

    def set(self, identifier, value):  # value é uma tupla de valor e tipo
        created = False
        if identifier not in self.symbol_table:
            self.create_entry(identifier)
            created = True
        self.symbol_table[identifier] = value

    def get(self, identifier):
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]

class Node:
    i = 0

    def __init__(self, value=None):
        self.value = value
        self.children = []
        self.id = self.newId()
        # self.id = 4

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i

    def evaluate(self):
        pass


class Block(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            if child != None:
                #print(f"child: {child}")
                child.evaluate(symbol_table)

class Assignment(Node):
    def evaluate(self, symbol_table):
        identifier = self.children[0]
        value_node = self.children[1]  # Acessando o nó de valor
        # print(f"isinstance(value_node, IntVal): {isinstance(value_node, IntVal)}")
        if isinstance(value_node, IntVal):  # Verificando se o nó de valor é do tipo IntVal
            value = value_node.evaluate()  # Se for, apenas obtemos o valor
        # vamos ver se é uma string
        elif isinstance(value_node, String):
            value = value_node.evaluate()
        else:
            value = value_node.evaluate(symbol_table)  # Caso contrário, avaliamos a expressão
        if value is None:
            raise ValueError(f"Atribuição inválida para a variável '{identifier}'")
        symbol_table.set(identifier, value)


class BinOp(Node):
    def evaluate(self, symbol_table):
        left = self.children[0]
        right = self.children[1]
        if not isinstance(left, IntVal) and not isinstance(left, String):
            left = left.evaluate(symbol_table)

        if not isinstance(right, IntVal) and not isinstance(right, String):
            right = right.evaluate(symbol_table)

        if self.value in ['mais', 'menos', 'vezes', 'DIVIDIDO POR'] or self.value in ['or', 'and', 'IGUAL A', 'MENOR QUE', 'MAIOR QUE']:
            if self.value == 'mais':
                return IntVal((left.value[0] + right.value[0], 'INT'))
            elif self.value == 'menos':
                return IntVal((left.value[0] - right.value[0], 'INT'))
            elif self.value == 'vezes':
                return IntVal((left.value[0] * right.value[0], 'INT'))
            elif self.value == 'DIVIDIDO POR':
                if right.value[0] == 0:
                    return IntVal((0, 'INT'))
                return IntVal((left.value[0] // right.value[0], 'INT'))
            # adicionar operadores de comparação and, or, ==, <, >:
            elif self.value == 'or':
                if left.value[1] == 'INT' and right.value[1] == 'INT':
                    if left.value[0] or right.value[0]:
                        return IntVal((1, 'INT'))
                    return IntVal((0, 'INT'))
                raise TypeError("Operação não suportada para os valores tipos fornecidos")
            elif self.value == 'and':
                if left.value[1] == 'INT' and right.value[1] == 'INT':
                    if left.value[0] and right.value[0]:
                        return IntVal((1, 'INT'))
                    return IntVal((0, 'INT'))
                raise TypeError("Operação não suportada para os valores tipos fornecidos")
            elif self.value == 'IGUAL A':
                if isinstance(left, str):
                    left = String((left, 'STRING'))
                if isinstance(right, str):
                    right = String((right, 'STRING'))
                if left.value[0] == right.value[0]:
                    return IntVal((1, 'INT'))
                return IntVal((0, 'INT'))

            elif self.value == 'MENOR QUE':
                if left.value[1] == 'INT' and right.value[1] == 'INT':
                    if left.value[0] < right.value[0]:
                        return IntVal((1, 'INT'))
                    return IntVal((0, 'INT'))
                elif isinstance(left, tuple) and isinstance(right, tuple):
                    if isinstance(left[0], str) and isinstance(right[0], str):
                        if left[0] < right[0]:
                            return IntVal((1, 'INT'))
                        return IntVal((0, 'INT'))
                    if left[0].value[0] < right[0].value[0]:
                        return IntVal((1, 'INT'))
                    return IntVal((0, 'INT'))
            elif self.value == 'MAIOR QUE':
                # print(f"self.value: {self.value}")
                if left.value[1] == 'INT' and right.value[1] == 'INT':
                    if left.value[0] > right.value[0]:
                        return IntVal((1, 'INT'))
                    return IntVal((0, 'INT'))
                elif isinstance(left, tuple) and isinstance(right, tuple):
                    if isinstance(left[0], str) and isinstance(right[0], str):
                        if left[0] > right[0]:
                            return IntVal((1, 'INT'))
                        return IntVal((0, 'INT'))
                    if left[0].value[0] > right[0].value[0]:
                        return IntVal((1, 'INT'))
                    return IntVal((0, 'INT'))
        else:
            raise TypeError("Operação não suportada para os valores fornecidos: ", left.value, right.value)

class IntVal(Node):
    def evaluate(self):
        return IntVal(self.value)

class Identifier(Node):
    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)

class String(Node):
    def evaluate(self):
        return self.value

class NoOp(Node):
    def evaluate(self):
        pass

class VarDec(Node):
    def evaluate(self, symbol_table):
        return

class Print(Node):
    def evaluate(self, symbol_table):
        # avalia se children[0] é um IntVal ou uma expressão
        if isinstance(self.children[0], IntVal) or isinstance(self.children[0], String):
            print(self.children[0].evaluate()[0])
        else:
            # print("Else")
            # checar se é binOp. Se for, avaliar
            if isinstance(self.children[0], BinOp):
                print(self.children[0].evaluate(symbol_table).value[0])
                return
            print(self.children[0].evaluate(symbol_table).value[0])


class While(Node):
    def evaluate(self, symbol_table):
        # Introduzir o filho 0 (condição) e retornar o resultado em EBX
        # Instruções do filho 1 (bloco de comandos)
        while self.children[0].evaluate(symbol_table).value[0]:  # reavalia a condição em cada iteração
            self.children[1].evaluate(symbol_table)


class If(Node):
    def evaluate(self, symbol_table):
        expression = self.children[0]  # condição do if
        block = self.children[1]  # bloco de comandos
        # verifica o len do nó, se for 3, tem um else
        if len(self.children) == 3:
            block_else = self.children[2]  # bloco de comandos do else
            if expression.evaluate(symbol_table).value[0]:
                block.evaluate(symbol_table)
            else:
                block_else.evaluate(symbol_table)
        else:
            if expression.evaluate(symbol_table).value[0]:
                block.evaluate(symbol_table)

class Lavar(Node):
    def evaluate(self, symbol_table):
        programa_de_lavagem = symbol_table.get('programa_de_lavagem')
        if programa_de_lavagem is None:
            raise ValueError("Programa de lavagem não definido")
        nivel_de_agua = symbol_table.get('nivel_de_agua')
        if nivel_de_agua is None:
            raise ValueError("Nível de água não definido")
        if programa_de_lavagem == 'rapido':
            print("Lavando rápido...")
        elif programa_de_lavagem == 'normal':
            print("Lavando normal...")
            print("Lavando normal...")
        elif programa_de_lavagem == 'pesada':
            print("Lavando pesado...")
            print("Lavando pesado...")
            print("Lavando pesado...")

class Enxaguar(Node):
    def evaluate(self, symbol_table):
        nivel_de_agua = symbol_table.get('nivel_de_agua')
        if nivel_de_agua is None:
            raise ValueError("Nível de água não definido")
        print("Enxaguando...")
        if symbol_table.get('enxague_extra'):
            print("Enxaguando com enxague extra...")
        

class Centrifugar(Node):
    def evaluate(self, symbol_table):
        print("Centrifugando...")

class NivelDeAgua(Node):
    def evaluate(self, symbol_table):
        print(f"Nível de água: {self.value}")
        symbol_table.set('nivel_de_agua', self.value)

class ProgramaDeLavagem(Node):
    def evaluate(self, symbol_table):
        print(f"Programa de lavagem: {self.value}")
        symbol_table.set('programa_de_lavagem', self.value)

class EnxagueExtra(Node):
    def evaluate(self, symbol_table):
        nivel_de_agua = symbol_table.get('nivel_de_agua')
        if nivel_de_agua is None:
            raise ValueError("Nível de água não definido")
        symbol_table.set('enxague_extra', True)
        print("Enxague extra: ativado")

class TurboPerformance(Node):
    def evaluate(self, symbol_table):
        print("Turbo performance: ativado")

class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source: str):
        self.source = PrePro.filter(source)
        self.position = 0
        self.current_char = self.source[self.position] if self.position < len(self.source) else None

    def advance(self):
        self.position += 1
        if self.position < len(self.source):
            self.current_char = self.source[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result), 'INT'

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char == '\n':
                self.advance()
                return Token('NEWLINE', '\n')

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token('INT', self.integer())

            if self.current_char == '"':
                self.advance()
                result = ''
                while self.current_char != '"':
                    result += self.current_char
                    self.advance()
                self.advance()
                return Token('STRING', result)
            
            # adicionar ;
            if self.current_char == ';':
                self.advance()
                return Token('SEMICOLON', ';')

            # Verificar o caso de ser um identificador de variável (começa com letra e contém letras e números)
            if self.current_char.isalpha():
                identifier = ''
                while self.current_char is not None and self.current_char.isalnum() or self.current_char == "_":
                    identifier += self.current_char
                    self.advance()
                if identifier in RESERVED_KEYWORDS:
                    # Se for um print, desvia
                    if identifier == 'definir':
                        return Token('DEFINIR', 'definir')
                    # checando para os novos elementos da lista de palavras reservadas
                    elif identifier == 'como':
                        return Token('COMO', 'como')
                    elif identifier == 'lavar':
                        return Token('LAVAR', 'lavar')
                    elif identifier == 'centrifugar':
                        return Token('CENTRIFUGAR', 'centrifugar')
                    elif identifier == 'enxaguar':
                        return Token('ENXAGUAR', 'enxaguar')
                    elif identifier == 'ativar':
                        return Token('ATIVAR', 'ativar')
                    elif identifier == 'enxague':
                        return Token('ENXAGUE', 'enxague')
                    elif identifier == 'extra':
                        return Token('EXTRA', 'extra')
                    elif identifier == 'turbo':
                        return Token('TURBO', 'turbo')
                    elif identifier == 'performance':
                        return Token('PERFORMANCE', 'performance')
                    elif identifier == 'selecionar':
                        return Token('SELECIONAR', 'selecionar')
                    elif identifier == 'programa':
                        return Token('PROGRAMA', 'programa')
                    elif identifier == 'de':
                        return Token('DE', 'de')
                    elif identifier == 'lavagem':
                        return Token('LAVAGEM', 'lavagem')
                    elif identifier == 'pesada':
                        return Token('PESADA', 'pesada')
                    elif identifier == 'normal':
                        return Token('NORMAL', 'normal')
                    elif identifier == 'rápido':
                        return Token('RÁPIDO', 'rápido')
                    elif identifier == 'nivel':
                        return Token('NIVEL', 'nivel')
                    elif identifier == 'agua':
                        return Token('AGUA', 'agua')
                    elif identifier == 'baixo':
                        return Token('BAIXO', 'baixo')
                    elif identifier == 'medio':
                        return Token('MEDIO', 'medio')
                    elif identifier == 'alto':
                        return Token('ALTO', 'alto')
                    elif identifier == 'enquanto':
                        return Token('ENQUANTO', 'enquanto')
                    elif identifier == 'faca':
                        return Token('FACA', 'faca')
                    elif identifier == 'fim':
                        return Token('FIM', 'fim')
                    elif identifier == 'se':
                        return Token('SE', 'se')
                    elif identifier == 'entao':
                        return Token('ENTAO', 'entao')
                    elif identifier == 'senao':
                        return Token('SENAO', 'senao')
                    elif identifier == 'exibir':
                        return Token('EXIBIR', 'exibir')
                    elif identifier == 'menos':
                        return Token('MENOS', 'menos')
                    elif identifier == 'mais':
                        return Token('MAIS', 'mais')
                    elif identifier == 'vezes':
                        return Token('VEZES', 'vezes')
                    elif identifier == 'dividido':
                        return Token('DIVIDIDO', 'dividido')
                    elif identifier == 'por':
                        return Token('POR', 'por')
                    elif identifier == 'e':
                        return Token('AND', 'and')
                    elif identifier == 'ou':
                        return Token('OR', 'or')
                    elif identifier == 'igual':
                        return Token('IGUAL', 'igual')
                    elif identifier == 'menor':
                        return Token('MENOR', 'menor')
                    elif identifier == 'maior':
                        return Token('MAIOR', 'maior')
                    elif identifier == 'a':
                        return Token('A', 'a')
                    elif identifier =='que':
                        return Token('QUE', 'que')
                    elif identifier == 'por':
                        return Token('POR', 'por')
                return Token('IDENTIFIER', identifier)
            # Se não corresponder a nenhum dos tipos de token conhecidos, levanta um erro
            raise SyntaxError("Caractere inválido encontrado: {}".format(self.current_char))
        return Token('EOF', '')

    def selectNext(self):
        token = self.get_next_token()
        self.next = token
        return token

class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.symbol_table = SymbolTable

    @staticmethod
    def parseBlock():  # resolve cada linha, que é um Statement
        token = Parser.tokenizer.selectNext()
        # cria o nó de bloco
        block_node = Block()
        # tabela de símbolos
        Parser.symbol_table = SymbolTable()
        while token.type != 'EOF':
            statement = Parser.parseStatement(token)
            block_node.children.append(statement)
            token = Parser.tokenizer.selectNext()
        block_node.evaluate(Parser.symbol_table)

    @staticmethod
    def parseStatement(token):
        # Se o token for um /n, não faz nada
        if token.type == 'NEWLINE':
            return
        # Criação de variável e atribuição
        elif token.type == 'DEFINIR':
            token = Parser.tokenizer.selectNext()
            if token.type == 'IDENTIFIER':
                identifier = token.value
                token = Parser.tokenizer.selectNext()
                # verifica se a variável já foi declarada checandop se o get é uma tupla
                if isinstance(Parser.symbol_table.get(identifier), tuple):
                    raise NameError(f"Variável '{identifier}' já declarada!!")
                # verifica se já faz assign na criação
                if token.type == 'COMO':
                    expression, next_token = Parser.parseBooleanExpression()
                    #Verifica se o próximo é um ;
                    if next_token.type != 'SEMICOLON':
                        raise SyntaxError(f"Erro: Esperado ';', encontrado '{next_token.value}'")
                    next_token = Parser.tokenizer.selectNext()
                    # Verifica se o próximo token é um /n, se não for, levanta um erro
                    if next_token.type != 'NEWLINE':
                        raise SyntaxError(f"Erro: Esperado fim de linha, encontrado '{next_token.value}'")
                    assignment_node = Assignment()
                    assignment_node.value = token.value
                    assignment_node.children.append(identifier)
                    assignment_node.children.append(expression)
                    #if isFunction is False:
                    Parser.symbol_table.set(identifier, expression)
                    return assignment_node
                else:
                    raise SyntaxError("Erro: Esperado símbolo de atribuição 'como' após identificador.")
        # Se o token for um print, verifica se tem um (, expressao e um ). Se sim, cria um nó de print
        elif token.type == 'EXIBIR':
            expression, token = Parser.parseBooleanExpression()
            if token.type == 'SEMICOLON':
                print_node = Print()
                print_node.value = "print"
                print_node.children.append(expression)
                return print_node
            else:
                print(token.type)
                raise SyntaxError("Erro: esperado ';' após expressão de exibição")
        #adiconar o caso "selecionar"
        elif token.type == 'SELECIONAR':
            #pode ser seleção de programa de lavagem (rápido, normal, pesada) ou nível de água (baixo, médio, alto)
            token = Parser.tokenizer.selectNext()
            if token.type == 'PROGRAMA':
                token = Parser.tokenizer.selectNext()
                if token.type == 'DE':
                    token = Parser.tokenizer.selectNext()
                    if token.type == 'LAVAGEM':
                        token = Parser.tokenizer.selectNext()
                        if token.type == 'RÁPIDO':
                            token = Parser.tokenizer.selectNext()
                            if token.type == 'SEMICOLON':
                                programa_node = ProgramaDeLavagem()
                                programa_node.value = "rapido"
                                return programa_node
                            else:
                                raise SyntaxError("Erro: esperado ';' após seleção de programa de lavagem")
                        elif token.type == 'NORMAL':
                            token = Parser.tokenizer.selectNext()
                            if token.type == 'SEMICOLON':
                                programa_node = ProgramaDeLavagem()
                                programa_node.value = "normal"
                                return programa_node
                            else:
                                raise SyntaxError("Erro: esperado ';' após seleção de programa de lavagem")
                        elif token.type == 'PESADA':
                            token = Parser.tokenizer.selectNext()
                            if token.type == 'SEMICOLON':
                                programa_node = ProgramaDeLavagem()
                                programa_node.value = "pesada"
                                return programa_node
                            else:
                                raise SyntaxError("Erro: esperado ';' após seleção de programa de lavagem")
                        else:  
                            raise SyntaxError("Erro: programa de lavagem inválido")
                    else:
                        raise SyntaxError("Erro: esperado 'lavagem' após 'de'")
                else:
                    raise SyntaxError("Erro: esperado 'de' após 'programa'")
            elif token.type == 'NIVEL':
                token = Parser.tokenizer.selectNext()
                if token.type == 'DE':
                    token = Parser.tokenizer.selectNext()
                    if token.type == 'AGUA':
                        token = Parser.tokenizer.selectNext()
                        if token.type == 'BAIXO':
                            token = Parser.tokenizer.selectNext()
                            if token.type == 'SEMICOLON':
                                nivel_node = NivelDeAgua()
                                nivel_node.value = "baixo"
                                return nivel_node
                            else:
                                raise SyntaxError("Erro: esperado ';' após seleção de nível de água")
                        elif token.type == 'MEDIO':
                            token = Parser.tokenizer.selectNext()
                            if token.type == 'SEMICOLON':
                                nivel_node = NivelDeAgua()
                                nivel_node.value = "medio"
                                return nivel_node
                            else:
                                raise SyntaxError("Erro: esperado ';' após seleção de nível de água")
                        elif token.type == 'ALTO':
                            token = Parser.tokenizer.selectNext()
                            if token.type == 'SEMICOLON':
                                nivel_node = NivelDeAgua()
                                nivel_node.value = "alto"
                                return nivel_node
                            else:
                                raise SyntaxError("Erro: esperado ';' após seleção de nível de água")
                        else:  
                            raise SyntaxError("Erro: nível de água inválido")
                    else:
                        raise SyntaxError("Erro: esperado 'agua' após 'de'")
                else:
                    raise SyntaxError("Erro: esperado 'de' após 'nivel'")
            else:
                raise SyntaxError("Erro: esperado 'programa' ou 'nivel' após 'selecionar'")

        elif token.type == 'ATIVAR':
            token = Parser.tokenizer.selectNext()
            if token.type == 'ENXAGUE':
                token = Parser.tokenizer.selectNext()
                if token.type == 'EXTRA':
                    token = Parser.tokenizer.selectNext()
                    if token.type == 'SEMICOLON':
                        enxague_node = EnxagueExtra()
                        token = Parser.tokenizer.selectNext()
                        if token.type != 'NEWLINE':
                            raise SyntaxError("Erro: esperado quebra de linha após ativação de enxague extra")
                        return enxague_node
                    else:
                        raise SyntaxError("Erro: esperado ';' após ativação de enxague extra")
                else:
                    raise SyntaxError("Erro: esperado 'extra' após 'enxague'")
            elif token.type == 'TURBO':
                token = Parser.tokenizer.selectNext()
                if token.type == 'PERFORMANCE':
                    token = Parser.tokenizer.selectNext()
                    if token.type == 'SEMICOLON':
                        turbo_node = TurboPerformance()
                        token = Parser.tokenizer.selectNext()
                        if token.type != 'NEWLINE':
                            raise SyntaxError("Erro: esperado quebra de linha após ativação de turbo performance")
                        return turbo_node
                    else:
                        raise SyntaxError("Erro: esperado ';' após ativação de turbo performance")
                else:
                    raise SyntaxError("Erro: esperado 'performance' após 'turbo'")
            else:
                raise SyntaxError(f"Erro: esperado 'enxague' ou 'turbo' após 'ativar'. Encontrado: {token.type}, {token.value}")
        elif token.type == 'ENQUANTO':  # precisa ser WHILE, BooleanExpression, DO, \n, Statement até achar um END. Se não achar end, levanta um erro
            expression, token = Parser.parseBooleanExpression()
            if token.type == 'FACA':
                # verificar se o próximo token é um \n
                token = Parser.tokenizer.selectNext()
                if token.type == 'NEWLINE':
                    block_node = Block()
                    token = Parser.tokenizer.selectNext()
                    while token.type != 'FIM':
                        # verifica se o token é um EOF e lança um erro
                        if token.type == 'EOF':
                            raise SyntaxError("Erro: Esperado 'fim' ao usar loop 'enquanto/faca'")
                        statement = Parser.parseStatement(token)
                        block_node.children.append(statement)
                        token = Parser.tokenizer.selectNext()
                    #verifica se não tem ; depois do fim (pega o proximo e checa)
                    token = Parser.tokenizer.selectNext()
                    if token.type != 'SEMICOLON':
                        raise SyntaxError("Erro: Esperado ';' após 'fim'")
                    while_node = While()
                    while_node.children.append(expression)
                    while_node.children.append(block_node)
                    return while_node
                else:
                    raise SyntaxError("Erro: Esperado '\n' após faca")
            # adicionar erro se não tiver o faca
            else:
                raise SyntaxError("Erro: Esperado 'faca' após a expressão booleana")
        elif token.type == 'SE':
            tem_else = False
            expression, token = Parser.parseBooleanExpression()
            if token.type == 'ENTAO':
                # verificar se o próximo token é um \n
                token = Parser.tokenizer.selectNext()
                if token.type == 'NEWLINE':
                    block_node = Block()
                    token = Parser.tokenizer.selectNext()
                    # não precisa ter um else, mas precisa ter um end pois é lua
                    while token.type != 'FIM':
                        # verifica se o token é um EOF e lança um erro
                        if token.type == 'EOF':
                            raise SyntaxError("Erro: Esperado 'fim' ao usar se/entao")
                        # se o token.type já for ELSE, o IF não tem bloco de comandos
                        if token.type == 'SENAO':
                            tem_else = True
                            token = Parser.tokenizer.selectNext()
                            if token.type == 'NEWLINE':
                                block_node_else = Block()
                                token = Parser.tokenizer.selectNext()
                                while token.type != 'FIM':
                                    statement = Parser.parseStatement(token)
                                    block_node_else.children.append(statement)
                                    token = Parser.tokenizer.selectNext()
                                if token.type == 'FIM':
                                    #pega o próximo token e verifica se é semi-colon
                                    token = Parser.tokenizer.selectNext()
                                    if token.type != 'SEMICOLON':
                                        raise SyntaxError("Erro: Esperado ';' após 'fim'")
                                    if_node = If()
                                    if_node.children.append(expression)
                                    if_node.children.append(block_node)
                                    # se tiver else, adiciona o bloco de comandos do else
                                    if tem_else:
                                        if_node.children.append(block_node_else)
                                    # verifica se o próximo token é um \n
                                    token = Parser.tokenizer.selectNext()
                                    if token.type == 'NEWLINE':
                                        return if_node
                                    else:
                                        raise SyntaxError("Erro: Esperado quebra de linha após ';'")
                            else:
                                raise SyntaxError("Erro: Esperado '\n' após SENAO")
                        statement = Parser.parseStatement(token)
                        token = Parser.tokenizer.selectNext()
                        block_node.children.append(statement)
                        if token.type == 'SENAO':
                            tem_else = True
                            token = Parser.tokenizer.selectNext()
                            if token.type == 'NEWLINE':
                                block_node_else = Block()
                                token = Parser.tokenizer.selectNext()
                                while token.type != 'FIM':
                                    statement = Parser.parseStatement(token)
                                    block_node_else.children.append(statement)
                                    token = Parser.tokenizer.selectNext()
                                break
                            else:
                                raise SyntaxError("Erro: Esperado '\n' após ELSE")
                    if token.type == 'FIM':
                        if_node = If()
                        if_node.children.append(expression)
                        if_node.children.append(block_node)
                        # se tiver else, adiciona o bloco de comandos do else
                        if tem_else:
                            if_node.children.append(block_node_else)
                        # verifica se o próximo token é um \n
                        token = Parser.tokenizer.selectNext()
                        #verifica se não tem ; depois do fim (pega o proximo e checa)
                        if token.type != 'SEMICOLON':
                            raise SyntaxError("Erro: Esperado ';' após 'fim'")
                        token = Parser.tokenizer.selectNext()
                        if token.type == 'NEWLINE':
                            return if_node
                        else:
                            raise SyntaxError("Erro: Esperado quebra de linha após FIM")
        elif token.type == 'LAVAR':
            token = Parser.tokenizer.selectNext()
            #verifica se o próximo token é um ; 
            if token.type == 'SEMICOLON':
                lavar_node = Lavar()
                #verifica se o próximo token é um \n
                token = Parser.tokenizer.selectNext()
                if token.type == 'NEWLINE':
                    return lavar_node
                else:
                    raise SyntaxError("Erro: Esperado quebra de linha após ';'")
            else:
                raise SyntaxError("Erro: Esperado ';' após 'lavar'")
        
        elif token.type == 'ENXAGUAR':
            token = Parser.tokenizer.selectNext()
            #verifica se o próximo token é um ; 
            if token.type == 'SEMICOLON':
                enxaguar_node = Enxaguar()
                #verifica se o próximo token é um \n
                token = Parser.tokenizer.selectNext()
                if token.type == 'NEWLINE':
                    return enxaguar_node
                else:
                    raise SyntaxError("Erro: Esperado quebra de linha após ';'")
            else:
                raise SyntaxError("Erro: Esperado ';' após 'enxaguar'")
        
        elif token.type == 'CENTRIFUGAR':
            token = Parser.tokenizer.selectNext()
            #verifica se o próximo token é um ; 
            if token.type == 'SEMICOLON':
                centrifugar_node = Centrifugar()
                #verifica se o próximo token é um \n
                token = Parser.tokenizer.selectNext()
                if token.type == 'NEWLINE':
                    return centrifugar_node
                else:
                    raise SyntaxError("Erro: Esperado quebra de linha após ';'")
            else:
                raise SyntaxError("Erro: Esperado ';' após 'centrifugar'")
        else:
            raise SyntaxError(
                f"Erro: Comando inválido: {token.value}.")  # \n O código de entrada foi:\n {Parser.tokenizer.source}")

    @staticmethod
    def parseExpression():
        result_expression, token = Parser.parseTerm()
        while token.type in ["MENOS", "MAIS"]:
            op = token.value
            result_term, token = Parser.parseTerm()
            bin_op_node = BinOp(op)
            bin_op_node.children.append(result_expression)
            bin_op_node.children.append(result_term)
            result_expression = bin_op_node
        return result_expression, token

    # criando o método RelationalExpression, que é uma expressão que pode conter operadores de comparação ==, <, >
    @staticmethod
    def parseRelationalExpression():
        result_expression, token = Parser.parseExpression()
        while token.type in ['MAIOR', 'MENOR', 'IGUAL']:
            if token.type == 'MAIOR':
                token = Parser.tokenizer.selectNext()
                if token.type == 'QUE':
                    result_term, token = Parser.parseExpression()
                    bin_op_node = BinOp('MAIOR QUE')
                    bin_op_node.children.append(result_expression)
                    bin_op_node.children.append(result_term)
                    result_expression = bin_op_node
                elif token.type == 'OU':
                    token = Parser.tokenizer.selectNext()
                    if token.type == 'IGUAL':
                        result_term, token = Parser.parseExpression()
                        bin_op_node = BinOp('MAIOR OU IGUAL')
                        bin_op_node.children.append(result_expression)
                        bin_op_node.children.append(result_term)
                        result_expression = bin_op_node
            elif token.type == 'MENOR':
                token = Parser.tokenizer.selectNext()
                if token.type == 'QUE':
                    result_term, token = Parser.parseExpression()
                    bin_op_node = BinOp('MENOR QUE')
                    bin_op_node.children.append(result_expression)
                    bin_op_node.children.append(result_term)
                    result_expression = bin_op_node
                elif token.type == 'OU':
                    token = Parser.tokenizer.selectNext()
                    if token.type == 'IGUAL':
                        result_term, token = Parser.parseExpression()
                        bin_op_node = BinOp('MENOR OU IGUAL')
                        bin_op_node.children.append(result_expression)
                        bin_op_node.children.append(result_term)
                        result_expression = bin_op_node
            elif token.type == 'IGUAL':
                token = Parser.tokenizer.selectNext()
                if token.type == 'A':
                    result_term, token = Parser.parseExpression()
                    bin_op_node = BinOp('IGUAL A')
                    bin_op_node.children.append(result_expression)
                    bin_op_node.children.append(result_term)
                    result_expression = bin_op_node
        return result_expression, token

    # criando o método BooleanTerm, que é uma expressão que pode conter o operator 'and'.
    @staticmethod
    def parseBooleanTerm():
        result_expression, token = Parser.parseRelationalExpression()
        while token.type == "AND":
            op = token.value
            result_term, token = Parser.parseRelationalExpression()
            bin_op_node = BinOp(op)
            bin_op_node.children.append(result_expression)
            bin_op_node.children.append(result_term)
            result_expression = bin_op_node
        return result_expression, token

    # criando o método BooleanExpression, que é uma expressão que pode conter o operator 'or'.
    @staticmethod
    def parseBooleanExpression():
        result_expression, token = Parser.parseBooleanTerm()
        while token.type == "OR":
            op = token.value
            result_term, token = Parser.parseBooleanTerm()
            bin_op_node = BinOp(op)
            bin_op_node.children.append(result_expression)
            bin_op_node.children.append(result_term)
            result_expression = bin_op_node
        return result_expression, token

    @staticmethod
    def parseTerm():
        result_term, token = Parser.parseFactor()
        while token.type in ["VEZES", "DIVIDIDO"]:
            if token.value == 'dividido':
                token = Parser.tokenizer.selectNext()
                if token.type == 'POR':
                    op = 'DIVIDIDO POR'
            else:
                op = token.value
            result_factor, token = Parser.parseFactor()
            bin_op_node = BinOp(op)
            bin_op_node.children.append(result_term)
            bin_op_node.children.append(result_factor)
            result_term = bin_op_node
        return result_term, token

    @staticmethod
    def parseFactor():
        token = Parser.tokenizer.selectNext()
        if token.type == 'INT':
            return IntVal(token.value), Parser.tokenizer.selectNext()
        elif token.type == 'STRING':
            return String((token.value, 'STRING')), Parser.tokenizer.selectNext()
        elif token.type == 'IDENTIFIER':
            identificador = token.value
            token = Parser.tokenizer.selectNext()
            return Identifier(identificador), token
        else:
            raise SyntaxError(f"Erro: Token inesperado: {token.value}")

    @staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.parseBlock()

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        code = file.read()
        #raise TypeError(f"code: {code}")
    try:
        Parser.run(code)
    except Exception as e:
        print(f"Ocorreu um erro durante a execução: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()