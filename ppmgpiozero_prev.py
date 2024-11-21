from gpiozero import DigitalOutputDevice
from time import sleep

# Настройка GPIO-пина
ppm_pin = DigitalOutputDevice(17)  # Используем GPIO17

# Параметры
num_channels = 8  # Количество каналов
pulse_width = 300 / 1_000_000  # Ширина импульса в секундах (300 мкс)
frame_length = 0.02  # Длина кадра в секундах (20 мс)
channels = [0.0015, 0.0016, 0.0017, 0.0015, 0.0018, 0.0019, 0.0014, 0.00155]  # Значения каналов в секундах

while True:
    current_time = 0
    for ch in channels:
        # Высокий уровень (импульс)
        ppm_pin.on()
        sleep(pulse_width)
        current_time += pulse_width

        # Низкий уровень (значение канала)
        ppm_pin.off()
        sleep(ch)
        current_time += ch

    # Синхросигнал
    sync_length = frame_length - current_time
    ppm_pin.on()
    sleep(pulse_width)
    ppm_pin.off()
    sleep(sync_length)
