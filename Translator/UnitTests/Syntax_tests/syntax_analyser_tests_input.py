from Translator.Lexer.lexer import Lexer
from Translator.Constants.constants import *

input_code = []
input_code.append('''
    int main(){
        int a = 5
        return a;                        
    }''')
input_code.append('''
    int main(){
        int a = 5 +
        return a;                        
    }''')
input_code.append('''
    int func( b){
        int a = 3;
        return b;
    }
    int main(){
        int a = 3;
        if (a<5){
            return a;}
    }
''')
input_code.append('''
    int {int a = 5 + 6;
    return a; }                       
    ''')
input_code.append('''
    int main(){
        int  = 5 + 6;
        return a; 
    }''')
input_code.append('''
    int main() {
        for (i = 0; i < 10; i = i + 1) {
            i = i + 1;
        }
    }''')
input_code.append('''
    int main() {
        int a = 3;
        (a<5){
        return a;}
    }''')
input_code.append('''
    int main() {
        int a  3;
        return a;
    }''')
input_code.append('''
    int main(){
        int a = 4;
        if (a !> 2) {
        return a;
        }
    }''')

input_code.append('''
    int main(){
        int a = %;
        return a;
    }''')



def get_syntax_analyser_test_input(i):
    lexer = Lexer()
    lexer.parse(input_code[i])
    lexer.lexicon.append(Constants.TOKEN_END_OF_LINE)
    return lexer
