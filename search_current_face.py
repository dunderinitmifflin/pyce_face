# press button
# take pic
# get rek id for face
# if yes
#  search against db for rek id
#  if exists
#   turn light green
#   print name of person
#  else turn on red light

from send_pic_to_register import take_pic, query_mysql_db_for_rek_id, turn_on_one_led_or_none
from get_rek_id import search_faces
from time import sleep

pin_green = 13
pin_yellow = 6
pin_red = 5

#RPi
from gpiozero import Button
btn = Button(17)

def on_button_press():
    turn_on_one_led_or_none(pin_yellow)
    take_pic()
    rek_id = search_faces()
    if rek_id is not None:
        result = query_mysql_db_for_rek_id(rek_id)
        print(result)
        if result is not None:
            turn_on_one_led_or_none(pin_green)
        else:
            turn_on_one_led_or_none(pin_red)
        sleep(2)
        turn_on_one_led_or_none()
    else:
        print(rek_id)
        turn_on_one_led_or_none(pin_red)
        sleep(2)
        turn_on_one_led_or_none()
        
if __name__ == '__main__':
    print('button ready to be pressed')
    while True:
        btn.when_pressed = on_button_press