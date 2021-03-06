from flask_basicauth import BasicAuth
from flask import Flask, request, jsonify
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle
import os

colunas = ['tamanho', 'ano', 'garagem']
modelo = pickle.load(open('models/modelo.sav', 'rb'))

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/')  # Definindo a rota 
def home():
    return '<h1>Minha primeira API!</h1>'

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to="en")
    return  "Polaridade: " + str(tb_en.sentiment.polarity)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input]) 
    return jsonify(preco = preco[0])

app.run(debug=True, host="0.0.0.0")  # Executando o app