import os
import sys
import numpy as np
import pandas as pd
import joblib
from src.exception import CustomException


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path, "wb") as file_obj:
            joblib.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e,sys)
    
def load_object(file_path):
    try:
        obj = joblib.load(file_path)
        return obj
    except Exception as e:
        raise CustomException(e,sys)
    
def kelly_criterion_fraction(probability, odds, fraction=1.0):
    """
    Calcula a fração do Critério de Kelly para o dimensionamento ideal da aposta.

    Parâmetros:
    - odds: Odds decimais (por exemplo, 2.0 para odds iguais, 3.0 para odds de 2:1, etc.).
    - probabilidade: Probabilidade de vitória (deve estar entre 0 e 1).
    - fração: Fração do bankroll atual a considerar (padrão é 1.0).

    Retorna:
    - A fração do bankroll atual a apostar de acordo com o Critério de Kelly.
    """
    try:
        b = odds - 1 
        q = 1 - probability
        kelly = (b * probability - q) / b
        
        kelly_fraction = fraction*kelly
        return kelly_fraction
    except Exception as e:
        raise CustomException(e,sys)

def suggest_bet(prob_w, odds_w, odds_l, bankroll, k=0.75, max_vlr_aposta=230):
    try:
        prob_l = 1-prob_w
        if prob_w >= 0.8 and (prob_w - (1/odds_w)) >= 0.2:            
            f_star_w = kelly_criterion_fraction(prob_w, odds_w, k) # Kelly apostando na vitoria
            f_star_w = f_star_w if f_star_w > 0 else 0
            stake_w = np.min([f_star_w*bankroll, max_vlr_aposta])
        else:
            stake_w = 0

        if prob_l >= 0.3 and (prob_l - (1/odds_l)) >= 0.4:            
            f_star_l = kelly_criterion_fraction(prob_l, odds_l, k) # Kelly apostando na derrota
            f_star_l = f_star_l if f_star_l > 0 else 0
            stake_l = np.min([f_star_l*bankroll, max_vlr_aposta])
        else:
            stake_l = 0
        
        return stake_w, stake_l

    except Exception as e:
        raise CustomException(e,sys)
