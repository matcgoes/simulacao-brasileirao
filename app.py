from flask import Flask, request, render_template
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
            diff_colocacao_adv_man=float(request.form.get('diff_colocacao_adv_man')),
            colocacao_man=float(request.form.get('colocacao_man')),
            med_perc_defesas_com_6_man=float(request.form.get('med_perc_defesas_com_6_man')),
            colocacao_vis=float(request.form.get('colocacao_vis')),
            med_perc_gols_sof_6_vis=float(request.form.get('med_perc_gols_sof_6_vis')),
            med_perc_defesas_com_3_man=float(request.form.get('med_perc_defesas_com_3_man')),
            med_perc_chutes_com_6_vis=float(request.form.get('med_perc_chutes_com_6_vis'))
        )

        pred_df = data.get_data_as_frame()
        print(pred_df.values)

        predict_pipeline=PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        return render_template('home.html', results=round(results[0],2)*100)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)