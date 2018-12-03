#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep

#임시 설정
temp_left_wheel = LargeMotor('outA')
temp_right_wheel = LargeMotor('outD')
temp_led = Leds()
temp_led.all_off()
sleep(1)
temp_left_wheel.run_forever(speed_sp = 100)
temp_right_wheel.run_forever(speed_sp = 100)
sleep(5.5)
temp_left_wheel.stop(stop_action = 'brake')
temp_right_wheel.stop(stop_action = 'brake')
del temp_left_wheel
del temp_right_wheel
del temp_led

# 초기 설정
from classMachine import *
from algorithm import *
machine = Machine()
machine.set_field()
machine.set_LCD()
machine.set_LED()
machine.set_color('in3', 'in2', 'in1')
machine.set_wheel('outA', 'outD')
machine.set_passenger('outB', 'outC')
machine.set_gyro('in4')

machine.direction = 90
machine.location_x = 0
machine.location_y = 0
machine.set_initial_direction()
machine.location_x = 0
machine.location_y = 0

# 1. 이동하면서 컬러를 탐지합니다
for i in range(6):
    machine.set_store_color()
    machine.run(1, machine.wheel.RUN_SPEED)
machine.turn(0, machine.wheel.TURN_SPEED)
for i in range(4):
    machine.set_store_color()
    machine.run(1, machine.wheel.RUN_SPEED)
machine.turn(270, machine.wheel.TURN_SPEED)
for i in range(6):
    machine.set_store_color()
    machine.run(1, machine.wheel.RUN_SPEED)
machine.turn(180, machine.wheel.TURN_SPEED)
for i in range(3):
    machine.set_store_color()
    machine.run(1, machine.wheel.RUN_SPEED)
machine.turn(90, machine.wheel.TURN_SPEED)
for i in range(6):
    machine.set_store_color()
    machine.run(1, machine.wheel.RUN_SPEED)

short_move(machine, 0, 0)
machine.locate(-1.5, 0, 'x')
machine.led.on('RED')
sleep(3)
machine.led.off()
sleep(1)

# 2 . 정보마당으로 이동하고 상점 색상을 인식, 최단경로를 계산합니다

machine.locate(0, 0, 'x')
short_move(machine, 0, 4)
machine.locate(-2.25, 4, 'x')
target_color = machine.color.COLOR_WORD[machine.color.middle_get_value()]
route = TSP(machine.field.store_color, target_color)
route_display = ""
for [x,y] in route:
    route_display += "%c%d " % (x+65, 5-y)
machine.lcd.print_text(route_display)
sleep(5)

# 3 . 최단경로를 따라 승객을 내려주고 출구로 이동합니다.
machine.locate(0, 4, 'x')
if machine.field.store_color[4][0] == target_color:
    machine.drop_passenger()
for i in range(1, len(route)):
    short_move(machine, route[i][0], route[i][1])
    if machine.field.store_color[route[i][1]][route[i][0]] == target_color:
        machine.drop_passenger()
machine.locate(7.5, 0, 'x')