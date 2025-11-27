# task.py
import argparse
import csv
from collections import defaultdict
from tabulate import tabulate


def build_table(files):
    d = defaultdict(list)

    for file in files:
        with open(file) as fh:
            dic = csv.DictReader(fh, delimiter=',')
            for reading in dic:
                d[reading['position']].append(float(reading['performance']))

    final_table = []
    for position, values in d.items():
        avg_perf = round(sum(values) / len(values), 2)
        final_table.append([position, avg_perf])

    final_table.sort(key=lambda row: row[1], reverse=True)
    return final_table


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+', help='One or more input files')
    parser.add_argument('--report', help='report')
    opt = parser.parse_args()

    final_table = build_table(opt.files)
    headers = ["position", opt.report]
    print(tabulate(final_table, headers=headers))


if __name__ == "__main__":
    main()

