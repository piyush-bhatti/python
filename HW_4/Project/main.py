import json
import re
import time
from os import listdir
from os.path import isfile, join
from statistics import stdev,mean


def load_files():

    only_files = [f for f in listdir('./') if isfile(join('./', f))]

    print(only_files)

    dict_1 = {}

    for file_name in only_files:

        key_value_dict = 0
        data_list = 0

        if re.match('[\w,-]+.csv',file_name):
            with open(file_name) as f:
                for line in f:
                    if re.match('\d{4}-\d{2}-\d{2},\d+.\d+',line):
                        parts = line.split(sep=',')
                        key_value_dict = re.search('[\w/-]+',file_name).group(0)


                        try:
                            if not([str(parts[0]), float(parts[1])] in data_list):
                                data_list.append((str(parts[0]), float(parts[1])))

                        except:
                            print("Skipping line")

            print(file_name)

        elif re.match('[\w,-]+.json',file_name):
            print(file_name)
            with open(file_name) as f:
                data = json.load(f)
                key_value_dict =re.search('[\w/-]+',file_name).group(0)
                    #"USD-{}".format(data['dataset']['dataset_code'])
                    #str(data['dataset']['name'])
                data_list = [tuple(x) for x in data['dataset']['data']]

        if data_list:

            dict_1[key_value_dict] = data_list
            print(dict_1)

            dict_1[key_value_dict].sort(key=lambda x: time.strptime(x[0], '%Y-%m-%d'))
    return dict_1


def write_operation(dict_1):
    with open('./files/concat_file.json','w') as f:
        json.dump(dict_1, f)


def request():
    currency_input = input("Enter currency codes separated by space : ")
    currency_parts = currency_input.split()
    key_value_dict = "{}-{}".format(currency_parts[0],currency_parts[1])
    period_input = input("Enter a period : ")
    period_parts = period_input.split(sep='-')
    start = process_date(period_parts[0],"start")
    end = process_date(period_parts[1],"end")
    return [key_value_dict,start,end]


def process_date(date,endpoint):
    try:
        if re.match('(\d{2})?.?(\d{2})?.?\d{4}',date):
            if re.match('\d{2}.\d{2}.\d{4}',date):
                parts = date.split(sep='.')
                date_processed = "{}-{}-{}".format(parts[2],parts[1],parts[0])

            elif re.match('\d{2}.\d{4}',date):
                parts = date.split(sep='.')
                if endpoint == "start":
                    date_processed = "{}-{}-01".format(parts[1],parts[0])
                elif endpoint == "end":
                    if parts[0] in ['1','3','5','7','8','10','12']:
                        date_processed = "{}-{}-31".format(parts[1], parts[0])
                    elif parts[0] in ['4','6','9','11']:
                        date_processed = "{}-{}-30".format(parts[1], parts[0])
                    elif parts[1] == 2:
                        if (parts[1] % 4) == 0:
                            if (parts[1] % 100) == 0:
                                if (parts[1] % 400) == 0:
                                    date_processed = "{}-{}-29".format(parts[1], parts[0])
                                else:
                                    date_processed = "{}-{}-28".format(parts[1], parts[0])
                            else:
                                date_processed = "{}-{}-29".format(parts[1], parts[0])
                        else:
                            date_processed = "{}-{}-28".format(parts[1], parts[0])

            elif re.match('\d{4}',date):
                if endpoint == "start":
                    date_processed = "{}-01-01".format(date)
                elif endpoint == "end":
                    date_processed = "{}-12-31".format(date)

        return date_processed

    except:
        print("Invalid Format")


def output(key_value_dict, start, end):
    with open('files/concat_file.json') as f:
        data = json.load(f)

    for x in data[key_value_dict]:
        if x[0] == start:
            index_1 = data[key_value_dict].index(x)
        if x[0] == end:
            index_2 = data[key_value_dict].index(x)
    list_1 = data[key_value_dict][index_1:index_2+1]

    minimum = min(x[1] for x in list_1)
    maximum = max(x[1] for x in list_1)
    mean_value = mean(x[1] for x in list_1)
    standard_deviation = stdev((x[1] for x in list_1))
    print("Min : {}".format(minimum))
    print("Max : {}".format(maximum))
    print("Mean value : {}".format(mean_value))
    print("Standard deviation : {}".format(standard_deviation))


a = {}
a = load_files()
write_operation(a)
x = 1
while x > 0:
    input_list = request()
    output(input_list[0],input_list[1],input_list[2])
