import random as r
from EssentialElements import*
from websearch import *
import bs4
import webbrowser

SINGULAR_PATTERN = r'(^(К|Ч)+[А-Яа-я]+(й|о|м|я)+\b)|(^(к|ч)+[А-Яа-я]+(й|о|м|я)+\b)'  # ед.число
PLURAL_PATTERN = r'(^(К|Ч)+[А-Яа-я]+е+\b)|(^(к|ч)+[А-Яа-я]+(е|х)+\b)'   # мн.число
DEFINITION_PATTERN = r'^((Ч|ч|э)+[А-яа-я]+\b)|((К|к|э)+[А-яа-я]+\b)'
EXTRA_S_PATTERN = r'(Б|б|Л|л|Ш|ш|Н|н|Т|т|В|в)+[А-Яа-я]+(й|я|м|о)+\b'  # слова относящиеся к полож. качествам игроков
EXTRA_P_PATTERN = r'(Б|б|Л|л|Ш|ш|Н|н|Т|т|В|в)+[А-Яа-я]+(е|и|х)+\b'
ROLE = '(А|а)мплуа'
stop_searching = ' Поиск прекращен'

keyValues = [balls, goalkeepers, strikers, midfielder, defenders, coaches, teams, footballers, footballers]

keyAttributes = {                      # словарь, где кажное ключевое слово связано с определенными значениями по смыслу
    keyWords[i]: keyValues[i] for i in range(len(keyWords))
}


significantDuo = {                   # словарь | ключи = футбольным элементам | значения = трактовкам
    significantAttr[i]: significantMeaning[i] for i in range(len(significantAttr))
}


def take_definition_answer(text):  # ответ на вопрос, который связан с футбольными элементами
    pattern = re.compile(DEFINITION_PATTERN)
    start = pattern.match(text)  # поиск ключевого слова в начале предложения
    if start is not None:
        for word in significantAttr:
            if word in text or word.lower() in text or word.upper() in text:
                answer = word + ' - ' + significantDuo[word]
                return answer
    else:
        start = pattern.search(text)  # поиск ключевого слова во всем предложении
        if start is not None:
            for word in significantAttr:
                if word in text or word.lower() in text:
                    answer = word + ' - ' + significantDuo[word]
                    return answer
    return False


def take_basic_answers(text):  # ответ на обычные футбольные вопросы (В духе - какой вратарь входит в топ-10 2019г?)
    pattern = re.compile(SINGULAR_PATTERN)
    start = pattern.match(text)
    extra_s_pattern = re.compile(EXTRA_S_PATTERN)
    extra_s_word = extra_s_pattern.search(text)
    pattern_amplya = re.compile(ROLE)
    amplya = pattern_amplya.search(text)  # выдает информацию пользователю о амплуа той или иной позиции на поле

    if (start is not None or extra_s_word is not None) and amplya is None:  # возможность дать ответ даже без вопросительного слова
        for word in keyWords:
            if (word in text or word.title() in text or word.upper() in text) and extra_s_word is None:
                answer = keyAttributes[word][r.randint(0, len(keyAttributes[word]) - 1)]
                return answer
            elif (word in text or word.title() in text or word.upper() in text) and extra_s_word is not None:
                answer = keyAttributes[word][r.randint(FIRST_TOP, LAST_TOP)]  # в ответе будет вратарь, входящий в топ 4
                return answer

    elif start is None:
        pattern = re.compile(PLURAL_PATTERN)
        start = pattern.match(text)
        extra_p_pattern = re.compile(EXTRA_P_PATTERN)
        extra_p_word = extra_p_pattern.search(text)
        if (start is not None or extra_p_pattern is not None) and amplya is None:
            for word in keyWords:
                if (word in text or word.title() in text or word.upper() in text) and extra_p_word is None:
                    return ', '.join(keyAttributes[word])
                elif (word in text or word.title() in text or word.upper() in text) and extra_p_word is not None:
                    return ', '.join(keyAttributes[word][FIRST_TOP:LAST_TOP+1])
        elif start is not None and amplya is not None:
            return choose_right_role(text)
    return False


def greeting(text):  # приветствие
    for search_str in greeting_in:
        start = re.search(search_str.lower(), text.lower())
        if start is not None:
            answer = greeting_system[r.randint(0, len(greeting_system) - 1)] + \
                        greeting_add[r.randint(0, len(greeting_add) - 1)]
            return answer
    return False


def take_info_match(text):  # информация о счете матча ЛЧ
    information = []
    clean_data_array = []
    team_list = []  # все команды, имеющие результат матча в ЛЧ
    team_s = []
    response_array = []
    if lc_parse(base_ulr, headers, information):
        create_clear_data(clean_data_array, information)
        create_team_list(team_list, clean_data_array)
        team_list = list(set(team_list))
        if teams_result(text, team_s, team_list) is not False:
            if len(team_s) == 2:
                search_match(team_s[0], team_s[1], response_array, clean_data_array)
                return ', '.join(response_array)
            elif len(team_s) == 1:
                search_match(team_s[0], SPACE, response_array, clean_data_array)
                return ', '.join(response_array)
    return False


def teams_result(text, team_s, team_list):
    for key in scores:  # поиск ключевого слова для выдачи информации о сыгранном матче
        if key.lower() in text.lower():
            while True:
                appending_team = compare_minor_major(text, team_list, team_s)
                if appending_team != "":
                    team_s.append(appending_team)
                else:
                    break
            if len(team_s) < 3:  # не может быть найденно более 2 команд, чтобы дать результат противостояния между ними
                return team_s
    return False


def compare_minor_major(minor_text, major_text, team_s):  # нахождение команды, с обработкой опечаток в названии
    main_array = major_text  # список команд играющих в лиге чемпионов
    secondary_array = minor_text.split()  # разбиение предложения по пробелам для поиска определенной команды
    for major_word in main_array:
        if len(major_word) > 2:
            for minor_word in secondary_array:
                if len(minor_word) > 2:  # самое короткое название команды-3 буквы - ПСЖ|-> игнорировать ненужные слова
                    major_word = major_word.lower()
                    minor_word = minor_word.lower()
                    if len(minor_word) == len(major_word):
                        counter = 0
                        for i in range(len(minor_word)):
                            if minor_word[i] == major_word[i]:
                                counter += 1
                        if counter > len(minor_word)//2:
                            if major_word not in team_s:  # исключение дубликотов найденных команд
                                return major_word
                    elif len(minor_word) < len(major_word):
                        for i in range(len(major_word)):
                            if len(major_word) >= len(minor_word) + i:
                                fixed_main_word = major_word[i:len(minor_word)+i]
                                counter = 0
                                for j in range(len(minor_word)):
                                    if fixed_main_word[j] == minor_word[j]:
                                        counter += 1
                                if counter > len(major_word)//2:
                                    if major_word not in team_s:
                                        return major_word
                    else:
                        for i in range(len(minor_word)):
                            if len(minor_word) >= len(major_word) + i:
                                fixed_word = minor_word[i:len(major_word)+i]
                                counter = 0
                                for j in range(len(major_word)):
                                    if fixed_word[j] == major_word[j]:
                                        counter += 1
                                if counter > len(minor_word)//2:
                                    if major_word not in team_s:
                                        return major_word
    return ""


def googling(text):  # поиск ответа в Google в крайних ситуациях
    divided_array = [';', ':', '.', '-', ' ', ',', '!', '?', '"', "'"]
    arr = re.split(str(divided_array), text)
    key_meanings = []  # для выявления ключевых слов при разбиении предложения
    for word in arr:
        extra_arr = []
        for key in keyAttributes:
            for values in keyAttributes[key]:
                extra_arr.append(values)
        if word in extra_arr:
            key_meanings.append(word)
        else:
            flag = True
            for i in word:
                if ord(i) < 1040 or ord(i) > 1103 or ord(i) == 1105 or ord(i) == 1025:  # при разбиении не учитывать нерусские слова
                    flag = False
                    break
            if flag and len(word) > 0:
                key_meanings.append(word)
    search_line = ' '.join(key_meanings)

    res = requests.get(google_search + search_line)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    linkElements = soup.select('a')
    linkToOpen = min(5, len(linkElements))
    for i in range(2, linkToOpen):
        webbrowser.open(google + linkElements[i].get('href'))



