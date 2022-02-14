from typing import Union, List


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывод сообщения с данными о тренировке"""
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000.
    HOUR_IN_MIN: float = 60.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return None

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEF_CAL_RUN_1: float = 18.
    COEF_CAL_RUN_2: float = 20.

    def get_spent_calories(self) -> float:
        """Получить количество
        затраченных калорий."""
        return ((self.COEF_CAL_RUN_1 * self.get_mean_speed()
                 - self.COEF_CAL_RUN_2)
                * self.weight / self.M_IN_KM * self.duration
                * self.HOUR_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CAL_WALK_1: float = 0.035
    COEF_CAL_WALK_2: float = 2.
    COEF_CAL_WALK_3: float = 0.029

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        walk_cal = ((self.COEF_CAL_WALK_1 * self.weight
                     + (super().get_mean_speed() ** self.COEF_CAL_WALK_2
                        // self.height) * self.COEF_CAL_WALK_3 * self.weight)
                    * self.duration * self.HOUR_IN_MIN)
        return walk_cal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_CAL_SWIM_1: float = 1.1
    COEF_CAL_SWIM_2: float = 2.

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEF_CAL_SWIM_1)
                * self.COEF_CAL_SWIM_2 * self.weight)


SP_DICT = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}


def read_package(workout_type: str, data: List[int]) -> Union[Training, None]:
    """Прочитать данные полученные от датчиков."""
    if workout_type in SP_DICT.keys():
        return SP_DICT[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    if training:
        info = training.show_training_info()
        print(info.get_message())
    else:
        print(f'Тренировка {workout_type} отсутствует.')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
