from flask import render_template, request, session

from Translator.TranslatorController import translator_controller
from flask_app import app


@app.route('/')
def index():
    syntax_error = None
    semantic_error = None
    input_code = ''
    lexer_data = ''
    syntax_data = ''
    semantic_data = ''
    output_code = ''
    if request.values.get('translate'):
        with open('Translator/InputBuffer/input_buffer.txt', 'w') as f:
            f.write(request.values.get('input_code').replace('\r', '').replace('\t', '    '))
        input_code = ''
        with open('Translator/InputBuffer/input_buffer.txt', 'r') as f:
            for line in f:
                input_code += line
        # Читаем результаты работы транслятора
        lexer_data, syntax_data, semantic_data, output_code, syntax_error, semantic_error = translator_controller.main()
    html = render_template(
        'index.html',
        input_code=input_code,
        int=int,
        lexer=lexer_data,
        syntax=syntax_data,
        semantic=semantic_data,
        output_code=output_code,
        syntax_error=syntax_error,
        semantic_error=semantic_error,
        len=len
    )
    return html
