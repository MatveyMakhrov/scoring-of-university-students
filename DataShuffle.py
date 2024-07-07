import pandas as pd

#Превращает оценки в int
def wordtoint():
    for i in range(len(data)):
        for j in data.columns:
            if pd.isna(data.loc[i, j]) or data.loc[i, j] in ["Неявка по ув.причине"]:
                data.loc[i, j] = 0
            elif data.loc[i, j] in ["не зачтено", "Неудовлетворительно", "Неявка"]:
                data.loc[i, j] = 2
            elif data.loc[i, j] in ["зачтено", "Удовлетворительно"]:
                data.loc[i, j] = 3
            elif data.loc[i, j] == "Хорошо":
                data.loc[i, j] = 4
            elif data.loc[i, j] == "Отлично":
                data.loc[i, j] = 5
                
#Создаёт list(list) со средними оценками в категориях для каждого студента
#В виде [Зач(2/3), З/О, Экз, Отчислен(0/1)], где 1 - отчислен
def average():
    if 2 < len(data.columns) and data.iloc[0, 2] in ["Зач", "З/О", "Экз"]:
        for i in range(len(data) - 1):
            row = [0, 0, 0]
            count = [0, 0, 0]
            for j in data.columns:
                if type(data.loc[i, j]) == int:
                    if data.loc[i, j] and data.loc[0, j] == "Зач":
                        row[0] += int(data.loc[i + 1, j])
                        count[0] += 1
                    elif data.loc[i, j] and data.loc[0, j] == "З/О":
                        row[1] += int(data.loc[i, j])
                        count[1] += 1
                    elif data.loc[i, j] and data.loc[0, j] == "Экз":
                        row[2] += int(data.loc[i, j])
                        count[2] += 1
            if count[0]:
                row[0] = round(row[0] / count[0], 3)
            if count[1]:
                row[1] = round(row[1] / count[1], 3)
            if count[2]:
                row[2] = round(row[2] / count[2], 3)
            
            if row != [0, 0, 0]:
                if "result" in data.columns and data.loc[i, "result"] in ["Да", "да"]:
                    row.append(1)
                elif "result" in data.columns and data.loc[i, "result"] in ["Нет", "нет"]:
                    row.append(0)
                res.append(row)
            
    else:
        print("Unable to count average")
        

#data = pd.read_excel("~/2k.xlsx")
data = pd.read_csv("~/2k.csv")
delete = ["№ \nп/п", "Учебная группа", "ФИО", "Номер ЛД", "Институт", "Долги", "Статус"]

#Удаляет колонки из delete, 
for i in data.columns:
    if i in delete:
        data = data.drop([i],axis=1)
        delete.remove(i)

res = []
wordtoint()
average()

print(res)