import numpy as np
import sklearn
from joblib import load

class Predictor():
    def __init__(self):
        self.model = load('./code_challenge_model.p')
        print("Booted up model")

    def predict(self,input_data):
        # this is just a suggestion, feel free to change
        return self.model.predict_proba([input_data])
