#### Модели

Interview - Опрос

Question - Вопросы с типами

``QUESTION_OPTIONS = [('text', 'ответ текстом'),
                    ('multi', 'ответ с выбором нескольких вариантов'),
                    ('choice', 'ответ с выбором одного варианта'),
                    ]
                    ``
                    
Answer - ответы, не могут создаваться в вопросе типа text

UserAnswer - Ответы юзера с ссылками на вопросы и ответы или текст

Опрос считается запущенный если передано время старта `"started_at"`, а
закончиный `"ended_at"`
#### Создание Опросов

`POST /api/interview/`

```json
{
        "title": "Опрос 1",
        "started_at": "2020-10-16T12:12:35",
        "ended_at": null,
        "description": "тестовый опрос"
}
```

Ответ 

```json
{
    "id": 111,
    "title": "Опрос 1",
    "started_at": "2020-10-16T12:12:35Z",
    "ended_at": null,
    "description": "тестовый опрос",
    "questions": []
}
```

Или вложенный
```json
{
  "title":"Опрос 1",
  "started_at":"2020-10-16T12:12:35",
  "ended_at": null,
  "description":"тестовый опрос",
  "questions":[
    {
      "text":"vopros2",
      "type_question":"choice",
      "answers":[
        {
          "text":"текстовый ответ"
        },
        {
          "text":"текстовый ответ 2"
        }
      ]
    },
    {
      "text":"vopros1",
      "type_question":"text"
    },
    {
      "text":"vopros2",
      "type_question":"multi",
      "answers":[
        {
          "text":"текстовый ответ 2"
        },
        {
          "text":"текстовый ответ"
        }
      ]
    }
  ]
}

```

Ответ

```json
{
    "id": 112,
    "title": "Опрос 1",
    "started_at": "2020-10-16T12:12:35Z",
    "ended_at": null,
    "description": "тестовый опрос",
    "questions": [
        {
            "id": 17,
            "text": "vopros2",
            "type_question": "multi",
            "answers": [
                {
                    "id": 13,
                    "text": "текстовый ответ"
                },
                {
                    "id": 12,
                    "text": "текстовый ответ 2"
                }
            ]
        },
        {
            "id": 16,
            "text": "vopros1",
            "type_question": "text",
            "answers": []
        },
        {
            "id": 15,
            "text": "vopros2",
            "type_question": "choice",
            "answers": [
                {
                    "id": 14,
                    "text": "текстовый ответ 2"
                },
                {
                    "id": 15,
                    "text": "текстовый ответ"
                }
            ]
        }
    ]
}
```
`POST /api/interview/<id>/` - добавление по id также , защита от перезаписи
`PUT /api/interview/<id>/` - обновление по id
`DELETE /api/interview/<id>/` - удаление

#### Вопросы

`POST /api/question/<id>/` - добавление по id также , защита от перезаписи
`PUT /api/question/<id>/` - обновление по id
`DELETE /api/question/<id>/` - удаление

#### Варианты ответов


