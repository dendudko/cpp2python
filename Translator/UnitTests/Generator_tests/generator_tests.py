import unittest

from Translator.CodeGenerator.code_generator import CodeGenerator
from generator_tests_input import *


class CodeGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.CodeGenerator = CodeGenerator()

    def testCodeGeneratorFor(self):
        with open("Expected_output_for_tests/code_generator_test_output_FOR.txt") as file:
            expected_output = file.read()
        a, b, c = get_code_generator_tests_input(0)
        self.CodeGenerator.parse(a, b, c)
        self.assertEqual(self.CodeGenerator.create_string_output(), expected_output)

    def testCodeGeneratorIf(self):
        with open("Expected_output_for_tests/code_generator_test_output_IF.txt") as file:
            expected_output = file.read()
        a, b, c = get_code_generator_tests_input(1)
        self.CodeGenerator.parse(a, b, c)
        self.assertEqual(self.CodeGenerator.create_string_output(), expected_output)

    def testCodeGeneratorIfElse(self):
        with open("Expected_output_for_tests/code_generator_test_output_IF_ELSE.txt") as file:
            expected_output = file.read()
        a, b, c = get_code_generator_tests_input(2)
        self.CodeGenerator.parse(a, b, c)
        self.assertEqual(self.CodeGenerator.create_string_output(), expected_output)

    def testCodeGeneratorWhile(self):
        with open("Expected_output_for_tests/code_generator_test_output_WHILE.txt") as file:
            expected_output = file.read()
        a, b, c = get_code_generator_tests_input(3)
        self.CodeGenerator.parse(a, b, c)
        self.assertEqual(self.CodeGenerator.create_string_output(), expected_output)

    def testCodeGeneratorFunctions(self):
        with open("Expected_output_for_tests/code_generator_test_output_FUNCTIONS.txt") as file:
            expected_output = file.read()
        a, b, c = get_code_generator_tests_input(4)
        self.CodeGenerator.parse(a, b, c)
        self.assertEqual(self.CodeGenerator.create_string_output(), expected_output)

    def testCodeGeneratorErrorSyntax(self):
        with open("Expected_output_for_tests/code_generator_test_output_ERROR_SYNTAX.txt") as file:
            expected_output = file.read()
        a, b, c = get_code_generator_tests_input(5)
        self.CodeGenerator.parse(a, b, c)
        self.assertEqual(self.CodeGenerator.create_string_output(), expected_output)

    def testCodeGeneratorErrorSemantic(self):
        with open("Expected_output_for_tests/code_generator_test_output_ERROR_SEMANTIC.txt") as file:
            expected_output = file.read()
        a, b, c = get_code_generator_tests_input(6)
        self.CodeGenerator.parse(a, b, c)
        self.assertEqual(self.CodeGenerator.create_string_output(), expected_output)

    def testCodeGeneratorSuperTest(self):
        with open("Expected_output_for_tests/code_generator_test_output_SUPER_TEST.txt") as file:
            expected_output = file.read()
        a, b, c = get_code_generator_tests_input(7)
        self.CodeGenerator.parse(a, b, c)
        self.assertEqual(self.CodeGenerator.create_string_output(), expected_output)


if __name__ == 'main':
    unittest.main()
