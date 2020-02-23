import predict_atk
import predict_benign
import pandas as pd

def run_predict(df):
    noAtk = {11:{'IsAtk':0, 'Time': 12345}}

    (noAtk,Atk) = predict_benign.run_predict(df)
    output = noAtk.copy()
    atk_output = predict_atk.run_predict(Atk)

    output.update(atk_output)
    return output



if __name__ == "__main__":
    print(run_predict("big_test_5.csv"))
