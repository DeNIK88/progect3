# -*- coding: utf-8 -*-
import pymorphy3
import re
import random
import tkinter


def generate_text():
    text_area.delete(1.0, tkinter.END)
    text_area.insert(tkinter.END, declension())




# Возвращает случайную эмоцию
def random_emotion():
    emotions_file = open("emotions.txt", 'r', encoding='utf8')
    emotions_list = emotions_file.readlines()
    emotions_list = [i.rstrip('\n') for i in emotions_list]
    return random.choice(emotions_list)


# Возвращает имя и пол имени
def name_gender_analyzer():
    name_file = open('name_list.txt', 'r', encoding='utf8')
    name_list = name_file.readlines()
    name_list = [i.rstrip() for i in name_list]
    name_list_with_gender = []
    for i in name_list:
        gender = pymorphy3.MorphAnalyzer().parse(i)[0].tag.gender
        name_list_with_gender.append([i, gender])

    return random.choice(name_list_with_gender)


# Параграфы очищенные от порядкового номера. Возвращает случайный параграф.
def tamplates_split():
    tamplates_file = open('tamplates.txt', 'r', encoding='utf8').read()
    paragraphs = re.split(r'\n\n', tamplates_file.strip())
    random_paragraph = random.choice(paragraphs)
    random_paragraph = random_paragraph.replace('NAME_PLACEHOLDER', name[0])
    return random_paragraph[2::]


def declension():
    paragraph_split = tamplates_split().split()
    for j, i in enumerate(paragraph_split):
        if '*' in i:
            parse_word_without_symbols = re.sub(r'[^а-яА-ЯёЁ\s]+', '', i)
            morph = pymorphy3.MorphAnalyzer().parse(parse_word_without_symbols)[0] # Используя morph.parse("был"), вы получаете наиболее подходящий морфологический разбор слова "был", что позволяет затем использовать его для дальнейших манипуляций, таких как изменение рода с помощью метода inflect.
            if name[1] == 'femn':
                morph.inflect({'femn'}).word
                paragraph_split[j] = morph.inflect({'femn'}).word
            elif name[1] == 'masc':
                morph.inflect({'masc'}).word
                paragraph_split[j] = morph.inflect({'masc'}).word
            else:
                pass
        if '(V)' in i:
            paragraph_split[j] = paragraph_split[j].replace('(V)', random_emotion())

    joined_paragraph = ' '.join(paragraph_split)
    return joined_paragraph


name = name_gender_analyzer()

window = tkinter.Tk()
window.title('PROJECT')
window.geometry('400x300')

btn1 = tkinter.Button(window, text='Generate', command=generate_text)
btn1.pack(pady=10)


text_area = tkinter.Text(window, wrap='word', height=10, width=50)
text_area.pack(pady=10)

window.mainloop()
