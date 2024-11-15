from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '¡Hola, mundo! Esta es una respuesta a una solicitud GET.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
