from Parser import Reader

def main():
    fname = '../../sample/sample.xlsx'
    csvread = Reader(fname, 4)
    print(csvread.read())


if __name__ == '__main__':
    main()