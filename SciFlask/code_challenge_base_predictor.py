import numpy as np
import sklearn
from joblib import load

class Predictor():
    def __init__(self):
        self.model = load('./code_challenge_model.p')
        

    def predict(self,input_data):
        return self.model.predict_proba([input_data])
