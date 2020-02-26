import pandas as pd

def main():
    fname = ''
    delta = 31536000*2
    csv = pd.read_csv(fname)
    csv['Timestamp'] += delta
    csv.to_csv(fname, header=True, index=False)

if __name__ == '__main__':
    main()