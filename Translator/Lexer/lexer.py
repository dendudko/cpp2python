from Translator.Constants.constants import *


class Lexer(object):
    def __init__(self):
        self.buffer = []
        self.current_state = LexerState.START
        self.lexicon = []
        self.errors = []

        self.positions = []
        self.current_pos = {
            'row': 0,
            'pos': 0
        }

    def parse(self, line):
        self.current_pos['pos'] = 0
        self.current_pos['row'] = self.current_pos['row'] + 1
        for char in line:
            if char != Constants.SLASH and self.current_state == LexerState.SLASH:
                self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                self.add_to_lexicon('/', LexerToken.OPERATOR)
                self.return_to_start()
            if char.isalpha():
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.START:
                    self.current_state = LexerState.ALPHABETIC
                    self.append_to_buffer(char)
                elif self.current_state in [LexerState.INTEGER, LexerState.REAL]:
                    self.append_to_buffer(char)
                    self.add_to_lexicon(''.join(self.buffer), LexerToken.INVALID)
                    self.errors.append(Error(ErrorTypes.INVALID, len(self.lexicon) - 1))
                    self.return_to_start()
                elif self.current_state == LexerState.ALPHABETIC:
                    self.append_to_buffer(char)
            elif char.isnumeric():
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.START:
                    self.current_state = LexerState.INTEGER
                    self.append_to_buffer(char)
                elif self.current_state in [LexerState.INTEGER, LexerState.REAL, LexerState.ALPHABETIC]:
                    self.append_to_buffer(char)
            elif char == Constants.DECIMAL:
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.INTEGER:
                    self.current_state = LexerState.REAL
                    self.append_to_buffer(char)
                elif self.current_state in [LexerState.ALPHABETIC, LexerState.REAL]:
                    self.append_to_buffer(char)
                    self.add_to_lexicon(''.join(self.buffer), LexerToken.INVALID)
                    self.errors.append(Error(ErrorTypes.INVALID, len(self.lexicon) - 1))
                    self.return_to_start()
            elif char in Constants.VALID_IDENTIFIER_SYMBOLS:
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.ALPHABETIC:
                    self.append_to_buffer(char)
                else:
                    self.append_to_buffer(char)
                    self.add_to_lexicon(''.join(self.buffer), LexerToken.INVALID)
                    self.errors.append(Error(ErrorTypes.INVALID, len(self.lexicon) - 1))
                    self.return_to_start()
            elif char in Constants.VALID_SEPARATORS:
                if ''.join(self.buffer) == "std" or ''.join(self.buffer) == "std:":
                    self.append_to_buffer(char)
                elif self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                else:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.current_pos['pos'] = self.current_pos['pos'] + 1
                    self.add_to_lexicon(char, LexerToken.SEPARATOR)
                    self.current_pos['pos'] = self.current_pos['pos'] - 1
                    self.return_to_start()
            elif char in Constants.VALID_OPERATORS:
                self.current_pos['pos'] = self.current_pos['pos'] + 1
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                else:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.OPERATOR)
                    self.return_to_start()
                self.current_pos['pos'] = self.current_pos['pos'] - 1
            elif char == Constants.SLASH:
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                elif self.current_state != LexerState.SLASH:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.current_state = LexerState.SLASH
                else:
                    self.current_state = LexerState.START
                    break
            elif char in Constants.VALID_STRING:
                if self.current_state != LexerState.STRING:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.OPERATOR)
                    self.current_state = LexerState.STRING
                else:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.OPERATOR)
                    self.current_state = LexerState.START
            elif char == " ":
                if self.current_state == LexerState.STRING:
                    self.append_to_buffer(char)
                else:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.return_to_start()
            elif char == '\n':
                self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                self.current_state = LexerState.START
                self.buffer.clear()
            else:
                if self.current_state != LexerState.STRING:
                    self.analyse_nonsymbol_lexeme(''.join(self.buffer))
                    self.add_to_lexicon(char, LexerToken.NOT_EXISTS)
                    self.errors.append(Error(ErrorTypes.NOT_EXISTS, len(self.lexicon)-1))
                    self.return_to_start()
                else:
                    self.append_to_buffer(char)
            self.current_pos['pos'] = self.current_pos['pos'] + 1

    def return_to_start(self):
        self.current_state = LexerState.START
        self.buffer.clear()

    @staticmethod
    def is_keyword(lexeme):
        if lexeme in Constants.VALID_KEYWORDS:
            return True
        else:
            return False

    @staticmethod
    def is_boolean(lexeme):
        if lexeme in Constants.VALID_BOOLEAN_VALUES:
            return True
        else:
            return False

    def append_to_buffer(self, char):
        self.buffer.append(char)

    def analyse_nonsymbol_lexeme(self, lexeme):
        if self.current_state == LexerState.STRING:
            self.add_to_lexicon(lexeme, LexerToken.STRING)
        elif self.current_state == LexerState.INTEGER:
            self.add_to_lexicon(lexeme, LexerToken.INTEGER)
        elif self.current_state == LexerState.REAL:
            self.add_to_lexicon(lexeme, LexerToken.REAL)
        elif self.current_state == LexerState.ALPHABETIC:
            if self.is_keyword(lexeme):
                self.add_to_lexicon(lexeme, LexerToken.KEYWORD)
            elif self.is_boolean(lexeme):
                self.add_to_lexicon(lexeme, LexerToken.BOOLEAN)
            else:
                self.add_to_lexicon(lexeme, LexerToken.IDENTIFIER)

    def add_to_lexicon(self, token, lexeme):
        new_listing = Listing(token, lexeme)
        self.positions.append(self.current_pos.copy())
        self.lexicon.append(new_listing)

    def create_string_output(self):
        result = ''
        result += ("{:<3} {:<12} {:<24}\n\n".format("ID", "TOKENS", "LEXEMES"))
        i = 0
        for entry in self.lexicon:
            result += ("{:<3} {:<12} {:<24}\n".format(i, entry.token.name, entry.lexeme))
            i += 1
        return result
