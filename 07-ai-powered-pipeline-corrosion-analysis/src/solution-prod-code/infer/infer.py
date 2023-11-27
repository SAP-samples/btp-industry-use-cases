import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask
from flask import request as call_request

# Creates Flask serving engine
app = Flask(__name__)

model = None

@app.before_first_request
def init():
    """
    Load model else crash, deployment will not start
    """
    global model
    model = pickle.load(open ('/mnt/models/gradient_boosting_regressor.pkl','rb')) # All the model files will be read from /mnt/models
    return None


@app.route("/v2/greet", methods=["GET"])
def status():
    global model
    if model is None:
        return "Flask Code: Model was not loaded."
    else:
        return "Model is loaded."


# You may customize the endpoint, but must have the prefix `/v<number>`
@app.route("/v2/predict", methods=["POST"])
def predict():
    """
    Perform an inference on the model created in initialize

    Returns:
        String value price.
    """

    global model
    #
    query = dict(call_request.json)
    input_features = [ # list of values from request call
        query['loc_id'],
        query['idx'],
        query['v01'],
        query['v02'],
        query['v03'],
        query['v04'],
        query['v05'],
        query['v06'],
        query['v07'],
        query['v08'],
        query['v09'],
        query['v10'],
        query['v11'],
        query['v12'],
        query['v13']
    ]

    df_test = pd.DataFrame([input_features], \
                      columns=['loc_id','idx','v01','v02','v03','v04','v05'\
                               ,'v06','v07','v08','v09','v10','v11','v12','v13'])

    # Prediction
    prediction = model.predict(df_test)
    output = str(prediction)

    # Response
    return output

if __name__ == "__main__":
    print("Serving Initializing")
    init()
    print(f'{os.environ["greetingmessage"]}')
    print("Serving Started")
    app.run(host="0.0.0.0", debug=True, port=9001)
