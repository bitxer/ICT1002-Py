import pandas as pd

def filedata():
    # df = pd.read_csv("sample_output/big_sample.txt")
    # testdata = df.head(900)
    # f = open("sample_output/big_sample.txt", "r")
    f = open("sample_output/small_sample.txt", "r")
    data = f.readline()
    
    return data

if __name__ == '__main__':
    filedata()