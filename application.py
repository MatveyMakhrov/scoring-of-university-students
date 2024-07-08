import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from student import NewStudent

import PySimpleGUI as sg

import pickle

# Импорт модели
with open('scoring_cb.pkl', 'rb') as file:
    model = pickle.load(file)


def predict_student(data_dict):
    student = NewStudent()
    student.load_data_from_dict(data_dict)
    return model.predict(student.data_processing())[0]



# Данные для выпадающих окон (института и группы).
data_for_colleges = {
    'ИБО': ['БЛГ-20-1', 'БЛГ-20-11', 'БЛГ-20-12', 'БЛГ-20-13', 'БЛГ-20-4', 'БЛГ-20-5'],
    'ИНМиН': ['БМТМ-20-1', 'БНМТ-20-1', 'БФЗ-20-1', 'БЭН-20-2'],
    'ИТКН': ['ББИ-20-2', 'ББИ-20-4', 'БИВТ-20-1', 'БИВТ-20-3', 'БИВТ-20-5', 'БИВТ-20-6', 'БИВТ-20-7', 'БИСТ-20-1', 'БИСТ-20-2', 'БИСТ-20-3', 'БПИ-20-1', 'БПИ-20-2', 'БПИ-20-3', 'БПИ-20-4', 'БПИ-20-9', 'БПМ-20-1', 'БПМ-20-4'],
    'МГИ': ['БЭЭ-20-1', 'СГД-20-1', 'СГД-20-2', 'СГД-20-3', 'СГД-20-4', 'СГД-20-5', 'СГД-20-6', 'СФП-20-1'],
    'ЭкоТех': ['БМТ-20-1', 'БМТ-20-2', 'БТМО-20-1', 'БТМО-20-2'],
    'ЭУПП им. В.А. Роменца': ['БМН-20-1', 'БМН-20-2', 'БМН-20-3', 'БЭК-20-1', 'БЭК-20-3']
}

# Данные для выпадающих окон (предмета и оценки).
data_lessons = {'Право': ['зачтено', 'не зачтено'], 
                'Физическая культура': ['зачтено', 'не зачтено'], 
                'Инженерная и компьютерная графика.1': ['зачтено', 'не зачтено'], 
                'История.1': ['зачтено', 'не зачтено'], 
                'Безопасность жизнедеятельности': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Инженерная и компьютерная графика': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'История': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Химия': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Иностранный язык': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Геодезия': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Инженерная компьютерная графика': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Информатика': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Программирование и алгоритмизация': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Практическая фонетика': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Математика': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка'], 
                'Иностранный язык.1': ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно', 'Неявка']}

# Словарь, который будет заполняться пользователем
# и отправляться на модель.
data = {    
        # 'Институт': None,
        # 'Группа': None,
        'Право': '0',
        'Физическая культура': '0',
        'Инженерная и компьютерная графика.1': '0',
        'История.1': '0',
        'Безопасность жизнедеятельности': '0',
        'Инженерная и компьютерная графика': '0',
        'История': '0',
        'Химия': '0',
        'Иностранный язык': '0',
        'Геодезия': '0',
        'Инженерная компьютерная графика': '0',
        'Информатика': '0',
        'Программирование и алгоритмизация': '0',
        'Практическая фонетика': '0',
        'Математика': '0',
        'Иностранный язык.1': '0',
        'Долги': '0'
}

# Переменные для связи двух выпадающих окон (институт и группа).
colleges = list(data_for_colleges.keys())
groups = data_for_colleges[colleges[0]]

lessons = list(data_lessons.keys())
scores = data_lessons[lessons[0]]

# Всё содержимое окна приложения
layout = [  [sg.Text('ФИО студента:'), sg.InputText(key='-NAME-')],
            [sg.Text('Институт:'), sg.Combo(colleges, key='-COLLEGE-', enable_events=True), sg.Text('Группа:'), sg.Combo(groups, key='-GROUP-')],
            [sg.Text('Чтобы добавить предмет, нажмите "+"'), sg.B('+', key='-ADD FRAME-')],
            [sg.Frame('', [[sg.T('Успеваемость')]], key='-FRAME-')],
            [sg.Button('Ок'), sg.Button('Закрыть'), sg.Text(size=(40, 1), key='output', justification='right')] ]

# Создание окна.
window = sg.Window('Тестовое приложение', layout)

i = 0  # Переменная для отслеживания номера строчки предмета и оценки.


# Цикл обработки событий для "events" и получения "values" входных данных.
while True:
    event, values = window.read()

    # Если пользователь закроет окно или нажмет кнопку 'Закрыть'
    if event == sg.WIN_CLOSED or event == 'Закрыть':
        break

    # Если пользователь нажмёт на кнопку '+'
    if event == '-ADD FRAME-':
        new_combo_key = f'-IN-{i}-'
        new_score_key = f'-SCORE-{i}-'
        window.extend_layout(window['-FRAME-'], [[sg.T('Предмет:'),
                                                  sg.Combo(lessons, key=new_combo_key, enable_events=True), 
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
                # print(values[score_key])
                if subject in data and score_key in values:
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
                    if values[score_key] == '2':
                        debts += 1 
                    # print(data)  # Выводим словарь для проверки

    # Обработка изменения института
    if event == '-COLLEGE-':
        selected_colleges = values['-COLLEGE-']
        new_groups = data_for_colleges[selected_colleges]
        window['-GROUP-'].update(values=new_groups)

    # Обработка изменения предмета
    if event == new_combo_key:
        selected_lessons = values[new_combo_key]
        new_scores = data_lessons[selected_lessons]
        window[new_score_key].update(values=new_scores)

    # Если пользователь нажмёт 'Ок', Словарь полностью заполнится
    if event == 'Ок':
        # data['Институт'] = values['-COLLEGE-']
        # data['Группа'] = values['-GROUP-']
        data['Долги'] = debts
        print(data)
        if predict_student(data) == 1:
            window['output'].update('Студент отчислен!')
        else:
            window['output'].update('Студент не отчислен!')

window.close()