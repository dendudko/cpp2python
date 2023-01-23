import copy

from Translator.Constants.constants import *


class SemanticAnalyser:
    def __init__(self):
        self.tokens = []
        self.positions = []
        self.attributes = []
        self.output = []
        self.errors = []
        self.ids = set()
        self.ids_to_tokens = {}
        self.current_token_index = 0
        self.cur_depth = 0
        self.cur_func = ()
        self.func_to_params = {}

        self.types_to_tokens = {
            'int': LexerToken.INTEGER,
            'std::string': LexerToken.STRING,
            'bool': LexerToken.BOOLEAN,
            'float': LexerToken.REAL,
            'double': LexerToken.REAL,
            'void': LexerToken.KEYWORD
        }

        self.err_to_str = {
            ErrorTypes.UNRECOGNIZED: "Error: Unrecognized value. Factor must be an integer, "
                                     "float, string, identifier or expression. [{},{}]\n",
            ErrorTypes.WRONG_TYPE: "Error: Wrong data type. [{},{}]\n",
            ErrorTypes.INVALID_EXP: "Error: Invalid expression. [{},{}]\n",
            ErrorTypes.INVALID_ID: "Error: string type does not support operators +, -, /, * . [{},{}]\n",
            ErrorTypes.REINITIALIZE: "Error: Reinitialization. [{},{}]\n",
            ErrorTypes.NOT_INITIALIZE: "Error: Not initialized. [{},{}]\n",
            ErrorTypes.MISSING_MAIN: "Error: Expected main function.\n",
            ErrorTypes.WRONG_COUNT: "Error: Wrong count of arguments. [{},{}]\n"
        }

    def backup(self, param_type: str):
        if self.current_token_index > 0:
            self.current_token_index -= 1
            if param_type == 'lexeme':
                value = self.tokens[self.current_token_index].lexeme
            elif param_type == 'token':
                value = self.tokens[self.current_token_index].token
            elif param_type == 'index':
                value = self.current_token_index
            else:
                raise ValueError
            self.advance_token()
            return value

    def create_string_output(self):
        result = ''
        for line in self.output:
            result += line
        return result

    def parse(self, tokens: list, positions: list, errors: list):
        self.tokens = tokens
        self.positions = positions
        self.errors = copy.copy(errors)

        if len(tokens) > 1:
            while not self.is_current_token_an([LexerToken.END_OF_FILE]) and len(self.errors) == 0:
                self.Start()
            if ('main', 0) not in self.ids and len(self.errors) == 0:
                self.output.clear()
                self.errprint(ErrorTypes.MISSING_MAIN)

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
        if self.tokens[self.current_token_index].token in token_types:
            self.output.append("Lexeme: " + self.tokens[self.current_token_index].lexeme +
                               "  Token: " + self.tokens[self.current_token_index].token.name + "\n")
            self.advance_token()
            return True
        else:
            return False

    def advance_token(self):
        if self.current_token_index < (len(self.tokens) - 1):
            self.current_token_index += 1

    def del_ids(self, depth: int):
        to_delete = []
        for id_depth in self.ids:
            if id_depth[1] == depth:
                to_delete.append(id_depth)
        for id_depth in to_delete:
            self.ids.remove(id_depth)
            self.ids_to_tokens.pop(id_depth)

    def check_id_in_ids(self, token_id: str):
        for depth in range(0, self.cur_depth + 1):
            if (token_id, depth) in self.ids:
                return token_id, depth
        return False

    def errprint(self, err_type: ErrorTypes):
        if len(self.errors) == 0:
            self.errors.append(Error(err_type, int(self.backup('index'))))
            self.output.append('\n' + self.err_to_str[err_type].format(
                self.positions[int(self.backup('index'))]['row'],
                self.positions[int(self.backup('index'))]['pos']) + 'Token index: '
                               + str(self.backup('index')))

    def Start(self):
        if self.token_in(Constants.VALID_DATA_TYPES):
            self.output.append("<Start> -> <Data-Type> <Identifier> (<Initialization>) {<Statement>}\n")
            data_type = self.types_to_tokens[self.backup('lexeme')]
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.check_id_in_ids(self.backup('lexeme')):
                    self.ids_to_tokens[(self.backup('lexeme'), self.cur_depth)] = data_type
                    self.ids.add((self.backup('lexeme'), self.cur_depth))
                    self.cur_func = (self.backup('lexeme'), self.cur_depth)
                    if self.token_is('('):
                        self.cur_depth = self.cur_depth + 1
                        if self.Initialization():
                            self.token_is(')')
                            self.token_is('{')
                            while not self.token_is("}") and len(self.errors) == 0:
                                self.Statement()
                            self.del_ids(self.cur_depth)
                            self.cur_depth = self.cur_depth - 1
                else:
                    self.errprint(ErrorTypes.REINITIALIZE)

    def Statement(self, _id=None) -> bool:
        start = False

        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            self.output.append("<Statement> -> <Assignment>\n")
            if self.check_id_in_ids(self.backup('lexeme')):
                start = self.Assignment(self.check_id_in_ids(self.backup('lexeme')))
            else:
                self.errprint(ErrorTypes.NOT_INITIALIZE)
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
            start = self.Expression(self.cur_func)
            self.token_in(Constants.VALID_EOL_SYMBOLS)
        else:
            self.errprint(ErrorTypes.WRONG_COUNT)

        return start

    def Declaration(self) -> bool:
        declaration = False
        self.output.append("<Declaration> -> <Data-Type> <Assignment>\n")
        data_type = self.types_to_tokens[self.backup('lexeme')]
        if self.is_current_token_an([LexerToken.IDENTIFIER]):
            if (self.backup('lexeme'), self.cur_depth) not in self.ids:
                self.ids_to_tokens[(self.backup('lexeme'), self.cur_depth)] = data_type
                self.ids.add((self.backup('lexeme'), self.cur_depth))
                if self.Instruction((self.backup('lexeme'), self.cur_depth)):
                    declaration = True
            else:
                self.errprint(ErrorTypes.REINITIALIZE)

        return declaration

    def Assignment(self, _id=None) -> bool:
        assignment = False
        identifier = self.backup('lexeme')
        if self.token_is('('):
            self.output.append("<Assignment> -> <Identifier> (<Function-Parameters>);\n")
            if self.Function_Parameters(len(self.func_to_params[self.check_id_in_ids(identifier)]),
                                        self.func_to_params[self.check_id_in_ids(identifier)]):
                self.token_is(')')
                self.token_in(Constants.VALID_EOL_SYMBOLS)
        elif self.Instruction(_id):
            assignment = True

        return assignment

    def Initialization(self) -> bool:
        initial = True
        if self.cur_func not in self.func_to_params.keys():
            self.func_to_params[self.cur_func] = []
        if self.token_in(Constants.VALID_DATA_TYPES):
            data_type = self.types_to_tokens[self.backup('lexeme')]
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if not self.check_id_in_ids(self.backup('lexeme')):
                    self.ids_to_tokens[(self.backup('lexeme'), self.cur_depth)] = data_type
                    self.ids.add((self.backup('lexeme'), self.cur_depth))
                    self.func_to_params[self.cur_func].append(data_type)
                else:
                    self.errprint(ErrorTypes.REINITIALIZE)
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

    def Instruction(self, _id=None) -> bool:
        instruction = False
        if self.token_is('='):
            self.output.append("<Instruction> -> <Identifier> = <Expression>;\n")
            if self.Expression(_id):
                instruction = True
                self.token_in(Constants.VALID_EOL_SYMBOLS)

        return instruction

    def If_Statement(self) -> bool:
        ifstate = False
        self.output.append("<If-Statement> -> if (<Conditional>) {<Statement>} <Else>\n")
        if self.token_is("("):
            if self.Conditional():
                if self.token_is(")"):
                    if self.token_is("{"):
                        self.cur_depth = self.cur_depth + 1
                        while not self.token_is("}"):
                            if len(self.errors) != 0:
                                break
                            self.Statement()
                        self.del_ids(self.cur_depth)
                        self.cur_depth = self.cur_depth - 1
                        ifstate = self.Else()

        return ifstate

    def Conditional(self, _id=None) -> bool:
        conditional = False
        self.output.append("<Conditional> -> <Expression> <Conditional-Operator> <Expression>\n")

        if self.Expression(_id):
            if self.token_is("="):
                if self.token_is("="):
                    if self.Expression(_id):
                        conditional = True
            if self.token_is("!"):
                if self.token_is("="):
                    if self.Expression(_id):
                        conditional = True

            if self.token_is("<") or self.token_is(">"):
                if self.token_is("="):
                    if self.Expression(_id):
                        conditional = True
                else:
                    if self.Expression(_id):
                        conditional = True

        return conditional

    def Else(self) -> bool:
        if self.token_is("else"):
            self.output.append("<Else> -> else {<Statement>}\n")
            if self.token_is("{"):
                self.cur_depth = self.cur_depth + 1
                while not self.token_is("}"):
                    if len(self.errors) != 0:
                        break
                    self.Statement()
                self.del_ids(self.cur_depth)
                self.cur_depth = self.cur_depth - 1
        else:
            if len(self.errors) == 0:
                self.output.append("<Else> -> epsilon\n")
        self.token_is(";")

        return True

    def For_Loop(self) -> bool:
        for_loop = False
        self.output.append("<For-loop> -> for (<Declaration>; <Conditional>; "
                           "<Identifier> = <Expression>) {<Statement>}\n")
        if self.token_is("("):
            self.cur_depth = self.cur_depth + 1
            if self.token_in(Constants.VALID_DATA_TYPES):
                self.output.append("<Declaration> -> <Data-Type> <Assignment>\n")
                data_type = self.types_to_tokens[self.backup('lexeme')]
                if self.is_current_token_an([LexerToken.IDENTIFIER]):
                    if not self.check_id_in_ids(self.backup('lexeme')):
                        self.ids_to_tokens[(self.backup('lexeme'), self.cur_depth)] = data_type
                        self.ids.add((self.backup('lexeme'), self.cur_depth))
                        _id = (self.backup('lexeme'), self.cur_depth)
                        self.Instruction((self.backup('lexeme'), self.cur_depth))
                        if self.Conditional(_id):
                            if self.token_is(";"):
                                if self.is_current_token_an([LexerToken.IDENTIFIER]):
                                    if self.check_id_in_ids(self.backup('lexeme')):
                                        if self.token_is('='):
                                            if not self.Expression():
                                                self.errprint(ErrorTypes.INVALID_EXP)
                                        self.token_is(")")
                                        self.token_is("{")
                                        while not self.token_is("}"):
                                            if len(self.errors) != 0:
                                                break
                                            self.Statement()
                                        self.del_ids(self.cur_depth)
                                        self.cur_depth = self.cur_depth - 1
                                        for_loop = True
                                    else:
                                        self.errprint(ErrorTypes.NOT_INITIALIZE)
                    else:
                        self.errprint(ErrorTypes.REINITIALIZE)
        return for_loop

    def While_Loop(self) -> bool:
        while_loop = False
        self.output.append("<While-Loop> -> while (<conditional>) {<Statement>};\n ")
        if self.token_is("("):
            self.Conditional()
            self.token_is(")")
            self.token_is("{")
            self.cur_depth = self.cur_depth + 1
            while not self.token_is("}"):
                if len(self.errors) != 0:
                    break
                self.Statement()
            self.del_ids(self.cur_depth)
            self.cur_depth = self.cur_depth - 1
            self.token_is(";")

        return while_loop

    def Expression(self, _id=None, argument=None) -> bool:
        expression = False
        self.output.append("<Expression> -> <Term> <Expression-Prime>\n")
        if self.Term(_id, argument):
            if self.Expression_Prime(_id, argument):
                expression = True

        return expression

    def Expression_Prime(self, _id=None, argument=None) -> bool:
        expression_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("+") or self.token_is("-"):
            self.output.append("<Expression-Prime> -> " + operator_token + " <Term> <Expression-Prime>\n")
            if not self.Term(_id, argument):
                expression_prime = False
            else:
                if not self.Expression_Prime(_id, argument):
                    expression_prime = False
        else:
            if len(self.errors) == 0:
                self.output.append("<Expression-Prime> -> epsilon\n")

        return expression_prime

    def Term(self, _id=None, argument=None) -> bool:
        term = False

        self.output.append("<Term> -> <Factor> <Term-Prime>\n")
        if self.Factor(_id, argument):
            if self.Term_Prime(_id, argument):
                term = True

        return term

    def Term_Prime(self, _id=None, argument=None) -> bool:
        term_prime = True
        operator_token = self.tokens[self.current_token_index].lexeme
        if self.token_is("*") or self.token_is("/"):
            self.output.append("<Term-Prime> -> " + operator_token + " <Factor> <Term-Prime>\n")
            if not self.Factor(_id, argument):
                term_prime = False
            else:
                if not self.Term_Prime(_id, argument):
                    term_prime = False
        else:
            if len(self.errors) == 0:
                self.output.append("<Term-Prime> -> epsilon\n")
        return term_prime

    def Function_Parameters(self, count_params=0, arguments=[]) -> bool:
        function_parameters = True
        self.output.append("<Function-Parameters> -> <Expression> | <Function-Parameters> -> <Expression>, "
                           "<Function-Parameters>\n")
        if count_params > 0:
            if self.Expression(argument=arguments[len(arguments) - count_params]):
                count_params -= 1
                if self.token_is(","):
                    function_parameters = self.Function_Parameters(count_params, arguments)
                elif count_params > 0:
                    self.errprint(ErrorTypes.WRONG_COUNT)
                    function_parameters = False
            else:
                self.errprint(ErrorTypes.WRONG_COUNT)
                function_parameters = False
        elif len(self.errors) == 0:
            self.output.append("<Function-Parameters> ->  epsilon\n")
        else:
            self.errprint(ErrorTypes.WRONG_COUNT)
            function_parameters = False
        return function_parameters

    def Factor(self, _id=None, argument=None) -> bool:
        factor = True
        operator = self.backup('lexeme')
        if self.token_in(Constants.SIGNED_OPERATORS):
            if self.is_current_token_an([LexerToken.IDENTIFIER]):
                if self.check_id_in_ids(self.backup('lexeme')):
                    identifier = self.backup('lexeme')
                    if _id is not None:
                        if self.ids_to_tokens[_id] != self.ids_to_tokens[self.check_id_in_ids(identifier)]:
                            self.errprint(ErrorTypes.WRONG_TYPE)
                            factor = False
                    if argument is not None:
                        if argument != self.ids_to_tokens[self.check_id_in_ids(identifier)]:
                            self.errprint(ErrorTypes.WRONG_TYPE)
                            factor = False
                    if not self.token_is('('):
                        if len(self.errors) == 0:
                            self.output.append("<Factor> -> <Identifier>\n")
                    else:
                        self.output.append("<Factor> -> <Identifier>(<Function-Parameters>)\n")
                        if not self.token_is(')'):
                            factor = self.Function_Parameters(
                                len(self.func_to_params[self.check_id_in_ids(identifier)]),
                                self.func_to_params[self.check_id_in_ids(identifier)])
                            if not self.token_is(')'):
                                factor = False
                        elif len(self.func_to_params[self.check_id_in_ids(identifier)]) != 0:
                            self.errprint(ErrorTypes.WRONG_COUNT)
                            factor = False
                else:
                    self.errprint(ErrorTypes.NOT_INITIALIZE)
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append("<Factor> -> <Integer>\n")
                if _id is not None:
                    if self.ids_to_tokens[_id] != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
                if argument is not None:
                    if argument != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append("<Factor> -> <Float>\n")
                if _id is not None:
                    if self.ids_to_tokens[_id] != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
                if argument is not None:
                    if argument != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
            elif self.token_is("("):
                self.output.append("<Factor> -> (<Expression>)\n")
                if self.Expression(_id, argument):
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
                if self.check_id_in_ids(self.backup('lexeme')):
                    identifier = self.backup('lexeme')
                    if _id is not None:
                        if self.ids_to_tokens[_id] != self.ids_to_tokens[self.check_id_in_ids(identifier)]:
                            self.errprint(ErrorTypes.WRONG_TYPE)
                            factor = False
                    if argument is not None:
                        if argument != self.ids_to_tokens[self.check_id_in_ids(identifier)]:
                            self.errprint(ErrorTypes.WRONG_TYPE)
                            factor = False
                    if not self.token_is('('):
                        if len(self.errors) == 0:
                            self.output.append("<Factor> -> <Identifier>\n")
                    else:
                        self.output.append("<Factor> -> <Identifier>(<Function-Parameters>)\n")
                        if not self.token_is(')'):
                            factor = self.Function_Parameters(
                                len(self.func_to_params[self.check_id_in_ids(identifier)]),
                                self.func_to_params[self.check_id_in_ids(identifier)])
                            if not self.token_is(')'):
                                factor = False
                        elif len(self.func_to_params[self.check_id_in_ids(identifier)]) != 0:
                            self.errprint(ErrorTypes.WRONG_COUNT)
                            factor = False
                else:
                    self.errprint(ErrorTypes.NOT_INITIALIZE)
            elif self.is_current_token_an([LexerToken.INTEGER]):
                self.output.append("<Factor> -> <Integer>\n")
                if _id is not None:
                    if self.ids_to_tokens[_id] != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
                if argument is not None:
                    if argument != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
            elif self.is_current_token_an([LexerToken.REAL]):
                self.output.append("<Factor> -> <Float>\n")
                if _id is not None:
                    if self.ids_to_tokens[_id] != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
                if argument is not None:
                    if argument != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
            elif self.is_current_token_an([LexerToken.BOOLEAN]):
                self.output.append("<Factor> -> <Boolean>\n")
                if _id is not None:
                    if self.ids_to_tokens[_id] != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
                if argument is not None:
                    if argument != self.backup('token'):
                        self.errprint(ErrorTypes.WRONG_TYPE)
                        factor = False
            elif self.token_is('"') or self.token_is("'"):
                self.output.append("<Factor> -> <String>\n")
                if operator not in ['=', 'return', '(', ',']:
                    self.errprint(ErrorTypes.INVALID_ID)
                elif self.is_current_token_an([LexerToken.STRING]):
                    if _id is not None:
                        if self.ids_to_tokens[_id] != self.backup('token'):
                            self.errprint(ErrorTypes.WRONG_TYPE)
                            factor = False
                    if argument is not None:
                        if argument != self.backup('token'):
                            self.errprint(ErrorTypes.WRONG_TYPE)
                            factor = False
                if not (self.token_is('"') or self.token_is("'")):
                    factor = False
            elif self.token_is("("):
                self.output.append("<Factor> -> (<Expression>)\n")
                if self.Expression(_id, argument):
                    if self.token_is(")"):
                        factor = True
                    else:
                        factor = False
            elif self.is_current_token_an([LexerToken.NOT_EXISTS, LexerToken.INVALID]):
                factor = False
            else:
                factor = False
        return factor
