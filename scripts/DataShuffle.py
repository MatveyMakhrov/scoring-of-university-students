import pandas as pd

# Показывает дисциплины как столбцы
def to_rows(k3):
    k3 = k3.join(pd.DataFrame({data.loc[0, "Дисциплина"]:[]}))
    k3.loc[0] = None
    k3.loc[0, "id"] = [data.loc[0, "Номер ЛД"]][0]
    k3.loc[0, "sem"] = [data.loc[0, "Семестр"]][0]
    k3.loc[0, "group"] = [data.loc[0, "Учебная группа"]][0]
    a = 0
    for i in range(len(data)):
        if data.loc[i, "Номер ЛД"] == k3.loc[a, "id"] and data.loc[i, "Семестр"] == k3.loc[a, "sem"]:
            if data.loc[i, "Дисциплина"] in k3.columns:
                if data.loc[i, "Оценка (без пересдач)"][0] in ["3", "4", "5"]:
                    k3.loc[a, data.loc[i, "Дисциплина"]] = int([data.loc[i, "Оценка (без пересдач)"]][0])
                else:
                    k3.loc[a, data.loc[i, "Дисциплина"]] = 2
            else:
                k3 = k3.join(pd.DataFrame({data.loc[i, "Дисциплина"]:[]}))
                if data.loc[i, "Оценка (без пересдач)"][0] in ["3", "4", "5"]:
                    k3.loc[a, data.loc[i, "Дисциплина"]] = int([data.loc[i, "Оценка (без пересдач)"]][0])
                else:
                    k3.loc[a, data.loc[i, "Дисциплина"]] = 2
        else:
            a = a + 1
            k3.loc[a] = None
            k3.loc[a, "id"] = [data.loc[i, "Номер ЛД"]][0]
            k3.loc[a, "group"] = [data.loc[i, "Учебная группа"]][0]
            k3.loc[a, "sem"] = [data.loc[i, "Семестр"]][0]
            if data.loc[i, "Оценка (без пересдач)"][0] in ["3", "4", "5"]:
                k3.loc[a, data.loc[i, "Дисциплина"]] = int([data.loc[i, "Оценка (без пересдач)"]][0])
            else:
                k3.loc[a, data.loc[i, "Дисциплина"]] = 2

# Оставляет только строки, где у кажого есть оценки за все 3 семестра
def norun():
    sem = 3
    for i in range(len(k3)):
        if sem == 3 and k3.loc[i, "sem"] == 1:
            sem = 1
        elif sem == 1 and k3.loc[i, "sem"] == 2:
            sem = 2
        elif sem == 2 and k3.loc[i, "sem"] == 3:
            sem = 3
        elif sem == 3:
            print(i + 2, sem, k3.loc[i, "sem"])
            k3 = k3.drop(i, axis=0)
            sem = 3
        elif sem == 2:
            print(i, i+1, sem)
            k3 = k3.drop(i - 2, axis=0)
            k3 = k3.drop(i - 1, axis=0)
            sem = 1
        elif sem == 1:
            print(i + 1, sem, k3.loc[i - 1, "sem"])
            k3 = k3.drop(i - 1, axis=0)
            sem = 1

k3 = pd.read_csv("~/3k.csv")

all = []

for i in range(len(k3)):
    d = 0
    t = 0
    c = 0
    p = 0
    for j in k3.columns:
        if k3.loc[i, j] == 5:
            p += 1
        elif k3.loc[i, j] == 4:
            c += 1
        elif k3.loc[i, j] == 3:
            t += 1
        elif k3.loc[i, j] == 2:
            d += 1
            
    if k3.loc[i, "group"][0:3] == "БЛГ":
        if k3.loc[i, "sem"] == 2 and k3.loc[i, "group"][0:6] == "БЛГ-20":
            d -= 3
        elif k3.loc[i, "sem"] == 3 and k3.loc[i, "group"][0:6] == "БЛГ-20":
            d -= 25
        elif k3.loc[i, "sem"] == 2 and k3.loc[i, "group"][0:6] == "БЛГ-21":
            d -= 3
        if k3.loc[i, "sem"] == 3 and k3.loc[i, "group"][0:6] == "БЛГ-21":
            d -= 6
    
    all.append([d, t, c, p])
        
#print(k3)
#k3.to_csv("~/3k.csv", index=False)

#БЛГ-20: 0, 3, 25
#БЛГ-21: 0, 3, 6
