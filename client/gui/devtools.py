import pandas as pd
import datagen

def filedata():
    datagen.run()
    f = open("generated.txt", "r")
    # f = open("sample_output/small_sample.txt")
    data = f.readline()
    
    return data

if __name__ == '__main__':
    filedata()