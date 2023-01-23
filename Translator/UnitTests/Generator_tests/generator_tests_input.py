from Translator.Lexer.lexer import Lexer
from Translator.SemanticAnalyser.semantic_analyser import *
from Translator.SyntaxAnalyser.syntax_analyser import *

input_code = []

input_code.append('''
    int main(){
        int a = 0;
        for (int i = 1; i < 10; i = i + 2){
            a = a + i;}
        int b = a;
        
        for (int i = 1; i <= 10 ; i = i + 1 ){
            b = b + 1;}
        int c = b;
    
        for (int i = 12; i > 1; i = i - 2){
            c = c + i;}
        int d = c;    
    
        for (int i = 12; i >= 5; i = i - 1){
            d = d + i;}
        int e = d;
    }''')
input_code.append('''
    int main(){
        int a = 10;
        if (a < 15){ 
            a = 0;}
        int b = a;
    }''')
input_code.append('''
   int main(){
        int a = 10;
        if (a < 15){ 
            a = 0;}
        else {a = a + 10; }
        int b = a;
    }''')
input_code.append('''
    int main(){
        int a = 10;
            while (a<=100)
                {a = a + 10;}
        int b = a;
    }''')
input_code.append('''
    int func1(int a){
        if (a < 15){a = 0;}
        else {a = a + 10; }
        return a;
    }
    
    int func2(int c){
        c=c+5;
        return c;
    }
    
    int main(){
        int a = 10;
        int b = func1(a);
        int c = a + func2(b);
    }''')
input_code.append('''
int (int a){
    a=a+5;
    return a;
}

int main(){
    int a = 10;
    int b = func1(a);
    int c = a + b;
}''')
input_code.append('''
    int func1(int c){
        c=c+5;
        return c;
    }
    
    int main(){
        a = 10;
        int b = func1(a);
        int c = a + b;
    }''')
input_code.append('''
    int func1(int a){
        for (int i = 1; i < 10; i = i + 2){
            a = a + i;}
        int b = a;
        
        for (int i = 1; i <= 10; i = i + 1 ){
            b = b + 1;}
        int c = b;
        
        for (int i = 12; i > 1; i = i - 2){
            c = c + i;}
        int d = c;    
        
        for (int i = 12; i >= 5; i = i - 1){
            d = d + i;}
        int e = d;
    
        return e;
    }
    

     int func2(int a){
        a = a + 1;
        return a;
    }

    int main() {
        int a = 3;
        int b = func1(a);
        int c = 15; 
        int d = 0;
    
        for (int i = 1; i <= 5; i = i + 1) { 
            for (int j = 5; j < 10; j = j + 2){ 
                for (int k = 10; k > 12; k = k - 2) { 
                    c = c + k;
                    c = c - i;
                    if (c < 30){b = b + j ;} 
                }                
            }
            d = d + 1;
        }
        while (d <= 20) {
            int e = 10;
            while (e >= 5){
                d = func2(d);
                e = e - 1;
            }
            d = d + 1;
        }
    }''')


def get_code_generator_tests_input(i):
    lexer = Lexer()
    syntax = SyntaxAnalyserRDP()
    semantic = SemanticAnalyser()
    lexer.parse(input_code[i])
    lexer.lexicon.append(Constants.TOKEN_END_OF_LINE)
    syntax.parse(lexer.lexicon, lexer.positions, lexer.errors)
    semantic.parse(syntax.tokens, syntax.positions, syntax.errors)

    return lexer.lexicon, semantic.errors, syntax.errors
