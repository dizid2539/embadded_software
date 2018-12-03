#!/usr/bin/env python3
from ev3dev.ev3 import *
import ev3dev.fonts as fonts
from time import sleep
import math

#단위 : 길이(mm), 시간(초), 각도(도)

#경기장
class Field(): 
    #상수
    BLOCK_LENGHT = 220        #칸의 길이
    SRORE_OUT_RADIUS = 35     #상점 바깥쪽 원 반지름
    SRORE_IN_RADIUS = 20      #상점 안쪽 원 반지름

    #변수
    store_color = [['NULL']*7 for i in range(5)]    #상점의 색상


#바퀴
class Wheel(): 

    #초기 객체 설정
    def __init__(self, leftOut, rightOut): 
        self.left = LargeMotor(leftOut)
        self.right = LargeMotor(rightOut)

    #상수
    RADIUS  = 27          #바퀴의 반지름
    RUN_SPEED = 100       #직진 시 회전 속도
    TURN_SPEED = 50      #회전 시 이동 속도
    ADJUST_SPEED = 50    #조정 시 이동 속도 

    #함수
    def left_get_position(self):                    #왼쪽 바퀴 각도 구하기
        return self.left.position
    def right_get_position(self):                   #오른쪽 바퀴 각도 구하기
        return self.right.position
    def left_run(self, speed):                      #왼쪽 바퀴 회전
        self.left.run_forever(speed_sp = speed)
    def right_run(self, speed):                     #오른쪽 바퀴 회전
        self.right.run_forever(speed_sp = speed)    
    def left_stop(self, stop_type):                 #왼쪽 바퀴 정지
        self.left.stop(stop_action = stop_type)
    def right_stop(self, stop_type):                #오른쪽 바퀴 정지
        self.right.stop(stop_action = stop_type)


#컬러 센서
class Color():

    #초기 객체 설정
    def __init__(self, leftIn, middleIn, rightIn):
        self.left = ColorSensor(leftIn)
        self.middle = ColorSensor(middleIn)
        self.right = ColorSensor(rightIn)

    #상수
    WHITEBLACK = 15                  #흰색-검은색 구별을 위한 반사광 감도 경계값
    COLOR_WORD = []                  #색상 배열(숫자->명칭)
    COLOR_WORD.append('NULL')
    COLOR_WORD.append('BLACK')
    COLOR_WORD.append('BLUE')
    COLOR_WORD.append('GREEN')
    COLOR_WORD.append('YELLOW')    
    COLOR_WORD.append('RED')
    COLOR_WORD.append('WHITE')
    COLOR_WORD.append('BROWN')

    #함수
    def set_mode(self, mode):         #컬러 센서 모드 설정하기
        self.left.mode = mode
        self.middle.mode = mode
        self.right.mode = mode
    def left_get_value(self):         #왼쪽 컬러 센서 값 구하기
        return self.left.value()
    def middle_get_value(self):      #가운데 컬러 센서 값 구하기
        return self.middle.value()
    def right_get_value(self):        #오른쪽 컬러 센서 값 구하기
        return self.right.value()    


#자이로 센서
class Gyro(): 

    #초기 객체 설정
    def __init__(self, gyroIn):
        self.gyro = GyroSensor(gyroIn)

    #함수
    def set_mode(self, mode):       #자이로 센서 모드 정하기
        self.gyro.mode = mode
    def get_value(self):            #자이로 센서 값 구하기
        return self.gyro.value()    


#승객 내리는 장치
class Passenger(): 
    
    #초기 객제 설정
    def __init__(self, rollerOut, gateOut):
        self.roller = MediumMotor(rollerOut)
        self.gate = MediumMotor(gateOut)

    #상수
    LOCATION_Y = 70          #승객 내리는 장치의 세로 위치
    ROLLER_SPEED = -75      #돌림 모터를 작동시키는 빠르기
    GATE_SPEED = 150         #문 모터를 작동시키는 빠르기
    ROLLER_ANGLE = 90        #한 명의 승객을 내리는 데 돌림 모터를 작동하는 각도
    GATE_ANGLE = 40          #문을 열고 닫는 데 문 모터를 작동하는 각도
    PASSENGER_OUT = 0        #내린 승객 수

    #함수
    def roller_get_position(self):                             #돌림 모터 각도 구하기
        return self.roller.position
    def roller_run(self, speed):                               #돌림 모터 작동
        self.roller.run_forever(speed_sp = speed)
    def roller_stop(self, stop_type):                          #돌림 모터 정지
        self.roller.stop(stop_action = stop_type)
    def gate_get_position(self):                             #문 모터 각도 구하기
        return self.gate.position
    def gate_run(self, speed):                                 #문 모터 작동
        self.gate.run_forever(speed_sp = speed)
    def gate_stop(self, stop_type):                            #문 모터 정지
        self.gate.stop(stop_action = stop_type)   


#LCD 화면
class LCD(Screen):

    #함수
    def print_text(self, text):    #lcd에 글자 출력
        self.clear()                                            
        self.draw.text((10,10), text, font=fonts.load('luBS12'))  
        self.update()


#버튼 LED                                                        
class LED(Leds):

    #함수
    def on(self, color):    #led 켜기
        if color == 'RED':
            led_color = self.RED
        if color == 'GREEN':
            led_color = self.GREEN
        if color == 'YELLOW':
            led_color = self.YELLOW
        if color == 'ORANGE':
            led_color = self.ORANGE
        if color == 'AMBER':
            led_color = self.AMBER
        self.set_color(self.LEFT, led_color)
        self.set_color(self.RIGHT, led_color)     

    def off(self):          #led 끄기
        self.all_off()