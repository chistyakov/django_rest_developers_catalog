# Task from job interview

С использованием Django REST Framework разработать два REST-сервиса, отдающих данные в формате JSON о разработчиках. Внести себя и еще несколько выдуманных кандидатов.
 
Пример моделей для использования (можно использовать любые, которые посчитаете нужным):
1. Developer
2. Skill
3. University
4. Company
 
Требуемые сервисы:

1. Список разработчиков
```shell
GET /developers/
```
 
Пример ответа:

```javascript
[{ 
 'name': 'Иван',
 'surname': 'Иванов',
 'skills': ['Python', 'Django', 'Django REST Framework'],
 'education': [{
  'university': {'name': 'Saint-Petersburg State University'},
  'year_of_graduation': '2016',
 }],
 'employment_history': [{
   'company': {'name': 'Horns and Hooves'},
   'role': 'Junior Python Developer'
   'from': '2017-02-01',
   'to': '2017-09-01'
 }],
}]
```
 
Предусмотреть фильтрацию по скиллам (GET /developers?skill=python&skill=django)
 

2. Конкретный разработчик
```shell
GET /developers/1
```


## How to run
```shell
docker build . -t developers
docker run -d -p 8000:8000 --name developers developers
```
