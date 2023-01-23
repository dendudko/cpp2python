import copy

from Translator.Constants.constants import *


class CodeGenerator:
    def __init__(self):
        self.tokens = []
        self.errors_syntax = []
        self.errors_semantic = []
        self.current_token_index = 0
        self.tabs_count = 1
        self.output = []

    # Расстановка табуляции и новой строки
    def tabs(self):
        if not self.output[-1] == "):\n":
            self.output.append("\n")
        for i in range(self.tabs_count):
            self.output.append("\t")

    # Переход к следующему токену
    def advance_token(self):
        if self.current_token_index < (len(self.tokens) - 1):
            self.current_token_index += 1

    # Проверка равенства токенов
    def token_is(self, token_to_match):
        if self.tokens[self.current_token_index].lexeme == token_to_match:
            self.advance_token()
            return True
        else:
            return False

    # Проверка на вхождение токена в группу
    def token_in(self, token_list):
        if len(token_list) == 1:
            return self.token_is(token_list[0])
        else:
            if self.tokens[self.current_token_index].lexeme in token_list:
                self.advance_token()
                return True
            else:
                return False

    # Проверка на вхождение в список переданных типов токенов
    def is_current_token_an(self, token_types):
        if self.tokens[self.current_token_index].token in token_types:
            self.advance_token()
            return True
        else:
            return False

    # Умножение и деление
    def Term_Prime(self):
        term_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("*") or self.token_is("/"):
            self.output.append(" " + operator_token + " ")
            if not self.Factor():
                term_prime = False
            else:
                if not self.Term_Prime():
                    term_prime = False

        return term_prime

    # Обработка выражений / и *
    def Term(self):
        term = False
        if self.Factor():
            if self.Term_Prime():
                term = True
        return term

    # Сложение и вычитание
    def Expression_Prime(self):
        expression_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("+") or self.token_is("-"):
            self.output.append(" " + operator_token + " ")
            if not self.Term():
                expression_prime = False
            else:
                if not self.Expression_Prime():
                    expression_prime = False

        return expression_prime

    # Обработка выражений + и -
    def Expression(self):
        expression = False
        if self.Term():
            if self.Expression_Prime():
                expression = True

        return expression

    # Обьявление переменной
    def variableDeclaration(self):
        instruction = False
        operator_token = self.tokens[self.current_token_index - 1].lexeme
        if self.token_is('='):
            self.output.append(operator_token + " " + self.tokens[
                self.current_token_index - 1].lexeme + " ")
            if self.Expression():
                instruction = True
            if not self.token_in(Constants.VALID_EOL_SYMBOLS):
                instruction = False

        return instruction

    # Запуск обьявления переменной
    def Declaration(self):
        declaration = False
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            if self.variableDeclaration():
                declaration = True

        return declaration
        # Обработка условий

    def Conditional(self, flag):
        conditional = False
        if flag:
            self.advance_token()
            self.advance_token()
            if self.token_is("="):
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme)
                    self.advance_token()
                    conditional = True
            if self.token_is("!"):
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme)
                    self.advance_token()
                    conditional = True
            if self.token_is("<") or self.token_is(">"):
                if self.token_is("="):
                    less_or_more = self.tokens[self.current_token_index - 2]
                    if less_or_more.lexeme == '>':
                        self.output.append(self.tokens[self.current_token_index].lexeme + " - 1, ")
                    else:
                        self.output.append(self.tokens[self.current_token_index].lexeme + " + 1, ")
                    while self.tokens[self.current_token_index].lexeme != "+" and self.tokens[
                        self.current_token_index].lexeme != "-":
                        self.advance_token()
                    if self.tokens[self.current_token_index].lexeme == "-":
                        self.output.append(self.tokens[self.current_token_index].lexeme)
                    self.output.append(self.tokens[self.current_token_index + 1].lexeme + "):")
                    conditional = True
                else:
                    self.output.append(self.tokens[self.current_token_index].lexeme + ", ")
                    while self.tokens[self.current_token_index].lexeme != "+" and self.tokens[
                        self.current_token_index].lexeme != "-":
                        self.advance_token()
                    if self.tokens[self.current_token_index].lexeme == "-":
                        self.output.append(self.tokens[self.current_token_index].lexeme)
                    self.output.append(self.tokens[self.current_token_index + 1].lexeme + "):")
                    conditional = True
        else:
            if self.Expression():
                operator_token = self.tokens[self.current_token_index].lexeme
                if self.token_is("="):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                if self.token_is("!"):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                if self.token_is("<") or self.token_is(">"):
                    self.output.append(" " + operator_token)
                    operator_token = self.tokens[self.current_token_index].lexeme
                    if self.token_is("="):
                        self.output.append(operator_token + " ")
                        if self.Expression():
                            conditional = True
                    else:
                        self.output.append(" ")
                        if self.Expression():
                            conditional = True

        return conditional

    # Аргументы функции
    def Function_Parameters(self):
        function_parameters = True
        if self.Expression():
            if self.token_is(","):
                self.output.append(", ")
                self.Function_Parameters()

        return function_parameters

    # Обработка вызова функции
    def Assignment(self):
        assignment = False
        if self.token_is('('):
            self.output.append(self.tokens[self.current_token_index - 2].lexeme +
                               self.tokens[self.current_token_index - 1].lexeme)
            if self.Function_Parameters():
                if self.token_is(')'):
                    self.output.append(")")
                self.token_in(Constants.VALID_EOL_SYMBOLS)
        elif self.variableDeclaration():
            assignment = True

        return assignment

    # Инициализация функций и её параметров
    def Initialization(self):
        initial = True
        if self.token_in(Constants.VALID_DATA_TYPES):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                if self.token_is(','):
                    self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
                    self.Initialization()
                else:
                    self.output.append("):\n")
            else:
                initial = False
        else:
            self.output.append("):\n")

        return initial

    def Else(self):
        if self.token_is("else"):
            self.output.append("\n")
            self.tabs_count -= 1
            for i in range(self.tabs_count):
                self.output.append("\t")
            self.tabs_count += 1
            self.output.append(self.tokens[self.current_token_index - 1].lexeme + ":")
            if self.token_is("{"):
                while not self.token_is("}"):
                    self.Statement()
        return True

    def If_Statement(self):
        ifstate = False
        self.output.append("\n")
        for i in range(self.tabs_count):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
        self.tabs_count += 1
        if self.token_is("("):
            if self.Conditional(False):
                if self.token_is(")"):
                    self.output[-1] = self.output[-1].strip()
                    self.output.append(":")
                    if self.token_is("{"):
                        while not self.token_is("}"):
                            self.Statement()
                        ifstate = self.Else()
        return ifstate

    # For
    def For_Loop(self):
        for_loop = False
        if self.output[-1][-1] != '\n':
            self.output.append("\n")
        for i in range(self.tabs_count):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
        self.tabs_count += 1
        if self.token_is("("):
            if self.token_in(Constants.VALID_DATA_TYPES):
                self.output.append(self.tokens[self.current_token_index].lexeme + " in range(")
                self.advance_token()
                if self.token_is("="):
                    self.output.append(self.tokens[self.current_token_index].lexeme + ", ")
                    self.advance_token()
                if self.Conditional(True):
                    while not self.token_is("{"):
                        self.advance_token()
                    while not self.token_is("}"):
                        self.Statement()
        return for_loop

    # While
    def While_Loop(self) -> bool:
        while_loop = False
        self.output.append("\n")
        for i in range(self.tabs_count):
            self.output.append("\t")
        self.output.append(self.tokens[self.current_token_index - 1].lexeme + " ")
        self.tabs_count += 1
        if self.token_is("("):
            self.Conditional(False)
            if self.token_is(")"):
                self.output[-1] = self.output[-1].strip()
                self.output.append(":")
                if self.token_is("{"):
                    while not self.token_is("}"):
                        self.Statement()
        return while_loop

    # Запуск функций для операторов
    def Statement(self):
        start = False
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            self.tabs()
            start = self.Assignment()
        elif self.token_in(Constants.VALID_DATA_TYPES):
            self.tabs()
            start = self.Declaration()
        elif self.token_is("if"):
            start = self.If_Statement()
            self.tabs_count -= 1
        elif self.token_is("for"):
            start = self.For_Loop()
            self.tabs_count -= 1
        elif self.token_is("while"):
            start = self.While_Loop()
            self.tabs_count -= 1
        elif self.token_is("return"):
            self.tabs()
            self.output.append("return ")
            start = self.Expression()
            self.token_in(Constants.VALID_EOL_SYMBOLS)

        return start

    # Значение переменной
    def Factor(self):
        factor = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_in(Constants.SIGNED_OPERATORS):
            self.output.append(operator_token)
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.token_is('('):
                    self.output.append(operator_token)
                else:
                    self.output.append(operator_token + "(")
                    if not self.token_is(')'):
                        self.Function_Parameters()
                        if not self.token_is(')'):
                            factor = False
                        else:
                            self.output.append(")")
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.token_is("("):
                self.output.append("(")
                if self.Expression():
                    if self.token_is(")"):
                        self.output.append(")")
                        factor = True
                    else:
                        factor = False
            else:
                factor = False
        else:
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.token_is('('):
                    self.output.append(operator_token)
                else:
                    self.output.append(operator_token + "(")
                    if not self.token_is(')'):
                        self.Function_Parameters()
                        if not self.token_is(')'):
                            factor = False
                        else:
                            self.output.append(")")
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme)
                factor = True
            elif self.is_current_token_an([LexerToken.BOOLEAN]):
                if self.tokens[self.current_token_index - 1].lexeme == "true":
                    self.output.append("True")
                else:
                    self.output.append("False")
                factor = True
            elif self.token_is('"') or self.token_is("'"):
                self.output.append(self.tokens[self.current_token_index - 1].lexeme +
                                   self.tokens[self.current_token_index].lexeme)
                self.is_current_token_an([LexerToken.STRING])
                if not (self.token_is('"') or self.token_is("'")):
                    factor = False
                else:
                    self.output.append(self.tokens[self.current_token_index - 1].lexeme)
            elif self.token_is("("):
                self.output.append("(")
                if self.Expression():
                    if self.token_is(")"):
                        self.output.append(")")
                        factor = True
                    else:
                        factor = False
            else:
                factor = False

        return factor

    def Start(self):
        if self.token_in(Constants.VALID_DATA_TYPES):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if self.token_is('('):
                    if not self.output:
                        self.output.append("def " + self.tokens[self.current_token_index - 2].lexeme + "(")
                    else:
                        self.output.append("\n\ndef " + self.tokens[self.current_token_index - 2].lexeme + "(")
                    if self.Initialization():
                        self.token_is(')')
                        self.token_is('{')
                        while not self.token_is("}"):
                            self.Statement()

    # Запуск программы
    def parse(self, tokens: list, errors_semantic: list, errors_syntax: list):
        self.tokens = tokens
        self.errors_syntax = copy.copy(errors_syntax)
        self.errors_semantic = copy.copy(errors_semantic)
        if len(tokens) > 1:
            if len(self.errors_syntax) != 0 or len(self.errors_semantic) != 0:
                self.output.append('No code for you. Do better!\n\n')
                return
            while not self.is_current_token_an([LexerToken.END_OF_FILE]):
                self.Start()
            self.output.append("\n\n\nif __name__ == " + '"__main__":\n    main()\n')

    def create_string_output(self):
        result = ''
        for line in self.output:
            result += line
        return result
