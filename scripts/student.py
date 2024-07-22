import numpy as np
import json

with open('./data/lessons_next.json', 'r', encoding='utf-8') as json_file:
    lessons_next = json.load(json_file)


with open('./data/lessons_third.json', 'r', encoding='utf-8') as json_file:
    lessons_third = json.load(json_file)


class NewStudent:
    def __init__(self, third):
        self.lessons = lessons_third if third is True else lessons_next
        self.programs = ['ББИ', 'БИВТ', 'БИСТ', 'БЛГ', 'БМН', 'БМТ',
                         'БМТМ', 'БНМ', 'БНМТ', 'БПИ', 'БПМ', 'БТМО',
                         'БФЗ', 'БЭК', 'БЭН', 'БЭЭ', 'СГД', 'СНТС', 'СФП']
        self.data = {key: 0 for key in list(self.lessons) + list(self.programs)}

    def load_data_from_dict(self, data_dict):
        for lesson, score in data_dict.items():
            if lesson in self.data:
                self.data[lesson] = score

    def prepare_data_for_prediction(self):
        return [self.data[key] for key in self.data]

    def data_processing(self):
        student_data = np.array(self.prepare_data_for_prediction()).reshape(1, -1)
        student_data = np.nan_to_num(student_data, nan=0, copy=True)
        return student_data
