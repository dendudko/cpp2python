import unittest

from Translator.SyntaxAnalyser.syntax_analyser import SyntaxAnalyserRDP
from syntax_analyser_tests_input import *


class SyntaxAnalyserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.SyntaxAnalyser = SyntaxAnalyserRDP()


    # Проверяем, что будет при отсутствии ;
    def testSyntaxAnalyserMissing(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(0)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'MISSING')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 8)

    # Проверяем, что будет при незаконченном выражении
    def testSyntaxAnalyserInvExp(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(1)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'INVALID_EXP')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 9)

    # Проверяем, что будет при незаконченной инициализации параметров функции
    def testSyntaxAnalyserExpInit(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(2)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'EXPECTED_INIT')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 2)

    # Проверяем, что будет если не объявить функцию
    def testSyntaxAnalyserExpDec(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(3)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'EXPECTED_DEC')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 0)

    # Проверяем, что будет если не объявить переменную
    def testSyntaxAnalyserInvalidId(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(4)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'INVALID_ID')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 5)

    # Проверяем, что будет если не объявить переменную в цикле
    def testSyntaxAnalyserWrongType(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(5)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'WRONG_TYPE')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 6)

    # Проверяем, что будет если не объявить ключевое слово цикла
    def testSyntaxAnalyserExpStat1(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(6)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'EXPECTED_STAT')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 9)

    # Проверяем, что будет если не объявить операор между выражениями
    def testSyntaxAnalyserExpStat2(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(7)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'EXPECTED_STAT')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 6)

    # Проверяем, что будет если указать несуществующий оператор между выражениями
    def testSyntaxAnalyserExpStat3(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(8)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'UNRECOGNIZED')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 13)

    # Проверяем, что будет если встретиться неизвестный символ
    def testSyntaxAnalyserExpStat3(self):
        input_for_syntax_analyser = get_syntax_analyser_test_input(9)
        self.SyntaxAnalyser.parse(input_for_syntax_analyser.lexicon, input_for_syntax_analyser.positions,
                                  input_for_syntax_analyser.errors)
        self.assertEqual(self.SyntaxAnalyser.errors[0].type.name, 'NOT_EXISTS')
        self.assertEqual(self.SyntaxAnalyser.errors[0].index, 8)


if __name__ == 'main':
    unittest.main()
