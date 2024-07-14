from .scripts.student import NewStudent

import PySimpleGUI as sg

import pickle

# Импорт модели
with open('scoring.pkl', 'rb') as file:
    model = pickle.load(file)


def predict_student(data_dict):
    student = NewStudent()
    student.load_data_from_dict(data_dict)
    return model.predict(student.data_processing())[0].round().astype(int)

# Данные для выпадающего окна
scores = ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка', 'зачтено', 'не зачтено']

# Словарь, который будет заполняться пользователем и отправляться на модель.
data = {}

# Всё содержимое окна приложения
layout = [  [sg.Text('Учебная группа (например, "БПМ"):'), sg.InputText(key='-GROUP-', size=(10, 1)), sg.Text('Семестр:'), sg.InputText(key='-SEM-', size=(15, 1))],
            [sg.Text('Количество предметов студента на 3-ем семестре:'), sg.InputText(key='-COUNT-', size=(10 ,1))],
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

    data['Семестр'] = values['-SEM-']
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
                if values[score_key] == 'Отлично':
                    values[score_key] = '5'
                if values[score_key] == 'Хорошо':
                    values[score_key] = '4'
                if values[score_key] == 'Удовлетворительно':
                    values[score_key] = '3'
                if values[score_key] == 'Неудовлетворительно':
                    values[score_key] = '2'
                if values[score_key] == 'Неявка':
                    values[score_key] = '2'
                if values[score_key] == 'зачтено':
                    values[score_key] = '5'
                if values[score_key] == 'не зачтено':
                    values[score_key] = '2'
                data[subject] = values[score_key]
                # print(data)  # Выводим словарь для проверки

    # Если пользователь нажмёт 'Ок', Словарь полностью заполнится
    if event == 'Ок':
        count = values['-COUNT-']
        print(data)
        debts = predict_student(data)
        fraction = debts / int(count)
        if debts > 0:
            window['output1'].update(f'Вероятное число двоек в следующем семестре: {debts}', text_color='pink')
            window['output2'].update(f'Доля двоек в следующем семестре: {round(fraction, 2)}', text_color='pink')
        else:
            window['output1'].update(f'Скорее всего, двоек в следующем семестре нет!', text_color='lightgreen')

window.close()