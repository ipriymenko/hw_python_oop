# Модуль фитнес-трекера

## Описание задания
Создать программный модуль для фитнес-трекера, используя парадигму ООП, который обрабатывает данные для трёх видов тренировок: бега, спортивной ходьбы и плавания.

## Описание решения

### Модуль содержит набор классов:
---
```python
class Training
    # Базовый класс треннировки
    def __init__(action: int, duration: float, weight: float)
        ...
``` 

##### СВОЙСТВА И МЕТОДЫ класса Training

* **action** - свойство содержит количество действий для тренировки (шагов, гребков, ..)
* **duration** - длительность тренировки в часах
* **weight** - вес участника тренировки
---
* **get_distance(self) -> float** - Получить дистанцию в км.
* **get_mean_speed(self) -> float** - Получить среднюю скорость движения.
* **show_training_info(self) -> InfoMessage** - Получить объект описывающий информацию о тренировке
* **get_spent_calories() -> float** — метод возвращает число потраченных калорий. Этот метод должен быть переопределен, в каждом производном классе, для учета специфики конкретного вида тренировки.

---
#### Производные классы **Running**, **SportWalking**, **Swimming**

```python
class Running(Training)
# класс для описывает тренировку по бегу

training = Running(action, duration, weight)
```

---
```python
class SportWalking(Training)
# класс для описывает тренировку по спортивной ходьбе

training = SportWalking(action, duration, weight, height)
```

* **height** - высота спортсмена в метрах

---
```python
class Swimming(Training)
# класс для описывает тренировку по плаванию

training = Swimming(action, duration, weight, length_pool, count_pool)
```

* **length_pool** - длина байсейна в метрах
* **count_pool** - число сколько раз спортсмен проплыл бассейн

### Утилиты

#### Декоратор для регистрации класса в индексе тренировок.

```python
@reg_workout(workout_type)
class SportWalking(Training)
    ...
```

* **workout_type** - код типа тренировки ('SWM','RUN','WLK'). Этот код присутствует в данных от сенсоров.

Каждый наследник класса **Training** описывающий конкретную тренировку (**Running, SportWalking, Swimming**) должен быть добавлен в индекс, что бы открыть для фитнес-трекера возможность распозновать тренировку и производить соответствующий расчет параметров тренировки.

```python
@reg_workout('SWM')
class SportWalking(Training)
    ...

@reg_workout('RUN')
class Running(Training)
    ...

@reg_workout('WLK')
class SportWalking(Training)
    ...

```

Для добавления нового вида тренировки, необходимо создать новый производный класс и зарегистрировать его в индексе тренировок с помощью декоратора:
```python

@reg_workout('ELP')
class Ellepsoiding(Training)
  ...
```

Количество принимаемых аргументов от сенсора для иницилизации объекта тренировки определяется количеством аргументов функции `__init__` класса (автоматически).
При необходимости можно указать явно:

```python
@reg_workout('ELP', 5)
class Ellepsoiding(Training)
  ...
```


