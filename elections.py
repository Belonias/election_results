import argparse
import requests
import datetime
import time
import csv
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-output_folder', '--of', type=str,
                        help='output folder selection', required=True)
    parser.add_argument('-min_date', '--md', type=str,
                        help='minimum date')
    parser.add_argument('-max_num_pages', '--mnp', type=int,
                        help='maximum number of pages')
    args = parser.parse_args()
    print('This is the input argument ', args)

    if args.md:
        try:
            datetime.datetime.strptime(args.md, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    controller(args)


def controller(args):
    url = 'http://www.electionguide.org/ajax/election/?sEcho=1&iColumns=5&sColumns=&iDisplayStart=0&iDisplayLength=1000000&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&iSortCol_0=3&sSortDir_0=desc&iSortingCols=1&bSortable_0=false&bSortable_1=true&bSortable_2=false&bSortable_3=true&bSortable_4=true&_=1547551919061'
    r = requests.get(url)
    data = r.json()
    if args.md and args.mnp:
        mnp_elections_list = max_num_pages(data, args.mnp)
        md_elections_list = min_date(mnp_elections_list, args.md)
        csv_table_writer(md_elections_list, args.of)
        print('Both arguments')
    elif args.md:
        md_elections_list = min_date(data, args.md)
        csv_table_writer(md_elections_list, args.of)
        print('Only md argument')
    elif args.mnp:
        mnp_elections_list = max_num_pages(data, args.mnp)
        csv_table_writer(mnp_elections_list, args.of)
        print('max num page arg')


def max_num_pages(data, args):
    new_elections_list = {}
    total_records = data['iTotalRecords']
    ROWS = args * 30
    if ROWS > total_records:
        ROWS = total_records
    new_elections_list['aaData'] = data['aaData'][:ROWS]
    print(type(new_elections_list))
    print(new_elections_list)
    return new_elections_list


def min_date(data, args):
    new_elections_list = {}
    date_filter = str(args)
    for elections in data['aaData']:
        if time.strptime(elections[3], "%Y-%m-%d") >= time.strptime(date_filter, "%Y-%m-%d"):
            new_elections_list.setdefault('aaData', []).append(elections)
    return new_elections_list


def csv_table_writer(data, args):
    now = datetime.datetime.now()
    # original job_execution_time = now.strftime("%Y-%m-%d %H:%M:%S")
    job_execution_time = now.strftime("%Y/%m/%d/%H%M%S")
    file_path = args + '/' + job_execution_time + '/'
    try:
        directory = os.path.dirname(file_path)
        os.makedirs(directory)
    except OSError:
        print('OSError')
    with open(file_path + 'table.csv', 'w+', newline='') as csvfile:
        row_writer = csv.writer(csvfile, delimiter=',')
        row_writer.writerow(['country', 'election_for', 'date', 'status'])
        for election in data['aaData']:
            if election[2][0] is None:
                row_writer.writerow([election[1][0].lower(), 'referendum', election[3].lower(), election[4].lower()])
            else:
                row_writer.writerow([election[1][0].lower(), election[2][0].lower(), election[3].lower(), election[4].lower()])


if __name__ == '__main__':
    main()
