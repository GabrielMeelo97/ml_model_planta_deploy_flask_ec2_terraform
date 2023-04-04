# Aplicação Web e API REST

# Versão da Linguagem Python
from platform import python_version
print('Versão da Linguagem Python Usada:', python_version())

# Para atualizar um pacote, execute o comando abaixo no terminal ou prompt de comando:
# pip install -U nome_pacote

# Para instalar a versão exata de um pacote, execute o comando abaixo no terminal ou prompt de comando:
# pip install nome_pacote==versão_desejada

# Imports
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from tensorflow.keras import backend
from tensorflow.keras.models import load_model

# Cria o objeto da app
app = Flask(__name__)

# Carrega o modelo treinado
@app.before_first_request
def load_model_to_app():
    app.predictor = load_model('./static/model/modelo1.h5')
    
# Responde as requisições para o diretório raiz (/) com index.html
@app.route("/")
def index():
    return render_template('index.html', pred = " ")

# Para as previsões usamos o método POST para enviar as variáveis de entrada ao modelo
@app.route('/predict', methods = ['POST'])
def predict():

    # Objeto com as variáveis de entrada que vieram a através do formulário
    data = [request.form['sepal_length'],
            request.form['sepal_width'],
            request.form['petal_length'], 
            request.form['petal_width']]

    # Converte para o tipo array
    data = np.array([np.asarray(data, dtype = float)])

    # Coleta as previsões
    predictions = app.predictor.predict(data)
    print('\nPrevisões de Probabilidades: {}'.format(predictions))

    # Como são retornadas probabilidades, extraímos a maior, que indica a categoria da planta
    tipo = np.where(predictions == np.amax(predictions, axis = 1))[1][0]
    print('\nPrevisão de Classe:', tipo)

    if tipo == 0:
        pred_planta = 'Setosa'

    if tipo == 1:
        pred_planta = 'Versicolor'

    if tipo == 2:
        pred_planta = 'Virginica'

    # Entrega na página web as previsões
    return render_template('index.html', pred = pred_planta)

# Função main para execução do programa
def main():
    app.run(host = '0.0.0.0', port = 8080, debug = False)  


# Execução do programa
if __name__ == '__main__':
    main()

