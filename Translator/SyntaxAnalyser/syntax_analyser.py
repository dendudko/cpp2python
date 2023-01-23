from Translator.Constants.constants import *


class SyntaxAnalyserRDP:
    def __init__(self):
        self.tokens = []
        self.positions = []
        self.current_token_index = 0
        self.output = []
        self.errors = []

        self.err_to_str = {
            ErrorTypes.EXPECTED_INIT: "{}Error: Expected Initialization variables. [{},{}]\n",
            ErrorTypes.MISSING: "Error: Missing {} [{},{}]\n",
            ErrorTypes.EXPECTED_DEC: "{}Error: Expected a declaration of function. [{},{}]\n",
            ErrorTypes.EXPECTED_STAT: "{}Error: Expected a statement. [{},{}]\n",
            ErrorTypes.EXPECTED_ID: "{}Error: Expected identifier. [{},{}]\n",
            ErrorTypes.UNRECOGNIZED: "{}Error: Unrecognized conditional operator. [{},{}]\n",
            ErrorTypes.WRONG_TYPE: "{}Error: Invalid data type. [{},{}]\n",
            ErrorTypes.INVALID_ID: "{}Error: Not a valid identifier. [{},{}]\n",
            ErrorTypes.INVALID_EXP: "{}Error: Invalid expression. [{},{}]\n",
            ErrorTypes.INVALID: "Error: Invalid position of character '{}'. [{},{}]\n",
            ErrorTypes.NOT_EXISTS: "Error: Not an existing character '{}'. [{},{}]\n"
        }

    def parse(self, tokens: list, positions: list, errors: list):
        self.tokens = tokens
        self.positions = positions
        self.errors = errors
        # Обработка ошибки из лексера
        if self.current_token_index == 0 and len(self.errors) > 0:
            err_type = None
            if ErrorTypes(self.errors[0].type) == ErrorTypes.INVALID:
                err_type = ErrorTypes.INVALID
            elif ErrorTypes(self.errors[0].type) == ErrorTypes.NOT_EXISTS:
                err_type = ErrorTypes.NOT_EXISTS
            self.output.append('\n' + self.err_to_str[err_type].format(
                self.tokens[int(self.errors[0].index)].lexeme,
                self.positions[int(self.errors[0].index)]['row'],
                self.positions[int(self.errors[0].index)]['pos'] + 1) + 'Token index: '
                               + str(self.errors[0].index))
        if len(tokens) > 1:
            while not self.is_current_token_an([LexerToken.END_OF_FILE]) and len(self.errors) == 0:
                self.Start()

    def create_string_output(self):
        result = ''
        for line in self.output:
            result += line
        return result

    def token_is(self, token_to_match: str) -> bool:
        if self.tokens[self.current_token_index].lexeme == token_to_match and len(self.errors) == 0:
            self.output.append("Lexeme: " + self.tokens[self.current_token_index].lexeme +
                               "  Token: " + self.tokens[self.current_token_index].token.name + "\n")
            self.advance_token()
            return True
        else:
            return False

    def token_in(self, token_list: list) -> bool:
        if len(token_list) == 1:
            return self.token_is(token_list[0])
        else:
            if self.tokens[self.current_token_index].lexeme in token_list:
                self.output.append("Lexeme: " + self.tokens[self.current_token_index].lexeme +
                                   "  Token: " + self.tokens[self.current_token_index].token.name + "\n")
                self.advance_token()
                return True
            else:
                return False

    def is_current_token_an(self, token_types: list) -> bool:
        if self.tokens[self.current_token_index].token in token_types and len(self.errors) == 0:
            self.output.append("Lexeme: " + self.tokens[self.current_token_index].lexeme +
                               "  Token: " + self.tokens[self.current_token_index].token.name + "\n")
            self.advance_token()
            return True
        else:
            return False

    def advance_token(self):
        if self.current_token_index < (len(self.tokens) - 1):
            self.current_token_index += 1

    def backup(self, flag: str):
        if self.current_token_index > 0:
            value = ''
            self.current_token_index -= 1
            if flag == 'lexeme':
                value = self.tokens[self.current_token_index].lexeme
            if flag == 'token':
                value = self.tokens[self.current_token_index].token
            if flag == 'index':
                value = self.current_token_index
            self.advance_token()
            return value

    def errprint(self, err_type: ErrorTypes, symbol=''):
        if len(self.errors) == 0:
            if self.current_token_index == 0:
                token_id = 0
            else:
                token_id = int(self.backup('index'))
            self.errors.append(Error(err_type, token_id))
            self.output.append('\n' + self.err_to_str[err_type].format(
                symbol,
                self.positions[token_id]['row'],
                self.positions[token_id]['pos']) + 'Token index: '
                               + str(token_id))

    def Start(self):
        if self.token_in(Constants.VALID_DATA_TYPES):
            self.output.append("<Start> -> <Data-Type> <Identifier> (<Initialization>) {<Statement>}\n")
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if self.token_is('('):
                    if self.Initialization():
                        if not self.token_is(')'):
                            self.errprint(ErrorTypes.EXPECTED_INIT)
                        if not self.token_is('{'):
                            self.errprint(ErrorTypes.MISSING, '{')
                        while not self.token_is("}") and len(self.errors) == 0:
                            self.Statement()
        else:
            self.errprint(ErrorTypes.EXPECTED_DEC)

    def Statement(self) -> bool:
        start = False

        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            self.output.append("<Statement> -> <Assignment>\n")
            start = self.Assignment()
        elif self.token_in(Constants.VALID_DATA_TYPES):
            self.output.append("<Statement> -> <Declaration>\n")
            start = self.Declaration()
        elif self.token_is("if"):
            self.output.append("<Statement> -> <If-Statement>\n")
            start = self.If_Statement()
        elif self.token_is("for"):
            self.output.append("<Statement> -> <For-Loop>\n")
            start = self.For_Loop()
        elif self.token_is("while"):
            self.output.append("<Statement> -> <While-Loop>\n")
            start = self.While_Loop()
        elif self.token_is("return"):
            self.output.append("<Statement> -> return <Expression>\n")
            start = self.Expression()
            if not self.token_in(Constants.VALID_EOL_SYMBOLS):
                self.errors.clear()
                self.errprint(ErrorTypes.MISSING, ';')
        else:
            self.errprint(ErrorTypes.EXPECTED_STAT)

        return start

    def Declaration(self) -> bool:
        declaration = False
        self.output.append("<Declaration> -> <Data-Type> <Assignment>\n")
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            if self.Instruction():
                declaration = True
        else:
            self.errprint(ErrorTypes.INVALID_ID)
        return declaration

    def Assignment(self) -> bool:
        assignment = False
        if self.token_is('('):
            self.output.append("<Assignment> -> <Identifier> (<Function-Parameters>)\n")
            if self.Function_Parameters():
                if not self.token_is(')'):
                    self.errprint(ErrorTypes.EXPECTED_INIT)
                if not self.token_in(Constants.VALID_EOL_SYMBOLS):
                    self.errprint(ErrorTypes.MISSING, ';')
            else:
                self.errprint(ErrorTypes.EXPECTED_ID)
        elif self.Instruction():
            assignment = True
        else:
            self.errprint(ErrorTypes.EXPECTED_INIT)

        return assignment

    def Initialization(self) -> bool:
        initial = True
        if self.token_in(Constants.VALID_DATA_TYPES):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if self.token_is(','):
                    self.output.append("<Initialization> -> <Data-Type> <Identifier>, <Initialization>\n")
                    self.Initialization()
                else:
                    self.output.append("<Data-Type> <Identifier>\n")
            else:
                initial = False
        else:
            self.output.append("<Initialization> -> epsilon\n")
        return initial

    def Instruction(self) -> bool:
        instruction = False
        if self.token_is('='):
            self.output.append("<Instruction> -> <Identifier> = <Expression>\n")
            if self.Expression():
                instruction = True
            else:
                self.errprint(ErrorTypes.INVALID_EXP)
            if not self.token_in(Constants.VALID_EOL_SYMBOLS):
                self.errprint(ErrorTypes.MISSING, ';')
                instruction = False
        else:
            self.errprint(ErrorTypes.EXPECTED_STAT)

        return instruction

    def If_Statement(self) -> bool:
        ifstate = False
        self.output.append("<If-Statement> -> if (<Conditional>) {<Statement>} <Else>\n")
        if self.token_is("("):
            if self.Conditional():
                if self.token_is(")"):
                    if self.token_is("{"):
                        while not self.token_is("}"):
                            if len(self.errors) != 0:
                                break
                            self.Statement()
                        ifstate = self.Else()
                    else:
                        self.errprint(ErrorTypes.MISSING, '{')
                else:
                    self.errprint(ErrorTypes.MISSING, ')')
            else:
                self.errprint(ErrorTypes.INVALID_EXP)
        else:
            self.errprint(ErrorTypes.MISSING, '(')

        return ifstate

    def Conditional(self) -> bool:
        conditional = False
        self.output.append("<Conditional> -> <Expression> <Conditional-Operator> <Expression>\n")
        if self.Expression():
            if self.token_is("="):
                if self.token_is("="):
                    if self.Expression():
                        conditional = True
                else:
                    self.errprint(ErrorTypes.UNRECOGNIZED)
            if self.token_is("!"):
                if self.token_is("="):
                    if self.Expression():
                        conditional = True
                else:
                    self.errprint(ErrorTypes.UNRECOGNIZED)
            if self.token_is("<") or self.token_is(">"):
                if self.token_is("="):
                    if self.Expression():
                        conditional = True
                elif self.token_in(Constants.VALID_KEYWORDS + Constants.VALID_OPERATORS):
                    self.errprint(ErrorTypes.UNRECOGNIZED)
                else:
                    if self.Expression():
                        conditional = True

        return conditional

    def Else(self) -> bool:
        if self.token_is("else"):
            self.output.append("<Else> -> else {<Statement>}\n")
            if self.token_is("{"):
                while not self.token_is("}"):
                    if len(self.errors) != 0:
                        break
                    self.Statement()
            else:
                self.errprint(ErrorTypes.MISSING, '{')
        else:
            if len(self.errors) == 0:
                self.output.append("<Else> -> epsilon\n")
        return True

    def For_Loop(self) -> bool:
        for_loop = False
        self.output.append(
            "<For-loop> -> for (<Declaration>; <Conditional>; <Identifier> = <Expression>) {<Statement>}\n")
        if self.token_is("("):
            if self.token_in(Constants.VALID_DATA_TYPES):
                self.Declaration()
                if self.Conditional():
                    if self.token_is(";"):
                        if self.is_current_token_an([LexerToken.IDENTIFIER]):
                            if self.token_is('='):
                                if not self.Expression():
                                    self.errprint(ErrorTypes.INVALID_EXP)
                        else:
                            ...  # Ошибка
                        if self.token_is(")"):
                            if self.token_is("{"):
                                while not self.token_is("}"):
                                    if len(self.errors) != 0:
                                        break
                                    self.Statement()
                            else:
                                self.errprint(ErrorTypes.MISSING, '{')
                        else:
                            self.errprint(ErrorTypes.MISSING, ')')
                    else:
                        self.errprint(ErrorTypes.MISSING, ';')
            else:
                self.errprint(ErrorTypes.WRONG_TYPE)
        else:
            self.errprint(ErrorTypes.MISSING, '(')

        return for_loop

    def While_Loop(self) -> bool:
        while_loop = False
        self.output.append("<While-Loop> -> while (<conditional>) {<Statement>}\n ")
        if self.token_is("("):
            self.Conditional()
            if self.token_is(")"):
                if self.token_is("{"):
                    while not self.token_is("}"):
                        if len(self.errors) != 0:
                            break
                        self.Statement()
                else:
                    self.errprint(ErrorTypes.MISSING, '{')
            else:
                self.errprint(ErrorTypes.MISSING, ')')
        else:
            self.errprint(ErrorTypes.MISSING, '(')

        return while_loop

    def Expression(self) -> bool:
        expression = False
        self.output.append("<Expression> -> <Term> <Expression-Prime>\n")
        if self.Term():
            if self.Expression_Prime():
                expression = True

        return expression

    def Expression_Prime(self) -> bool:
        expression_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("+") or self.token_is("-"):
            self.output.append("<Expression-Prime> -> " + operator_token + " <Term> <Expression-Prime>\n")
            if not self.Term():
                expression_prime = False
                self.errprint(ErrorTypes.INVALID_EXP)
            else:
                if not self.Expression_Prime():
                    expression_prime = False
                    self.errprint(ErrorTypes.INVALID_EXP)
        else:
            self.output.append("<Expression-Prime> -> epsilon\n")

        return expression_prime

    def Term(self) -> bool:
        term = False

        self.output.append("<Term> -> <Factor> <Term-Prime>\n")
        if self.Factor():
            if self.Term_Prime():
                term = True

        return term

    def Term_Prime(self) -> bool:
        term_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("*") or self.token_is("/"):
            self.output.append("<Term-Prime> -> " + operator_token + " <Factor> <Term-Prime>\n")
            if not self.Factor():
                term_prime = False
                self.errprint(ErrorTypes.INVALID_EXP)
            else:
                if not self.Term_Prime():
                    term_prime = False
                    self.errprint(ErrorTypes.INVALID_EXP)
        else:
            self.output.append("<Term-Prime> -> epsilon\n")
        return term_prime

    def Function_Parameters(self) -> bool:
        function_parameters = True
        self.output.append("<Function-Parameters> -> <Expression> | <Expression>, <Function-Parameters>\n")
        if self.Expression():
            if self.token_is(","):
                self.Function_Parameters()
        else:
            self.output.append("<Function-Parameters> ->  epsilon\n")
        return function_parameters

    def Factor(self) -> bool:
        factor = True
        if self.token_in(Constants.SIGNED_OPERATORS):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.token_is('('):
                    self.output.append("<Factor> -> <Identifier>\n")
                else:
                    self.output.append("<Factor> -> <Identifier>(<Function-Parameters>)\n")
                    if not self.token_is(')'):
                        self.Function_Parameters()
                        self.token_is(')')
                        self.errprint(ErrorTypes.MISSING, ')')
                        factor = False
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append("<Factor> -> <Integer>\n")
                factor = True
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append("<Factor> -> <Float>\n")
                factor = True
            elif self.token_is("("):
                self.output.append("<Factor> -> (<Expression>)\n")
                if self.Expression():
                    if self.token_is(")"):
                        factor = True
                    else:
                        factor = False
            elif self.is_current_token_an([LexerToken.NOT_EXISTS, LexerToken.INVALID, LexerToken.STRING]):
                factor = False
            else:
                factor = False
        else:
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.token_is('('):
                    self.output.append("<Factor> -> <Identifier>\n")
                else:
                    self.output.append("<Factor> -> <Identifier>(<Function-Parameters>)\n")
                    if not self.token_is(')'):
                        self.Function_Parameters()
                        if not self.token_is(')'):
                            factor = False
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append("<Factor> -> <Integer>\n")
                factor = True
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append("<Factor> -> <Float>\n")
                factor = True
            elif self.is_current_token_an([LexerToken.BOOLEAN]):
                self.output.append("<Factor> -> <Boolean>\n")
                factor = True
            elif self.token_is('"') or self.token_is("'"):
                self.output.append("<Factor> -> <String>\n")
                self.is_current_token_an([LexerToken.STRING])
                if not (self.token_is('"') or self.token_is("'")):
                    factor = False
            elif self.token_is("("):
                self.output.append("<Factor> -> (<Expression>)\n")
                if self.Expression():
                    if self.token_is(")"):
                        factor = True
                    else:
                        factor = False
            elif self.is_current_token_an([LexerToken.NOT_EXISTS]) or self.is_current_token_an([LexerToken.INVALID]):
                factor = False
            else:
                factor = False
        return factor
