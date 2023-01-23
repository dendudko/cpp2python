from flask import Flask

app = Flask(__name__, template_folder='./Web/templates/', static_folder='./Web/static/')
app.secret_key = b'_5#y2L"F4Q8hui\n\xec]/'

import Web.controllers.index
