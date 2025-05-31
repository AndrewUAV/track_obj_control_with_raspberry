import time
from gpiozero import DigitalOutputDevice


class PPMGenerator:
    GAP = 100  

    def __init__(self, gpio, channels=6, frame_ms=20):
        self.gpio = gpio
        self.channels = channels

        
        self.frame_ms = frame_ms
        self._frame_us = int(frame_ms * 1000)
        self._frame_secs = frame_ms / 1000.0

        
        self._widths = [1500] * channels

        
        self.pin = DigitalOutputDevice(self.gpio)
        self.pin.off()

        self._update_time = time.time()

    def _update(self):
        
        micros = 0

        
        for i in self._widths:

            self.pin.on()
            time.sleep(self.GAP / 1000000.0)  
            micros += self.GAP

           
            self.pin.off()
            time.sleep(i / 1000000.0) 
            micros += i

        
        sync_length = self._frame_us - micros
        self.pin.on()
        time.sleep(self.GAP / 1000000.0)
        self.pin.off()
        time.sleep(sync_length / 1000000.0)

    def update_channel(self, channel, width):
        
        self._widths[channel] = width
        self._update()

    def update_channels(self, widths):
        "
        self._widths[:self.channels] = widths[:self.channels]
        self._update()

    def cancel(self):
        
        self.pin.off()


def generate_ppm(ch1=1500, ch2=1500, ch3=1500, ch4=1500, ch5=1500, ch6=1500):
    
    pulse_widths = [ch1, ch2, ch3, ch4, ch5, ch6]

    
    ppm = PPMGenerator(gpio=18, channels=6, frame_ms=20)

    
    ppm.update_channels(pulse_widths)

   
    time.sleep(2)

    
    ppm.cancel()


if __name__ == '__main__':
    generate_ppm()
