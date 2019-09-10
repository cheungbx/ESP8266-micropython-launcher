import os
import gc
from machine import Pin, I2C
from utime import sleep_ms, ticks_ms, ticks_diff

def pressed (btn) :
  v1 = btn.value()
  sleep_ms (20)
  if (not v1) and (not (btn.value())):
    while btn.value() :
       sleep_ms (10)
    return True
  else:
    return False
  
btnLeft = Pin(12, Pin.IN, Pin.PULL_UP)
btnRight = Pin(13, Pin.IN, Pin.PULL_UP)
btnUp = Pin(14, Pin.IN, Pin.PULL_UP)
btnDown = Pin(2, Pin.IN, Pin.PULL_UP)
btnA = Pin(0, Pin.IN, Pin.PULL_UP)
import ssd1306


# configure oled display I2C SSD1306
i2c = I2C(-1, Pin(5), Pin(4))   # SCL, SDA
display = ssd1306.SSD1306_I2C(128, 64, i2c)


SKIP_NAMES = ("boot", "main", "menu")


files = [item[0] for item in os.ilistdir(".") if item[1] == 0x8000]
      # print("Files: %r" % files)

module_names = [
    filename.rsplit(".", 1)[0]
    for filename in files
    if filename.endswith("py") and not filename.startswith("_")
]
module_names = [module_name for module_name in module_names if not module_name in SKIP_NAMES]
module_names.sort()
tot_file = len(module_names)
tot_rows = const(5)
screen_pos = 0
file_pos = 0

launched = False
while not launched :
  display.fill(0)
  display.text('ESP8266 uPython ', 5, 0, 1)
  i = 0
  for j in range (file_pos, min(file_pos+tot_rows, tot_file)) :
    current_row = 12 + 10 *i
    if i == screen_pos :
      display.fill_rect(5, current_row, 118, 10, 1)
      display.text(str(j) + " " + module_names[j], 5, current_row, 0)
    else:
      display.fill_rect(5, current_row, 118, 10, 0)
      display.text(str(j) + " " + module_names[j], 5, current_row, 1)     
    i+=1

  if pressed(btnUp):
    if screen_pos > 0 :
      screen_pos -= 1
    else :
        if file_pos > 0 :
          file_pos = max (0, file_pos - tot_rows)
          screen_pos=tot_rows-1
          
  if pressed(btnDown):
    if screen_pos < min(tot_file - file_pos - 1, tot_rows -1) :
      screen_pos = min(tot_file-1, screen_pos + 1)
    else :
      if file_pos + tot_rows < tot_file :
        file_pos = min (tot_file, file_pos + tot_rows)
        screen_pos=0

  if pressed(btnRight):
    display.fill(0)
    display.text("launching " , 5, 20, 1) 
    display.text(module_names[file_pos + screen_pos], 5, 40, 1) 
    display.show()
    sleep_ms(2000)
    gc.collect()  
    module = __import__(module_names[file_pos + screen_pos])  
    launched = True
  

  if pressed(btnLeft):
    launched = True  
    display.fill(0)
    display.text("exited ", 5, 24, 1) 
  display.show()


