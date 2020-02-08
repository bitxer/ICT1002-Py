import predict_atk
import pandas as pd

def run_predict(df):
    noAtk = {11:{'IsAtk':0, 'Time': 12345}}

    #(noAtk,Atk) = ???() <-- pytorch
    output = noAtk.copy()
    atk_output = predict_atk.run_predict(df)

    output.update(atk_output)
    return output



if __name__ == "__main__":
    print(run_predict("small_test_no_labels.csv"))
