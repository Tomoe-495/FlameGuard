from django.shortcuts import render
import pickle
import warnings
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

warnings.filterwarnings('ignore')
scaler = MinMaxScaler()

data = pd.read_csv('forestfires.csv')
data = data.drop(['X', 'Y', 'month', 'day', 'FFMC', 'DMC', 'DC', 'ISI', 'rain'], axis=1)
X = data[['temp', 'RH', 'wind']]  # Features
data['fire'] = data['area'].apply(lambda x: 1 if x > 0 else 0)
y = data['fire']  # New binary target

data = data.drop(['area'], axis=1)

# Normalize the feature data
X_scaled = scaler.fit_transform(X)


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def fire_prediction(temp, humidity, oxygen):
  input_data = [[temp, humidity, oxygen]]
  input_data = scaler.transform(input_data)
  prediction = model.predict(input_data)
  return f'{prediction[0]:.2f}'

# Create your views here.
def home(request):
    return render(request, 'home.html', {'result': 0})


def get_prediction(request):
    output = 0
    if request.method == 'POST':

        temp = int(request.POST.get('temp'))
        oxygen = int(request.POST.get('oxy'))
        humidity = int(request.POST.get('hum'))

        output = fire_prediction(temp, humidity, oxygen)

    return render(request, 'home.html', {'result':output})
