import time
from gpiozero import DigitalOutputDevice


class PPMGenerator:
    GAP = 100  # Ширина промежутка между импульсами (в мкс)

    def __init__(self, gpio, channels=6, frame_ms=20):
        self.gpio = gpio
        self.channels = channels

        # Устанавливаем параметры кадра и каналов
        self.frame_ms = frame_ms
        self._frame_us = int(frame_ms * 1000)
        self._frame_secs = frame_ms / 1000.0

        # Ширины импульсов для каналов по умолчанию
        self._widths = [1500] * channels

        # Настройка пина
        self.pin = DigitalOutputDevice(self.gpio)
        self.pin.off()

        self._update_time = time.time()

    def _update(self):
        """Обновление сигнала PPM."""
        micros = 0

        # Генерация сигнала для каждого канала
        for i in self._widths:
            # Высокий импульс
            self.pin.on()
            time.sleep(self.GAP / 1000000.0)  # Пауза на GAP в микросекундах
            micros += self.GAP

            # Низкий импульс
            self.pin.off()
            time.sleep(i / 1000000.0)  # Пауза на ширину импульса канала
            micros += i

        # Синхросигнал — конец кадра
        sync_length = self._frame_us - micros
        self.pin.on()
        time.sleep(self.GAP / 1000000.0)
        self.pin.off()
        time.sleep(sync_length / 1000000.0)

    def update_channel(self, channel, width):
        """Обновление ширины импульса для конкретного канала."""
        self._widths[channel] = width
        self._update()

    def update_channels(self, widths):
        """Обновление ширины импульсов для всех каналов."""
        self._widths[:self.channels] = widths[:self.channels]
        self._update()

    def cancel(self):
        """Остановка сигнала."""
        self.pin.off()


def generate_ppm(ch1=1500, ch2=1500, ch3=1500, ch4=1500, ch5=1500, ch6=1500):
    """Функция для генерации PPM сигнала на определенных каналах."""
    pulse_widths = [ch1, ch2, ch3, ch4, ch5, ch6]

    # Используем GPIO18 для отправки сигнала
    ppm = PPMGenerator(gpio=18, channels=6, frame_ms=20)

    # Обновляем каналы и начинаем генерацию
    ppm.update_channels(pulse_widths)

    # Работает 2 секунды
    time.sleep(2)

    # Останавливаем генерацию
    ppm.cancel()


if __name__ == '__main__':
    generate_ppm()
