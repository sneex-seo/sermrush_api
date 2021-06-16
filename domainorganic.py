from requests_html import HTMLSession
import csv
from tempfile import NamedTemporaryFile
from shutil import move


api_key = 'f812a9aa1dd8ef29511e25e0483ed3cb'  # написать свой API ключ
region = 'ua'  # написать кодировку нужного региона
csv_file_name = "winnerloser.csv"  # csv файл для записи
limit = "100" #лимит строк в выдаче по запросу
txtdomain_files_name = 'domains.txt' # файл откуда будем брать запросы


with open(txtdomain_files_name, 'r+') as f:
    domains = [line.strip() for line in f]


for domain in domains:
    api_url = f'https://api.semrush.com/?type=phrase_this&key\
={api_key}&phrase={domain}&export_columns=Ph,Nq,Cp,Co,Nr,Td&database={region}'
    session = HTMLSession()
    response = session.get(api_url)
    with open(csv_file_name, 'a', newline='') as f:
        f.write(f'{response.text}\n')
    #f.write(response.text)



def get_balance(key):
    api_url = f'http://ru.semrush.com/users/countapiunits.html?key={key}'
    session = HTMLSession()
    response = session.get(api_url)
    result_data = response.json()
    balance = result_data
    print('Остаток лимитов на балансе: ' + str(balance))




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

remove_dublicates(csv_file_name)
remove_empty_lines(csv_file_name)
get_balance(api_key)