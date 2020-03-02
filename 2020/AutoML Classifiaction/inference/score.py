# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import pickle
import numpy as np
import pandas as pd
import azureml.train.automl
from sklearn.externals import joblib
from azureml.core.model import Model

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


input_sample = pd.DataFrame(data=[{'age': 57, 'job': 'technician', 'marital': 'married', 'education': 'high.school', 'default': 'no', 'housing': 'no', 'loan': 'yes', 'contact': 'cellular', 'month': 'may', 'day_of_week': 'mon', 'duration': 371, 'campaign': 1, 'pdays': 999, 'previous': 1, 'poutcome': 'failure', 'emp.var.rate': -1.8, 'cons.price.idx': 92.893, 'cons.conf.idx': -46.2, 'euribor3m': 1.299, 'nr.employed': 5099.1}])
output_sample = np.array([0])


def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = Model.get_model_path(model_name = 'AutoML4da9cdeeb0')
    model = joblib.load(model_path)


@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))
def run(data):
    try:
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
