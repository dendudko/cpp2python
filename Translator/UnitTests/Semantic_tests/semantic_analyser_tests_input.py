from Translator.Lexer.lexer import Lexer
from Translator.SyntaxAnalyser.syntax_analyser import *

input_code = []

input_code.append('''
    int main(){
    a = 5 + 6;
    return a; 
    }''')
input_code.append('''
    int main() {
        for (int i = 0; i < 10; i = i + 1) {
            i = i + 1;
        }
        i = 4;
    }''')
input_code.append('''
   int main(){
        std::string a = 5;
        return a;
    }''')
input_code.append('''
    int hui(){
        int a = 5;
    }''')
input_code.append('''
    int main(){
        int a = 5;
        std::string a = 'abc';
        return a;
    }''')
input_code.append('''
    int main(){
        std::string a = 'a'+'bc';
    }''')
input_code.append('''
    int func(int a, int b){
        if (a>b){
        return a;
        }
    }
    int main(){
        int a = func();
    }''')
input_code.append('''
    int func(int a, int b){
        if (a>b){
        return a;
        }
    }
    int main(){
        int a = func(1);
    }''')
input_code.append('''
    int func(int a, int b){
        if (a>b){
        return a;
        }
    }
    int main(){
        int a = func(1, 2, 3);
    }''')
input_code.append('''
    int func(){
        return 5;
    }
    int main(){
        int a = func(1);
    }''')
input_code.append('''
     int func(int a, int b){
        if (a>b){
        return a;
        }
    }
    int main(){
        int a = func(1, 'hello');
    }''')
input_code.append('''
     int main(){
        int a = func(1, 2);
    }

    int func(int a, int b){
        if (a>b){
        return a;
        }
    }''')

def get_semantic_analyser_test_input(i):
    lexer = Lexer()
    syntax = SyntaxAnalyserRDP()
    lexer.parse(input_code[i])
    lexer.lexicon.append(Constants.TOKEN_END_OF_LINE)
    syntax.parse(lexer.lexicon, lexer.positions, lexer.errors)
    return syntax
