# Modelo de Deep Learning

# Imports
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Nomes das colunas
nomes_colunas = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Species']

# Dataset
# https://archive.ics.uci.edu/ml/datasets/Iris
dados = pd.read_csv('https://raw.githubusercontent.com/dsacademybr/Datasets/master/dataset3.csv', names = nomes_colunas, header = 0)

# Separa as variáveis de entrada e saída
saida = dados["Species"].astype("category")
entrada = dados.drop("Species", axis = 1)

# Encoding da variável target (conversão de texto para número)
dataEncoder = LabelEncoder()
saida_num = dataEncoder.fit_transform(saida)

# Divide os dados em treino e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(entrada, saida_num, test_size = 0.3, random_state = 42)

# Converte a variável de saída em tipo categórico
y_treino = to_categorical(y_treino)
y_teste = to_categorical(y_teste)

# Modelo de Deep Learning
modelo = Sequential()
modelo.add(Dense(10, input_dim = 4, activation = 'relu'))
modelo.add(Dense(10, activation = 'relu'))
modelo.add(Dense(3, activation = 'softmax'))

# Compilação do modelo
modelo.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# Treinamento do modelo
modelo.fit(X_treino, y_treino, epochs = 300, batch_size = 10)

# Avalia o modelo
scores = modelo.evaluate(X_teste, y_teste)
print("\nAcurácia: %.2f%%" % (scores[1]*100))

# Salva o modelo
modelo.save('modelos/modelo1.h5')

