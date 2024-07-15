from scripts.student import NewStudent

import PySimpleGUI as sg

import pickle

# Импорт модели
with open('./models/scoring_next_sem.pkl', 'rb') as file:
    model_next_sem = pickle.load(file)

with open('./models/scoring_third_sem.pkl', 'rb') as file:
    model_third_sem = pickle.load(file)


def predict_next_sem(data_dict):
    data_dict['Семестр'] -= 1
    third = False
    student = NewStudent(third)
    student.load_data_from_dict(data_dict)
    return model_next_sem.predict(student.data_processing())[0].round().astype(int)


def predict_third_sem(data_dict):
    third = True
    student = NewStudent(third)
    student.load_data_from_dict(data_dict)
    return model_third_sem.predict(student.data_processing())[0].round().astype(int)


# Данные для выпадающего окна
scores = ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка', 'зачтено', 'не зачтено']

# Словарь, который будет заполняться пользователем и отправляться на модель.
data = {}

# Всё содержимое окна приложения
layout = [  [sg.Text('Учебная группа (например, "БПМ"):'), sg.InputText(key='-GROUP-', size=(10, 1)), sg.Text('Семестр предсказания:'), sg.InputText(key='-SEM-', size=(15, 1))],
            [sg.Text('Количество предметов студента в указанном семестре:'), sg.InputText(key='-COUNT-', size=(10 ,1))],
            [sg.Text('Чтобы добавить предмет, нажмите "+"'), sg.B('+', key='-ADD FRAME-')],
            [sg.Frame('', [[sg.T('Успеваемость')]], key='-FRAME-')],
            [sg.Button('Ок'), sg.Button('Закрыть'), sg.Text(size=(50, 1), key='output1', justification='right')],
            [sg.Text(size=(60, 1), key='output2', justification='right')] ]

# Создание окна.
window = sg.Window('Скоринг учащегося', layout)

i = 0  # Переменная для отслеживания номера строчки предмета и оценки.

# Цикл обработки событий для "events" и получения "values" входных данных.
while True:
    event, values = window.read()

    data['Семестр'] = int(values['-SEM-'])
    data[values['-GROUP-']] = 1

    # Если пользователь закроет окно или нажмет кнопку 'Закрыть'
    if event == sg.WIN_CLOSED or event == 'Закрыть':
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
    # Добавление данных об предметах в словарь
    else:
        debts = 0
        for key in values:
            if key.startswith('-IN-'):  
                idx = key.split('-')[2]
                subject = values[key]
                score_key = f'-SCORE-{idx}-'
                #print(values[score_key])

                score_mapping = {
                    'Отлично': 5,
                    'Хорошо': 4,
                    'Удовлетворительно': 3,
                    'Неудовлетворительно': 2,
                    'Неявка': 2,
                    'зачтено': 5,
                    'не зачтено': 2
                }

                score_value = score_mapping.get(values[score_key], 0)

                if subject in data:
                    data[subject] += score_value
                else:
                    data[subject] = score_value
                # print(data)  # Выводим словарь для проверки

    # Если пользователь нажмёт 'Ок', Словарь полностью заполнится
    if event == 'Ок':
        count = values['-COUNT-']
        print(data)
        if data['Семестр'] == 3:
            debts = predict_third_sem(data)
        else:
            debts = predict_next_sem(data)
        fraction = debts / int(count)
        data.clear()
        if debts > 0:
            window['output1'].update(f'Вероятное число двоек в следующем семестре: {debts}', text_color='pink')
            window['output2'].update(f'Доля двоек в следующем семестре: {round(fraction, 2)}', text_color='pink')
        else:
            window['output1'].update(f'Скорее всего, двоек в следующем семестре нет!', text_color='lightgreen')
            window['output2'].update(f'')

window.close()