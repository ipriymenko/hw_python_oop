"""СПРИНТ 2. ПРОЕКТ ФИТНЕС-ТРЕККЕР"""
import inspect
from typing import Callable, Type

# Словарь - индекс, связывает класс тренировки с данными
workout_index = {}


class TrainingInitInfo:
    """Класс с данными необходимыми для создания объекта тренировки
    по типу тренировки"""

    def __init__(self, cls: Type, data_len: int) -> None:
        self.cls = cls
        self.data_len = data_len


def reg_workout(workout_type: str, data_len: int = -1) -> Callable:
    """Декоратор, для регистрации типов тренировки.
        workout_type - тип тренировки,
        data_len - необходимое число аргументов для конструктора тренировки,
            если = -1, то определить автоматически (по умолч.)
    """

    def decor(cls: Type) -> Type:
        trn_inf = TrainingInitInfo(cls, (data_len if data_len >= 0 else len(
            inspect.getfullargspec(getattr(cls, "__init__")).args) - 1))
        workout_index[workout_type] = trn_inf
        return cls

    return decor


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить текст информационного сообщения."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """Информация о тренировке:
            action - количество действий (шагов)
            duration - время тренировки в ч.
            weight - вес в кг.
        """
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0.0

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@reg_workout("RUN")
class Running(Training):
    """Тренировка: бег."""
    LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время бега."""
        return ((self.CALORIES_MEAN_SPEED_SHIFT
                 + self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed())
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H
                )


@reg_workout("WLK")
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CM_IN_M = 100
    KMH_IN_MSEC = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """Информация о тренировке:
            action - количество шагов
            duration - время тренировки в ч.
            weight - вес в кг.
            height - рост в м. или см.
        """
        super().__init__(action, duration, weight)
        self.height = height if height < 3 else height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время ходьбы."""
        return (
            ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
              + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                 / self.height)
              * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
             * self.duration * self.MIN_IN_H)
        )


@reg_workout("SWM")
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 2
    CALORIES_MEAN_SPEED_SHIFT = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        """Информация о тренировке:
            action - количество шагов
            duration - время тренировки в ч.
            weight - вес в кг.
            length_pool - длинна бассейна в м.
            count_pool - сколько раз переплыл бассейн.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время плавания."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.weight * self.duration
                )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in workout_index:
        raise Exception(f'Wrong workout type "{workout_type}" '
                        f'(expected types: {list(workout_index.keys())})!')

    expected_args = workout_index[workout_type].data_len
    if expected_args != len(data):
        raise Exception(f'Wrong data length for workout "{workout_type}" '
                        f'(expected {expected_args}, got {len(data)})!')

    return workout_index[workout_type].cls(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
