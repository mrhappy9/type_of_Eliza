import re
USER = '<USER>:      '
SYS = '<SYSTEM>: '
ERROR_SYS = '<SYSTEM>: Была произведена попытка некорректного ввода.'
ENTER_KEY = 13  # код кнопки 'Enter'
FIRST_TOP = 0  # все лучшие игроки, тренеры ...
LAST_TOP = 3   # расположены на отрезке [0,3]

RN = open('renouncement.txt')  # слова, отражающие отказ пользователя в поиске
renouncement = RN.read().split(', ')
RN.close()

ReS = open('results_from_google.txt')  # сообщение о том, что ответ получен от Google
google_results = ReS.read().split('; ')
ReS.close()

AG = open('agreements.txt')  # слова, отражающие согласие пользователя в поиске
agreements = AG.read().split(', ')
AG.close()

GOOGLE = open('answers_from_google.txt')  # спросить соглашение у пользователя на нахождение инф-ии в Google
google_answers = GOOGLE.read().split('; ')
GOOGLE.close()

SR = open('scores.txt')  # ключ слова для поиска результата матча ЛЧ
scores = SR.read().split(', ')
SR.close()

FT = open('footballers.txt')  # отдельные футболисты(вне зависимости от позиции на поле)
footballers = FT.read().split(', ')
FT.close()

RS = open('main_roles.txt')  # амплуа в футболе
roles = RS.read().split(', ')
RS.close()

RG = open('regret.txt')  # сожаления о том, что не существует ответа на заданный вопрос
regrets = RG.read().split('; ')
RG.close()

TM = open('team.txt')  # названия топ-команд
teams = TM.read().split(', ')
TM.close()

GK = open('goalkeepers.txt')  # имена топ-вратарей
goalkeepers = GK.read().split(', ')
GK.close()

BALLS = open('balls.txt')  # названия футбольных мячей
balls = BALLS.read().split(', ')
BALLS.close()

kW = open('keywords.txt')  # ключевые слова
keyWords = kW.read().split(', ')
kW.close()

st_forwards = open('attacking.txt')  # имена топ-нападающих
strikers = st_forwards.read().split(', ')
st_forwards.close()

midF = open('midfielder.txt')  # имена топ-полузащитников
midfielder = midF.read().split(', ')
midF.close()

defence = open('defender.txt')  # имена топ-защитников
defenders = defence.read().split(', ')
defence.close()

chS = open('coach.txt')  # имена топ-тренеров
coaches = chS.read().split(', ')
chS.close()


gR_in = open('greeting_in.txt')  # фразы приветствия пользователя
greeting_in = gR_in.read().split(', ')
gR_in.close()

gR_sys = open('greeting_system.txt')  # фразы приветствия системы
greeting_system = gR_sys.read().split(', ')
gR_sys.close()

gR_ad = open('greeting_ad.txt')  # фразы, необоходимые для добавляние к приветствию системы
greeting_add = gR_ad.read().split('; ')
gR_ad.close()

sgAttr = open('significantAttr.txt')  # футбольные элементы
significantAttr = sgAttr.read().split(', ')
sgAttr.close()

sgMeaning = open('significantMeaning.txt')  # трактовка футбольных элементов
significantMeaning = sgMeaning.read().split('; ')
sgMeaning.close()


def choose_right_role(text):  # обработка амплуа(конктретные аббревиатуры для каждой позиции на поле)
    fake_min = 10 ** 10
    info = ''
    role = ['(В|вратар)', '(З|з)ащитни', '(П|п)олузащитн', '(Н|н)ападающ']
    for word in role:
        pattern = re.compile(word)
        start = pattern.search(text)
        if start is not None:
            cur = tuple(start.span())[0]
            if cur < fake_min:  # сделана дополнительная проверка, чтобы избежать ошибок с защ. и полузащ.
                info = ', '.join(roles[roles.index(str(role.index(word)))+1:roles.index(str(role.index(word)+1))]) \
                    if role.index(word) < (len(role) - 1) else ', '.join(roles[roles.index(str(role.index(word)))+1:])
                fake_min = cur
    return info