import time
import pigpio


class PPMGenerator:
    WAVES = 5
    GAP = 100

    def __init__(self, pi, gpio, channels=6, frame_ms=20):
        self.pi = pi
        self.gpio = gpio


        if frame_ms < 5:
            frame_ms = 5
            channels = 2
        elif frame_ms > 100:
            frame_ms = 100

        self.frame_ms = frame_ms
        self._frame_us = int(frame_ms * 1000)
        self._frame_secs = frame_ms / 1000.0

        if channels < 1:
            channels = 1
        elif channels > (frame_ms // 2):
            channels = int(frame_ms // 2)

        self.channels = channels

        self._widths = [1500] * channels

        self._wid = [None] * self.WAVES
        self._next_wid = 0

        pi.write(gpio, pigpio.LOW)

        self._update_time = time.time()

    def _update(self):

        wf = []
        micros = 0

        for i in self._widths:
            wf.append(pigpio.pulse(0, 1 << self.gpio, self.GAP))
            wf.append(pigpio.pulse(1 << self.gpio, 0, i))
            micros += (i + self.GAP)

        wf.append(pigpio.pulse(0, 1 << self.gpio, self._frame_us - micros))

        self.pi.wave_add_generic(wf)
        wid = self.pi.wave_create()
        self.pi.wave_send_using_mode(wid, pigpio.WAVE_MODE_REPEAT_SYNC)
        self._wid[self._next_wid] = wid

        self._next_wid += 1
        if self._next_wid >= self.WAVES:
            self._next_wid = 0

        remaining = self._update_time + self._frame_secs - time.time()
        if remaining > 0:
            time.sleep(remaining)
        self._update_time = time.time()

        wid = self._wid[self._next_wid]
        if wid is not None:
            self.pi.wave_delete(wid)
            self._wid[self._next_wid] = None

    def update_channel(self, channel, width):
        self._widths[channel] = width
        self._update()

    def update_channels(self, widths):
        self._widths[:self.channels] = widths[:self.channels]
        self._update()

    def cancel(self):
        self.pi.wave_tx_stop()
        for i in self._wid:
            if i is not None:
                self.pi.wave_delete(i)


def generate_ppm(ch1=1500, ch2=1500, ch3=1500, ch4=1500, ch5=1500, ch6=1500):
    """
    :param ch1: none
    :param ch2: pulse signal for roll angle
    :param ch3: pulse signal for pitch angle
    :param ch4: pulse signal for throttle
    :param ch5: pulse signal for yaw angle
    :param ch6: none
    :return: nothing
    """
    pulse_widths = [ch1, ch2, ch3, ch4, ch5, ch6]

    pi = pigpio.pi()

    if not pi.connected:
        exit(0)

    pi.wave_tx_stop()

    ppm = PPMGenerator(pi, gpio=18, channels=6, frame_ms=20)

    ppm.update_channels(pulse_widths)

    time.sleep(2)

    ppm.cancel()

    pi.stop()


if __name__ == '__main__':
    generate_ppm()