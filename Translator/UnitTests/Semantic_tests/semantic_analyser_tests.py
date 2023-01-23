import unittest

from Translator.SemanticAnalyser.semantic_analyser import SemanticAnalyser
from semantic_analyser_tests_input import *


class SemanticAnalyserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.SemanticAnalyser = SemanticAnalyser()

    # Проверяем, что будет когда переменная не инициализирована
    def testSemanticAnalyserNotInit(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(0)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'NOT_INITIALIZE')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 5)

    # Проверяем, что будет когда вызывается переменная, инициализированная в цикле, вне цикла (область видимости переменной)
    def testSemanticAnalyserNotInit2(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(1)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'NOT_INITIALIZE')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 30)

    # Проверяем, что будет если присвоить переменной одного типа значение другого типа
    def testSemanticAnalyserWrongType(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(2)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'WRONG_TYPE')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 8)

    # Проверяем, что будет если не объявлена main функция
    def testSemanticAnalyserMissMain(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(3)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'MISSING_MAIN')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 10)

    # Проверяем, что будет если повторно объявить переменную
    def testSemanticAnalyserReInit(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(4)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'REINITIALIZE')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 11)

    # Проверяем, что будет когда переменная типа string содержит оператор
    def testSemanticAnalyserInvId(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(5)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'INVALID_ID')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 12)

    # Проверяем, что будет если передавать в функцию неверное количество параметров
    def testSemanticAnalyserWrongCount1(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(6)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'WRONG_COUNT')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 32)

    def testSemanticAnalyserWrongCount2(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(7)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'WRONG_COUNT')

    def testSemanticAnalyserWrongCount3(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(8)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'WRONG_COUNT')

    def testSemanticAnalyserWrongCount4(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(9)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'WRONG_COUNT')

    # Проверяем, что будет если передать в функцию параметры неправильного типа
    def testSemanticAnalyserWrongType2(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(10)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'WRONG_TYPE')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 35)

 # Проверяем, что будет если вызвать функцию до ее объявления
    def testSemanticAnalyserNotInit3(self):
        input_for_semantic_analyser = get_semantic_analyser_test_input(11)
        self.SemanticAnalyser.parse(input_for_semantic_analyser.tokens, input_for_semantic_analyser.positions,
                                    input_for_semantic_analyser.errors)
        self.assertEqual(self.SemanticAnalyser.errors[0].type.name, 'NOT_INITIALIZE')
        self.assertEqual(self.SemanticAnalyser.errors[0].index, 8)


if __name__ == 'main':
    unittest.main()
