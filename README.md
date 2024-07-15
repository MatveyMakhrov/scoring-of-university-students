# Student Scoring App
Приложение, предоставляющее функционал предсказывания количества долгов на следующей сессии по предудущим оценкам.

## Установка и запуск
Чтобы запустить приложение на ОС Windows, выполните следующие шаги:
1. Сконируйте этот репозиторий:
```
git clone https://github.com/MatveyMakhrov/scoring-of-university-students.git
```
2. Перейдите в папку репозитория и создайте в ней виртуальное окружение:
```
python -m venv .
```
3. Запустите виртуальное окружение:
```
Scripts\activate
```
4. Загрузите все используемые библиотеки:
```
pip install -r requirements.txt
```
5. Запустите файл приложения:
```
python application.py
```

## Работа с приложением

На главном экране приложения, нужно указать название группы, семестр и количество предметов в следующем семестре.

![image](https://github.com/MatveyMakhrov/scoring-of-university-students/blob/main/res/image_1.png)

Далее если нажать на кнопку "+", будут появляться новые строчки, с воможностью указания предмета и оценки.

![image](https://github.com/MatveyMakhrov/scoring-of-university-students/blob/main/res/image_2.png)

И после того, как указать все данные на студента, нужно нажать кнопку "Ок", чтобы предсказать количесвто долгов и долю в следующем семестре.

![image](https://github.com/MatveyMakhrov/scoring-of-university-students/blob/main/res/image_3.png)
