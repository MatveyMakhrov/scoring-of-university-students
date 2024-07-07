import PySimpleGUI as sg

#Данные для выпадающих окон
data_for_colleges = {
    'ИБО': ['БЛГ-20-1', 'БЛГ-20-11', 'БЛГ-20-12', 'БЛГ-20-13', 'БЛГ-20-4', 'БЛГ-20-5'],
    'ИНМиН': ['БМТМ-20-1', 'БНМТ-20-1', 'БФЗ-20-1', 'БЭН-20-2'],
    'ИТКН': ['ББИ-20-2', 'ББИ-20-4', 'БИВТ-20-1', 'БИВТ-20-3', 'БИВТ-20-5', 'БИВТ-20-6', 'БИВТ-20-7', 'БИСТ-20-1', 'БИСТ-20-2', 'БИСТ-20-3', 'БПИ-20-1', 'БПИ-20-2', 'БПИ-20-3', 'БПИ-20-4', 'БПИ-20-9', 'БПМ-20-1', 'БПМ-20-4'],
    'МГИ': ['БЭЭ-20-1', 'СГД-20-1', 'СГД-20-2', 'СГД-20-3', 'СГД-20-4', 'СГД-20-5', 'СГД-20-6', 'СФП-20-1'],
    'ЭкоТех': ['БМТ-20-1', 'БМТ-20-2', 'БТМО-20-1', 'БТМО-20-2'],
    'ЭУПП им. В.А. Роменца': ['БМН-20-1', 'БМН-20-2', 'БМН-20-3', 'БЭК-20-1', 'БЭК-20-3']
}

lessons = ['Право', 'Физическая культура', 'Безопасность жизнедеятельности', 'Инженерная и компьютерная графика', 'Химия', 'Иностранный язык', 'Геодезия', 'Инженерная компьютерная графика', 'Информатика', 'Программирование и алгоритмизация', 'Практическая фонетика', 'Математика']
scores = ['2', '3', '4', '5']

data = {    
        'Институт': None,
        'Группа': None,
        'Право': '0',
        'Физическая культура': '0',
        'Безопасность жизнедеятельности': '0',
        'Инженерная и компьютерная графика': '0',
        'Химия': '0',
        'Иностранный язык': '0',
        'Геодезия': '0',
        'Инженерная компьютерная графика': '0',
        'Информатика': '0',
        'Программирование и алгоритмизация': '0',
        'Практическая фонетика': '0',
        'Математика': '0',
        'Иностранный язык': '0'
}

colleges = list(data_for_colleges.keys())
groups = data_for_colleges[colleges[0]]

# All the stuff inside your window.
layout = [  [sg.Text('ФИО студента:'), sg.InputText(key='-NAME-')],
            [sg.Text('Институт:'), sg.Combo(colleges, key='-COLLEGE-', enable_events=True), sg.Text('Группа:'), sg.Combo(groups, key='-GROUP-')],
            [sg.Text('Чтобы добавить предмет, нажмите "+"'), sg.B('+', key='-ADD FRAME-')],
            [sg.Frame('', [[sg.T('Успеваемость')]], key='-FRAME-')],
            [sg.Button('Ок'), sg.Button('Закрыть')] ]

# Create the Window
window = sg.Window('Тестовое приложение', layout)

i = 0

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Закрыть':
        break
    if event == '-ADD FRAME-':
        new_combo_key = f'-IN-{i}-'
        new_score_key = f'-SCORE-{i}-'
        window.extend_layout(window['-FRAME-'], [[sg.T('Предмет:'),
                                                  sg.Combo(lessons, key=new_combo_key, enable_events=True), 
                                                  sg.T('Оценка:'), 
                                                  sg.Combo(scores, key=new_score_key)]])
        i += 1
    else:
        for key in values:
            # if key not in ['-COLLEGE-', '-GROUP-']:
            #     print('')
            #     # continue
            if key.startswith('-IN-'):  
                idx = key.split('-')[2]
                subject = values[key]
                score_key = f'-SCORE-{idx}-'
                # print(subject)
                #print(subject)
                #print(score_key) 
                if subject in data and score_key in values:
                    data[subject] = values[score_key]
                    # print(data)  # Выводим словарь для проверки

    # Обработка изменения института
    if event == '-COLLEGE-':
        selected_colleges = values['-COLLEGE-']
        new_groups = data_for_colleges[selected_colleges]
        window['-GROUP-'].update(values=new_groups)

    if event == 'Ок':
        data['Институт'] = values['-COLLEGE-']
        data['Группа'] = values['-GROUP-']
        print(data)

window.close()