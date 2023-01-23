import os

from Translator.CodeGenerator.code_generator import CodeGenerator
from Translator.Constants.constants import *
from Translator.Lexer.lexer import Lexer
from Translator.SemanticAnalyser.semantic_analyser import SemanticAnalyser
from Translator.SyntaxAnalyser.syntax_analyser import SyntaxAnalyserRDP


class TranslatorController:
    def __init__(self):
        self.lexer = Lexer()
        self.syntax_analyser = SyntaxAnalyserRDP()
        self.semantic_analyser = SemanticAnalyser()
        self.code_generator = CodeGenerator()

    def parse(self):
        syntax_error = False
        semantic_error = False
        if os.path.exists('Translator/InputBuffer/input_buffer.txt'):
            with open('Translator/InputBuffer/input_buffer.txt', 'r') as f:
                for line in f:
                    if line != "\n":
                        self.lexer.parse(line)
                    else:
                        self.lexer.current_pos['row'] = self.lexer.current_pos['row'] + 1

                self.lexer.lexicon.append(Constants.TOKEN_END_OF_LINE)
                if len(self.lexer.positions) > 1:
                    self.lexer.positions.append(
                        {'row': self.lexer.positions[-1]['row'], 'pos': self.lexer.positions[-1]['pos'] + 1})
                self.syntax_analyser.parse(self.lexer.lexicon, self.lexer.positions, self.lexer.errors)
                step_1 = self.lexer.create_string_output()
                step_2 = self.syntax_analyser.create_string_output()
                self.semantic_analyser.parse(self.syntax_analyser.tokens, self.syntax_analyser.positions,
                                             self.syntax_analyser.errors)
                step_3 = self.semantic_analyser.create_string_output()
                self.code_generator.parse(self.lexer.lexicon, self.syntax_analyser.errors,
                                          self.semantic_analyser.errors)
                step_4 = self.code_generator.create_string_output()
                if len(self.syntax_analyser.errors) > 0 and len(self.syntax_analyser.output) > 0:
                    step_4 += 'SYNTAX ANALYSER:\n' + self.syntax_analyser.output[-1]
                    syntax_error = True
                elif len(self.semantic_analyser.errors) > 0 and len(self.semantic_analyser.output) > 0:
                    step_4 += 'SEMANTIC ANALYSER:\n' + self.semantic_analyser.output[-1]
                    semantic_error = True
                return step_1, step_2, step_3, step_4, syntax_error, semantic_error


def main():
    p = TranslatorController()
    return p.parse()
