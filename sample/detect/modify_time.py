import pandas as pd

def main():
    fname = 'sample.csv'
    delta = 31536000 * 2
    csv = pd.read_csv(fname)
    csv['Timestamp'] += delta
    csv.to_csv(fname, header=True, index=False)
    ext = fname.split('.')[-1]
    fname = fname.split('.')[:-1]
    fname = '.'.join(str(x) for x in fname)

    # To TSV
    csv.to_csv(index=False, header=True,  path_or_buf='{}.tsv'.format(fname), sep='\t')
    # To JSON
    csv.to_json(index=False, indent=2, path_or_buf='{}.json'.format(fname), orient='table')
    # To xls
    csv.to_excel(index=False, header=True, excel_writer='{}.xls'.format(fname))
    # To xlsx
    csv.to_excel(index=False, header=True, excel_writer='{}.xlsx'.format(fname))



if __name__ == '__main__':
    main()