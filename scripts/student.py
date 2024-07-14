import numpy as np
import json

with open('./data/lessons.json', 'r', encoding='utf-8') as json_file:
    lessons = json.load(json_file)


class NewStudent:
    def __init__(self):
        self.lessons = lessons
        self.programs = ['ББИ', 'БИВТ', 'БИСТ', 'БЛГ', 'БМН', 'БМТ',
                         'БМТМ', 'БНМ', 'БНМТ', 'БПИ', 'БПМ', 'БТМО',
                         'БФЗ', 'БЭК', 'БЭН', 'БЭЭ', 'СГД', 'СНТС', 'СФП']
        self.scores = ['0', '1', '2', '3', '4', '5']
        self.data = {key: np.NaN for key in list(self.lessons) + list(self.programs)}

    def add_score(self, key, score):
        if key in self.data:
            self.data[key] = score

    def load_data_from_dict(self, data_dict):
        for lesson, score in data_dict.items():
            if lesson in self.data:
                self.data[lesson] = score

    def data_processing(self):
        student_data = np.array(self.prepare_data_for_prediction()).reshape(1, -1)
        student_data = np.nan_to_num(student_data, nan=0, copy=True)
        return student_data

    def prepare_data_for_prediction(self):
        return [self.data[key] for key in self.data]