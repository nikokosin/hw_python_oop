
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000.0
    MINUTES_IN_HOUR: float = 60.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите калории в %s.' % type(self).__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration
                * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    """Константы для нащей формулы расчета каллорий для Ходьбы"""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    KMH_IN_MSEC: float = 0.278
    HEIGHT_DIV: float = 100.0
    MEAN_SPEED_POW_VALUE: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed_ms = (self.get_mean_speed() * self.KMH_IN_MSEC)
        height_in_meters = self.height / self.HEIGHT_DIV
        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight)
                + (mean_speed_ms ** self.MEAN_SPEED_POW_VALUE
                / height_in_meters) * self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight)
                * self.duration * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    """Константы для формулы"""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    CALORIES_MEAN_SPEED_SHIFT: float = 2.0
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость"""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время плавания."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    data_len = {
        'SWM': 5,
        'RUN': 3,
        'WLK': 4
    }

    try:
        if len(data) != data_len[workout_type]:
            raise ValueError(f'Неправильное количество'
                             f'элементов для {workout_type}')
        if not all(isinstance(x, (float, int)) for x in data):
            raise ValueError('В массиве присутствуют значения,'
                             ' отличные от целых чисел')
        return training_type[workout_type](*data)
    except KeyError:
        raise ValueError('Неизвестная тренировка')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('ВWQ', [1, 2, 3]),
        ('SWM', [720, 1, 80, 40, '21']),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except (ValueError, TypeError) as e:
            print(f"Ошибка: {e}")
