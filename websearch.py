import requests
from bs4 import BeautifulSoup as bs


MISS = [':', '.', ' ']  # список для сортировки полученных данных
FAILURE_GAME = '-'  # для отсеивания матчей, результат которых еще не выставлен на сайте ЛЧ
SPACE = ''

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
base_ulr = 'https://terrikon.com/champions-league'
google_search = 'https://google.com/search?q='
google= 'https://google.com'


def lc_parse(base_url, headers, information):  # парсинг данных с сайта ЛЧ
    session = requests.Session()  # для обхода ошибки 403 Forbidden
    req = session.get(base_url, headers=headers)
    if req.status_code == 200:    # сервер успешно ответил за запрос
        soup = bs(req.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'col2'})
        for div in divs:
            title = div.find('table', attrs={'class': 'gameresult'}).text  # поиск информации о прошедших матчах ЛЧ
            information.append(title)
        return True
    return False


def create_clear_data(clean_data_array, information):  # создание обработанного массива данных с сайта ЛЧ
    string = ''
    for main_word in information:
        brr = main_word.split('\n')
        for word in brr:
            if FAILURE_GAME not in word and word != SPACE:  # не брать в рассчет несыгранные матчи
                step = 0
                for i in range(len(word)+1):
                    if i < len(word)-1:
                        if word[i].isdigit():
                            if (word[i-1].isdigit() is False and word[i-1] not in MISS) and (word[i+1].isdigit() or word[i+1] in MISS):
                                string += word[step:i] + ' '
                                step = i
                            elif (word[i-1].isdigit() is True or word[i-1] in MISS) and (word[i+1].isdigit() is False and word[i+1] not in MISS):
                                string += word[step:i+1] + ' '
                                i += 1
                                step = i
                            else:
                                string += word[step:i]
                                step = i
                        else:
                            string += word[step:i]
                            step = i
                    else:
                        string += word[step:i]
                        step = i
                clean_data_array.append(string)
                string = ''


def search_match(guest, home, response_array, clean_data_array):  # информация о результате матча
    if guest != '' and home != '':
        for word in clean_data_array:
            if guest in word.lower() and home in word.lower():
                response_array.append(word)
    elif guest != '' and home == '':
        for word in clean_data_array:
            if guest in word.lower():
                response_array.append(word)
    else:
        for word in clean_data_array:
            if home in word.lower():
                response_array.append(word)
    return response_array


def create_team_list(team_list, clean_data_array):  # создание списка всех команд, которые сыграли матчи в ЛЧ
    for word in clean_data_array:
            team_list += getting_word(word).split(', ')
    return team_list


def getting_word(word):  # получение информации о клубах
    check = []
    tmp = ''
    for index in range(len(word)):
        if word[index].isdigit() is False and word[index] not in MISS:
            tmp += word[index]
        elif tmp != '':
            check.append(tmp)
            tmp = ''
    return ', '.join(check)



