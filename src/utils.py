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
