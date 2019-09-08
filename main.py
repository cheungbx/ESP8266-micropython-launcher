import gc
from machine import Pin, I2C
from utime import sleep_ms, ticks_ms, ticks_diff
btnLeft = Pin(12, Pin.IN, Pin.PULL_UP)
btnRight = Pin(13, Pin.IN, Pin.PULL_UP)
btnUp = Pin(14, Pin.IN, Pin.PULL_UP)
btnDown = Pin(2, Pin.IN, Pin.PULL_UP)
btnA = Pin(0, Pin.IN, Pin.PULL_UP)
import ssd1306

# configure oled display I2C SSD1306
i2c = I2C(-1, Pin(5), Pin(4))   # SCL, SDA

display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.fill(0)
display.text('ESP8266 uPython ', 5, 0, 1)
gc.collect()
print (gc.mem_free())
display.text('Mem:'+str(gc.mem_free()), 5, 8, 1)
display.text('U = Brick', 5, 16, 1)
display.text('D = Snake', 5, 24, 1)
display.text('L = LHT', 5, 32,  1)
display.text('R = ...', 5, 40,  1)
display.text('A = Exit', 5, 48,  1)
display.show()
countdown = 5
timer = ticks_ms()
while countdown > 0 :
  countdown = 5 - int (ticks_diff(ticks_ms(), timer) // 1000)
  if not btnA.value():
    countdown = 0
  gc.collect()
  if not btnUp.value():
    import brick
  if not btnDown.value():
    import snake
  if not btnLeft.value():
    import lht
  if not btnRight.value():
    pass
  display.fill_rect( 110, 40, 18, 8, 0)
  display.text(str(countdown), 110, 40,  1)
  display.show()
display.fill(0)
display.text('Exited', 5, 40,  1)
display.show()

