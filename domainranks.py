from requests_html import HTMLSession
import csv
from tempfile import NamedTemporaryFile
from shutil import move


api_key = 'f812a9aa1dd8ef29511e25e0483ed3cb'  # написать свой API ключ
region = 'ua'  # написать кодировку нужного региона
txtdomain_file_name = 'domainranks.txt'  # текстовый файл с списком доменов
csv_file_name = "domainranks.csv"  # csv файл для записи


def remove_dublicates(csv_file):

    with open(csv_file, 'r+', newline='') as f:
        data = list(csv.reader(f))
        new_data = [a for i, a in enumerate(data) if a not in data[:i]]
        f.seek(0)
        write = csv.writer(f)
        write.writerows(new_data)
        f.truncate()


def remove_empty_lines(csv_file):
    try:
        with open(csv_file, "rb") as fin, NamedTemporaryFile(delete=False) as fout:
            temp_filename = fout.name
            for line in fin:
                if line.strip():
                    fout.write(line)
    except FileNotFoundError:
        print("{} does not exist.".format(csv_file))
    else:
        move(temp_filename, csv_file)


def bulk_domains_analysis(api_key, region, txtdomain_files_name, csv_file):

    with open(txtdomain_files_name, 'r+') as f:
        domains = [line.strip() for line in f]

    for domain in domains:
        api_url = f'https://api.semrush.com/?key={api_key}&type=domain_ranks&\
            export_columns=Db,Dn,Rk,Or,Ot,Oc&domain={domain}&database={region}'
        session = HTMLSession()
        response = session.get(api_url)
        with open(csv_file, 'a', newline='') as f:
            f.write(f'{response.text}\n')
            # f.write(response.text)


def get_balance(key):
    api_url = f'http://ru.semrush.com/users/countapiunits.html?key={key}'
    session = HTMLSession()
    response = session.get(api_url)
    result_data = response.json()
    balance = result_data
    print('Остаток лимитов на балансе: ' + str(balance))


bulk_domains_analysis (api_key, region, txtdomain_file_name, csv_file_name)
remove_dublicates(csv_file_name)
remove_empty_lines(csv_file_name)
get_balance(api_key)