from scripts.student import NewStudent

import PySimpleGUI as sg

import pickle
import json
from collections import defaultdict

# Импорт модели
with open('./models/scoring_next_sem.pkl', 'rb') as file:
    model_next_sem = pickle.load(file)

with open('./models/scoring_third_sem.pkl', 'rb') as file:
    model_third_sem = pickle.load(file)

score_mapping = {
    'Отлично': 5,
    'Хорошо': 4,
    'Удовлетворительно': 3,
    'Неудовлетворительно': 2,
    'Неявка': 2,
    'зачтено': 5,
    'не зачтено': 2
}


def predict_student(data_dict):
    if data_dict['Семестр'] == 3:
        student = NewStudent(third=True)
        student.load_data_from_dict(data_dict)
        return model_third_sem.predict(student.data_processing())[0].round().astype(int)
    else:
        data_dict['Семестр'] -= 1
        student = NewStudent(third=False)
        student.load_data_from_dict(data_dict)
        return model_next_sem.predict(student.data_processing())[0].round().astype(int)


def handle_duplicates(pairs):
    d = defaultdict(int)
    for key, value in pairs:
        if value in score_mapping:
            value = score_mapping.get(value, value)
            d[key] += value
        elif key in ['Семестр', 'Количество предметов']:
            value = int(value)
            d[key] = value
        else:
            d[key] = value
            continue
        print(value)
    return dict(d)


# Данные для выпадающего окна
scores = ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка', 'зачтено', 'не зачтено']

# Словарь, который будет заполняться пользователем и отправляться на модель.
data = {}

# Массив для временного хранения данных о предметах
rows = []

# Всё содержимое окна приложения
layout = [
    [
        sg.Text('Учебная группа (например, "БПМ"):'), sg.InputText(key='-GROUP-', size=(10, 1)),
        sg.Text('Семестр предсказания:'), sg.InputText(key='-SEM-', size=(15, 1))
    ],
    [
        sg.Text('Количество предметов студента в указанном семестре:'), sg.InputText(key='-COUNT-', size=(10, 1))
    ],
    [
        sg.Text('Чтобы добавить предмет, нажмите "+"'), sg.Button('+', key='-ADD FRAME-')
    ],
    [sg.Frame('', [[sg.Text('Успеваемость')]], key='-FRAME-')],
    [sg.Text("Или загрузите JSON-файл со всеми данными:")],
    [
        sg.FileBrowse(file_types=(("JSON Files", "*.json"),), button_text="Выберите файл", key='-FILE-BROWSE-', pad=(5, 10)),
        sg.InputText(key='-FILE-', readonly=True)
    ],
    [
        sg.Button('Предсказать', key='predict', pad=(5, 0), size=(12, 0)),
        sg.Text(key='output1')
    ],
    [
        sg.Text(' ', size=(12, 0), pad=(5, 0)),
        sg.Text(key='output2')
    ]
]

# Создание окна.
window = sg.Window('Скоринг учащегося', layout)

i = 0  # Переменная для отслеживания номера строчки предмета и оценки.

# Цикл обработки событий для "events" и получения "values" входных данных.
while True:
    event, values = window.read()

    # Если пользователь закроет окно или нажмет кнопку 'Закрыть'
    if event == sg.WIN_CLOSED:
        break

    # Если пользователь нажмёт на кнопку '+'
    if event == '-ADD FRAME-':
        new_combo_key = f'-IN-{i}-'
        new_score_key = f'-SCORE-{i}-'
        window.extend_layout(window['-FRAME-'], [[sg.T('Предмет:'),
                                                  sg.InputText(key=new_combo_key),
                                                  sg.T('Оценка:'),
                                                  sg.Combo(scores, key=new_score_key)]])
        i += 1

    # Если пользователь нажмёт 'Ок', Словарь полностью заполнится
    if event == 'predict':
        count = 1
        if values['-GROUP-'] and values['-SEM-'] and values['-COUNT-']:
            for key in values:
                if key.startswith('-IN-'):
                    idx = key.split('-')[2]
                    subject = values[key]
                    score_key = f'-SCORE-{idx}-'
                    # print(values[score_key])

                    score_value = score_mapping.get(values[score_key], 0)

                    if subject in data:
                        data[subject] += score_value
                    else:
                        data[subject] = score_value
            data['Семестр'] = int(values['-SEM-'])
            data[values['-GROUP-']] = 1
            count = int(values['-COUNT-'])
            data = {k: v for k, v in data.items() if k != ''}
        else:
            filename = values['-FILE-']
            if filename:
                with open(filename, 'r', encoding='utf-8') as file:
                    raw_data = json.load(file, object_pairs_hook=handle_duplicates)
                print(raw_data)
                raw_data['Семестр'] = int(raw_data['Семестр'])
                raw_data[raw_data['Группа']] = 1
                raw_data = {key: score_mapping.get(value, value) for key, value in raw_data.items()}

                data = {}
                for key, value in raw_data.items():
                    if key in data:
                        data[key] += value
                    else:
                        data[key] = value

                count = int(data['Количество предметов'])
                del data['Группа']
                del data['Количество предметов']
                print(data)

        third = False
        semester = data['Семестр']

        debts = predict_student(data)
        fraction = debts / count
        data.clear()

        window['output1'].update(f'Семестр предсказания: {semester}')
        if debts > 0:
            window['output2'].update(f'Вероятное число двоек: {debts}, доля двоек: {round(fraction, 2)}', text_color='pink')
        else:
            window['output3'].update(f'Скорее всего, двоек в указанном семестре нет!', text_color='lightgreen')

window.close()