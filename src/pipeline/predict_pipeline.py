import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object, kelly_criterion_fraction, suggest_bet
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            vars_final = [
                'med_perc_chutes_com_6_man',
                'diff_colocacao_adv_man',
                'colocacao_man',
                'med_perc_defesas_com_6_man',
                'colocacao_vis',
                'med_perc_gols_sof_6_vis',
                'med_perc_defesas_com_3_man',
                'med_perc_chutes_com_6_vis'
            ]
            model_path = 'artifacts/model_f.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            data_scaled=preprocessor.transform(features[vars_final])
            preds=model.predict_proba(data_scaled)[:,1]

            prob_w = preds[0]
            odds_w = features['odds_w'].values[0]
            odds_l = features['odds_l'].values[0]
            bankroll = features['bankroll'].values[0]
            bet_w, bet_l = suggest_bet(prob_w, odds_w, odds_l, bankroll)                        
            
            return prob_w, bet_w, bet_l
        
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self,
                 med_perc_chutes_com_6_man: float,
                #  diff_colocacao_adv_man: float,
                 colocacao_man: float,
                 med_perc_defesas_com_6_man: float,
                 colocacao_vis: float,
                 med_perc_gols_sof_6_vis: float,
                 med_perc_defesas_com_3_man: float,
                 med_perc_chutes_com_6_vis: float,
                 odds_w: float,
                 odds_l: float,
                 bankroll: float):
        
        self.med_perc_chutes_com_6_man = med_perc_chutes_com_6_man
        self.diff_colocacao_adv_man = colocacao_man - colocacao_vis
        self.colocacao_man = colocacao_man
        self.med_perc_defesas_com_6_man = med_perc_defesas_com_6_man
        self.colocacao_vis = colocacao_vis
        self.med_perc_gols_sof_6_vis = med_perc_gols_sof_6_vis
        self.med_perc_defesas_com_3_man = med_perc_defesas_com_3_man
        self.med_perc_chutes_com_6_vis = med_perc_chutes_com_6_vis
        self.odds_w = odds_w
        self.odds_l = odds_l
        self.bankroll = bankroll

    def get_data_as_frame(self):
        try:
            custom_data_input_dict = {
                'med_perc_chutes_com_6_man': [self.med_perc_chutes_com_6_man],
                'diff_colocacao_adv_man': [self.diff_colocacao_adv_man],
                'colocacao_man': [self.colocacao_man],
                'med_perc_defesas_com_6_man': [self.med_perc_defesas_com_6_man],
                'colocacao_vis': [self.colocacao_vis],
                'med_perc_gols_sof_6_vis': [self.med_perc_gols_sof_6_vis],
                'med_perc_defesas_com_3_man': [self.med_perc_defesas_com_3_man],
                'med_perc_chutes_com_6_vis': [self.med_perc_chutes_com_6_vis],
                'odds_w': [self.odds_w],
                'odds_l': [self.odds_l],
                'bankroll': [self.bankroll]
            }
            
            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e, sys)

