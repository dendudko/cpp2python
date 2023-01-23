from Translator.Lexer.lexer import Lexer
from Translator.Constants.constants import *
import unittest


class LexerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.Lexer = Lexer()
        with (open('lexer_tests_input', 'r')) as f:
            for line in f:
                self.Lexer.parse(line)

    # Тесты для операторов
    def testPlus(self):
        self.assertIn(self.Lexer.lexicon[0].lexeme, Constants.VALID_OPERATORS)
        self.assertEqual(self.Lexer.lexicon[0].token, LexerToken.OPERATOR)

    def testMinus(self):
        self.assertIn(self.Lexer.lexicon[1].lexeme, Constants.VALID_OPERATORS)
        self.assertEqual(self.Lexer.lexicon[1].token, LexerToken.OPERATOR)

    def testEqual(self):
        self.assertIn(self.Lexer.lexicon[2].lexeme, Constants.VALID_OPERATORS)
        self.assertEqual(self.Lexer.lexicon[2].token, LexerToken.OPERATOR)

    def testMultiply(self):
        self.assertIn(self.Lexer.lexicon[3].lexeme, Constants.VALID_OPERATORS)
        self.assertEqual(self.Lexer.lexicon[3].token, LexerToken.OPERATOR)

    def testForwardSlash(self):
        self.assertIn(self.Lexer.lexicon[4].lexeme, Constants.SLASH)
        self.assertEqual(self.Lexer.lexicon[4].token, LexerToken.OPERATOR)

    def testLess(self):
        self.assertIn(self.Lexer.lexicon[5].lexeme, Constants.VALID_OPERATORS)
        self.assertEqual(self.Lexer.lexicon[5].token, LexerToken.OPERATOR)

    def testMore(self):
        self.assertIn(self.Lexer.lexicon[6].lexeme, Constants.VALID_OPERATORS)
        self.assertEqual(self.Lexer.lexicon[6].token, LexerToken.OPERATOR)

    def testExclamationMark(self):
        self.assertIn(self.Lexer.lexicon[7].lexeme, Constants.VALID_OPERATORS)
        self.assertEqual(self.Lexer.lexicon[7].token, LexerToken.OPERATOR)

    def testSingleQuotes(self):
        self.assertIn(self.Lexer.lexicon[8].lexeme, Constants.VALID_STRING)
        self.assertEqual(self.Lexer.lexicon[8].token, LexerToken.OPERATOR)

    def testDoubleQuotes(self):
        self.assertIn(self.Lexer.lexicon[11].lexeme, Constants.VALID_STRING)
        self.assertEqual(self.Lexer.lexicon[11].token, LexerToken.OPERATOR)

    # Тесты для разделителей
    def testOpenParenthesis(self):
        self.assertIn(self.Lexer.lexicon[14].lexeme, Constants.VALID_SEPARATORS)
        self.assertEqual(self.Lexer.lexicon[14].token, LexerToken.SEPARATOR)

    def testClosedParenthesis(self):
        self.assertIn(self.Lexer.lexicon[15].lexeme, Constants.VALID_SEPARATORS)
        self.assertEqual(self.Lexer.lexicon[15].token, LexerToken.SEPARATOR)

    def testOpenSquareBracket(self):
        self.assertIn(self.Lexer.lexicon[16].lexeme, Constants.VALID_SEPARATORS)
        self.assertEqual(self.Lexer.lexicon[16].token, LexerToken.SEPARATOR)

    def testCloseSquareBracket(self):
        self.assertIn(self.Lexer.lexicon[17].lexeme, Constants.VALID_SEPARATORS)
        self.assertEqual(self.Lexer.lexicon[17].token, LexerToken.SEPARATOR)

    def testOpenCurlyBrace(self):
        self.assertIn(self.Lexer.lexicon[18].lexeme, Constants.VALID_SEPARATORS)
        self.assertEqual(self.Lexer.lexicon[18].token, LexerToken.SEPARATOR)

    def testCloseCurlyBrace(self):
        self.assertIn(self.Lexer.lexicon[19].lexeme, Constants.VALID_SEPARATORS)
        self.assertEqual(self.Lexer.lexicon[19].token, LexerToken.SEPARATOR)

    def testComma(self):
        self.assertIn(self.Lexer.lexicon[20].lexeme, Constants.VALID_SEPARATORS)
        self.assertEqual(self.Lexer.lexicon[20].token, LexerToken.SEPARATOR)

    def testSemiColon(self):
        self.assertIn(self.Lexer.lexicon[21].lexeme, Constants.VALID_EOL_SYMBOLS)
        self.assertEqual(self.Lexer.lexicon[21].token, LexerToken.SEPARATOR)

    def testColon(self):
        self.assertIn(self.Lexer.lexicon[22].lexeme, Constants.VALID_SEPARATORS)
        self.assertEqual(self.Lexer.lexicon[22].token, LexerToken.SEPARATOR)

    # Тесты для ключевых слов
    def testInt(self):
        self.assertIn(self.Lexer.lexicon[23].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[23].token, LexerToken.KEYWORD)

    def testFloat(self):
        self.assertIn(self.Lexer.lexicon[24].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[24].token, LexerToken.KEYWORD)

    def testBool(self):
        self.assertIn(self.Lexer.lexicon[25].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[25].token, LexerToken.KEYWORD)

    def testIf(self):
        self.assertIn(self.Lexer.lexicon[26].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[26].token, LexerToken.KEYWORD)

    def testElse(self):
        self.assertIn(self.Lexer.lexicon[27].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[27].token, LexerToken.KEYWORD)

    def testWhile(self):
        self.assertIn(self.Lexer.lexicon[28].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[28].token, LexerToken.KEYWORD)

    def testDouble(self):
        self.assertIn(self.Lexer.lexicon[29].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[29].token, LexerToken.KEYWORD)

    def testStdString(self):
        self.assertIn(self.Lexer.lexicon[30].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[30].token, LexerToken.KEYWORD)

    def testVoid(self):
        self.assertIn(self.Lexer.lexicon[31].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[31].token, LexerToken.KEYWORD)

    def testReturn(self):
        self.assertIn(self.Lexer.lexicon[32].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[32].token, LexerToken.KEYWORD)

    def testFor(self):
        self.assertIn(self.Lexer.lexicon[33].lexeme, Constants.VALID_KEYWORDS)
        self.assertEqual(self.Lexer.lexicon[33].token, LexerToken.KEYWORD)

    # Тесты для типов
    def testNumber(self):
        self.assertEqual(self.Lexer.lexicon[34].token, LexerToken.INTEGER)

    def testRealNumber(self):
        self.assertEqual(self.Lexer.lexicon[35].token, LexerToken.REAL)

    def testFalse(self):
        self.assertIn(self.Lexer.lexicon[36].lexeme, Constants.VALID_BOOLEAN_VALUES)
        self.assertEqual(self.Lexer.lexicon[36].token, LexerToken.BOOLEAN)

    def testTrue(self):
        self.assertIn(self.Lexer.lexicon[37].lexeme, Constants.VALID_BOOLEAN_VALUES)
        self.assertEqual(self.Lexer.lexicon[37].token, LexerToken.BOOLEAN)

    def testFirstString(self):
        self.assertIn(self.Lexer.lexicon[8].lexeme, Constants.VALID_STRING)
        self.assertEqual(self.Lexer.lexicon[8].token, LexerToken.OPERATOR)
        self.assertEqual(self.Lexer.lexicon[9].token, LexerToken.STRING)
        self.assertIn(self.Lexer.lexicon[10].lexeme, Constants.VALID_STRING)
        self.assertEqual(self.Lexer.lexicon[10].token, LexerToken.OPERATOR)

    def testSecondString(self):
        self.assertIn(self.Lexer.lexicon[11].lexeme, Constants.VALID_STRING)
        self.assertEqual(self.Lexer.lexicon[11].token, LexerToken.OPERATOR)
        self.assertEqual(self.Lexer.lexicon[12].token, LexerToken.STRING)
        self.assertIn(self.Lexer.lexicon[13].lexeme, Constants.VALID_STRING)
        self.assertEqual(self.Lexer.lexicon[13].token, LexerToken.OPERATOR)

    # тесты для других символов
    def testTilde(self):
        self.assertEqual(self.Lexer.lexicon[38].token, LexerToken.NOT_EXISTS)

    def testDollar(self):
        self.assertIn(self.Lexer.lexicon[39].lexeme, Constants.VALID_IDENTIFIER_SYMBOLS)
        self.assertEqual(self.Lexer.lexicon[39].token, LexerToken.INVALID)

    def testSlovo(self):
        self.assertEqual(self.Lexer.lexicon[40].token, LexerToken.IDENTIFIER)


if __name__ == "main":
    unittest.main()
