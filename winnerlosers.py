from requests_html import HTMLSession
import csv



api_key = 'f812a9aa1dd8ef29511e25e0483ed3cb'  # написать свой API ключ
region = 'ua'  # написать кодировку нужного региона
csv_file_name = "winnerloser.csv"  # csv файл для записи
limit = "10" #лимит строк в выдаче по запросу, 10000 строк сьесть 200к лимитов

#um_asc	- сортировка по трафику органик по убыванию
#um_desc - сортировка по трафику органик по возрастанию
#om_asc - соритровка по количеству органик ключей по убыванию
#om_desc- сортировка по количеству органик ключей по возрастанию


def winnerloser(api_key, csv_file_name, limit, region):
    api_url = f'https://api.semrush.com/?type=rank_difference&key={api_key}&display_limit={limit}&database={region}&display_sort=um_asc'
    session = HTMLSession()
    response = session.get(api_url)
    with open(csv_file_name, 'a', newline='') as f:
        f.write(f'{response.text}\n')
    #f.write(response.text)


#Функция которая выводит баланс апи на аккаунте
def get_balance(key):
    api_url = f'http://ru.semrush.com/users/countapiunits.html?key={key}'
    session = HTMLSession()
    response = session.get(api_url)
    result_data = response.json()
    balance = result_data
    print('Остаток лимитов на балансе: ' + str(balance))


winnerloser(api_key, csv_file_name, limit, region)
get_balance(api_key)