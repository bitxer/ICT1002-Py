import pandas as pd
import datagen

def filedata():
    # df = pd.read_csv("sample_output/big_sample.txt")
    # testdata = df.head(900)
    # f = open("sample_output/big_sample.txt", "r")
    datagen.run()
    f = open("generated.txt", "r")
    # f = open("sample_output/small_sample.txt")
    data = f.readline()
    
    return data

if __name__ == '__main__':
    filedata()