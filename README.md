# CF_take_tasks

```
pip install requests2
```
json формат для ввода из файла input.json:
```
{
  "plot": [2000, 2500], // рейтинг задач [l, r]
  "tags": [], // теги для задач,
  "ban_tags": ["fft", "*special"], // запрещенные теги для задач
  "handles": ["_Stefan_", "tox1c_kid"], // хендлы пользователей, у которых не должно быть посылок по задачам
  "number_of_problems": 4, // кол-во генерируемых задач
  "output_tags": false // нужно ли выводить теги задач
}
```
