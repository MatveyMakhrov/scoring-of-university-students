import numpy as np


class NewStudent:
    def __init__(self):
        self.lessons = [
            'Право', 'Физическая культура', 'Инженерная и компьютерная графика.1',
            'История.1', 'Безопасность жизнедеятельности', 'Инженерная и компьютерная графика',
            'История', 'Химия', 'Иностранный язык', 'Геодезия', 'Инженерная компьютерная графика',
            'Информатика', 'Программирование и алгоритмизация', 'Практическая фонетика',
            'Математика', 'Иностранный язык.1', 'Долги'
        ]
        self.scores = ['0','1', '2', '3', '4', '5']
        self.data = {lesson: np.NaN for lesson in self.lessons}

    def add_score(self, lesson, score):
        if lesson in self.data:
            self.data[lesson] = score

    def load_data_from_dict(self, data_dict):
        for lesson, score in data_dict.items():
            if lesson in self.data:
                self.data[lesson] = score
        debts = int(self.data['Долги'])
        debts *= -1
        self.data['Долги'] = str(debts)

    def data_processing(self):
        student_data = np.array(self.prepare_data_for_prediction()).reshape(1, -1)
        student_data = np.nan_to_num(student_data, nan=0, copy=True)
        return student_data

    def prepare_data_for_prediction(self):
        return [self.data[lesson] for lesson in self.lessons]