from flask import Flask, request, render_template, session
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application=Flask(__name__, template_folder='templates', static_folder='static')

app = application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data = CustomData(
            med_perc_chutes_com_6_man=float(request.form.get('med_perc_chutes_com_6_man')),
            # diff_colocacao_adv_man=float(request.form.get('diff_colocacao_adv_man')),
            colocacao_man=float(request.form.get('colocacao_man')),
            med_perc_defesas_com_6_man=float(request.form.get('med_perc_defesas_com_6_man')),
            colocacao_vis=float(request.form.get('colocacao_vis')),
            med_perc_gols_sof_6_vis=float(request.form.get('med_perc_gols_sof_6_vis')),
            med_perc_defesas_com_3_man=float(request.form.get('med_perc_defesas_com_3_man')),
            med_perc_chutes_com_6_vis=float(request.form.get('med_perc_chutes_com_6_vis')),
            odds_w=float(request.form.get('odds_w')),
            odds_l=float(request.form.get('odds_l')),
            bankroll=float(request.form.get('bankroll'))
        )

        pred_df = data.get_data_as_frame()
        print(pred_df.values)

        predict_pipeline=PredictPipeline()
        prob_w, bet_w, bet_l = predict_pipeline.predict(pred_df)     

        print(f'Probabilidade Modelo {prob_w}')
        print(f'Aposta Vitoria {bet_w}')   
        print(f'Aposta Derrota {bet_l}')

       
        return render_template('home.html', 
                               prob_w=round(prob_w*100,2),
                               bet_w=round(bet_w,2),
                               bet_l=round(bet_l,2),
                               show_results=True) # Flag para mostrar o modal


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)