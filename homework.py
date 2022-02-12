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

    def get_message(self):
        message = (f"Тип тренировки: {self.training_type}; "
                   f"Длительность: {self.duration:.3f} ч.; "
                   f"Дистанция: {self.distance:.3f} км; "
                   f"Ср. скорость: {self.speed:.3f} км/ч; "
                   f"Потрачено ккал: {self.calories:.3f}.")
        # выводимое сообщение
        # все значения типа float
        # округляются до 3 знаков после запятой
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

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
        # базовая формула расчёта
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # базовая формула расчёта
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # формула расчёта
        kr1: int = 18
        kr2: int = 20
        kt: int = 60
        run_cal = ((kr1 * super().get_mean_speed() - kr2)
                   * self.weight / self.M_IN_KM * self.duration * kt)
        return run_cal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        kw1 = 0.035
        kw2 = 2
        kw3 = 0.029
        kt = 60
        # формула расчёта
        walk_cal = (kw1 * self.weight
                    + (super().get_mean_speed() ** kw2 // self.height)
                    * kw3 * self.weight) * self.duration * kt
        return walk_cal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        swim_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return swim_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        ks1 = 1.1
        ks2 = 2
        swim_cal = (Swimming.get_mean_speed(self) + ks1) * ks2 * self.weight
        return swim_cal


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    sport_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}

    for i in range(len(data)):
        if workout_type == sport_dict[workout_type]:
            sport_dict[workout_type](*data)

    return sport_dict[workout_type](*data)


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
