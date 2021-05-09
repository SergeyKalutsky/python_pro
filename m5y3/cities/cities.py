from random import  randint, choice, sample
LEVEL = 5  # 0, 1, 2, 3, 4, 5

# выгружает словарь из текстового файла
def prepare_dictionary(filename='dict'):
    textfile = open('dict', 'r')
    content = textfile.readlines()
    print(content)
    words = [] 
    for line in content:
        words.append(line.rstrip('\n'))
    textfile.close()
    return words

# находит в списке слово, которое начинается на заданную букву
def find_word(letter, word_list):
    print('Вспоминаю город на букву ', letter, '...')
    for word in word_list:
        if word[0] == letter:
            return word

# уже использованные в игре слова
used_words = []
# полный словарь игры
all_words = prepare_dictionary()
# словарь компьютера
computer_words = sample(all_words, len(all_words) // 2 ** (5 - LEVEL))
print('Привет! Поиграем в города? Мой ход:')
# взяли случайное слово из словаря компьютера
city_1 = choice(computer_words)
print(city_1)
# перенесли слово из списка computer_words в список used_words:
used_words.append(city_1)
computer_words.remove(city_1)

# статус игры:
run = True
# чей сейчас ход:
step = 'man' # 'computer'  #

while run:
    # если слово оканчивается на ЪЬЫ, берем предпоследнюю букву:
    if city_1[len(city_1) - 1] in ('Ь', 'Ы', 'Ъ'):
        last_letter = city_1[len(city_1) - 2]
    else:
        last_letter = city_1[len(city_1) - 1]

    # шаг компьютера
    if step == 'computer':
        # ищем подходящее слово
        city_2 = find_word(last_letter, computer_words)
        # если слово не нашли city_2 == None
        if city_2 is not None:
            # компьютер сделал ход:
            print(city_2)
            # перенесли слово в список использованных:
            computer_words.remove(city_2)
            used_words.append(city_2)
            # переход к следующему ходу:
            city_1 = city_2
            step = 'man'
        else:
            # компьютер не нашел подходящего слова:
            print('Сдаюсь! Вы выиграли!')
            run = False

    # шаг человека
    elif step == 'man':
        # введенное слово перевели в верхний регистр
        city_2 = input().upper()
        # если введено "-" конец игры:
        if city_2 == '-':
            print('Я победил!!!')
            run = False
        # проверка корректности хода
        # первая буква совпадает с последней буквой предыдущего слова?
        elif last_letter != city_2[0]:
            print('Неверный ход. Попытайтесь еще раз')
        # слово не повторяется?
        elif city_2 in used_words:
            print('Такой город уже встречался. Введите другой')
        # Слово есть в списке всех городов?
        elif city_2 not in all_words:
            print('Такого города нет. Введите корректное название города')
        # Переход к следуюещему ходу
        else:
            used_words.append(city_2)
            step = 'computer'
            city_1 = city_2