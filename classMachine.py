#!/usr/bin/env python3
from classPart import *


#각을 0~360도 범위 내로 변환하는 함수
def angle_range(angle):
    if angle < 0:
        while angle < 0:
            angle += 360
    elif angle >= 360:
        while angle >= 360:
            angle -= 360
    return angle

#기계의 각도를 라디안 각도로 변환하는 함수
def angle_to_radian(angle):
    return angle_range(-1*angle + 90) * math.pi / 180

#라디안 각도롤 기계의 각도로 변환하는 함수
def angle_to_machine(angle):    
    return angle_range(-1 * ((angle*180/math.pi) - 90)) 


#로봇
class Machine(): 

    #겍채 설정
    def set_field(self):                                  #경기장
        self.field = Field()
    def set_LCD(self):                                    #LCD
        self.lcd = LCD()
    def set_LED(self):                                    #LCD
        self.led = LED()
    def set_wheel(self, leftOut, rightOut):               #바퀴
        self.wheel = Wheel(leftOut, rightOut)
    def set_color(self, leftIn, middleIn, rightIn):       #컬러 센서
        self.color = Color(leftIn, middleIn, rightIn)
    def set_gyro(self, gyroIn):                           #자이로 센서
        self.gyro = Gyro(gyroIn)
    def set_passenger(self, rollerOut, gateOut):          #승객 내리는 장치
        self.passenger = Passenger(rollerOut, gateOut)    

    #변수
    direction = 0        #기계의 방향
    location_x = 0       #가계 구역 안에서의 x좌표
    location_y = 0       #가계 구역 안에서의 y좌표

    #함수
    #직진, block은 이동할 칸의 개수, speed는 속도
    def run(self, block, speed):
        self.gyro.set_mode('GYRO-ANG')
        standard_angle = self.gyro.get_value()
        standard_wheel_angle = self.wheel.left_get_position()
        if block < 0:
            speed *= -1
        while True:
            error = (standard_angle - self.gyro.get_value()) * 10
            self.wheel.left_run(speed + error)
            self.wheel.right_run(speed - error)
            if 2*math.pi*self.wheel.RADIUS*abs(self.wheel.left_get_position()-standard_wheel_angle)/360 >= abs(block)*self.field.BLOCK_LENGHT:
                break
        self.wheel.left_stop('hold')
        self.wheel.right_stop('hold')
        target_x = self.location_x + math.cos(angle_to_radian(self.direction)) * block
        target_y = self.location_y + math.sin(angle_to_radian(self.direction)) * block
        if (target_x != round(target_x)) and (math.log10(abs(target_x - round(target_x))) < -3):
            target_x = round(target_x)
        if (target_y != round(target_y)) and (math.log10(abs(target_y - round(target_y))) < -3):
            target_y = round(target_y)
        self.location_x = target_x
        self.location_y = target_y
        sleep(1)

    #포인트 턴, angle은 회전 방향
    def turn(self, angle, speed):
        angle = angle_range(angle)
        if angle != self.direction:
            self.gyro.set_mode('GYRO-ANG')
            standard_angle = self.gyro.get_value()
            relative_angle = angle_range(angle - self.direction)
            if relative_angle < 180:
                self.wheel.left_run(speed)
                self.wheel.right_run(speed * -1)
            else:
                self.wheel.left_run(speed * -1)
                self.wheel.right_run(speed)
                relative_angle = 360 - relative_angle
            while True:
                if abs(standard_angle - self.gyro.get_value()) > relative_angle:
                    break
            self.wheel.left_stop('hold')
            self.wheel.right_stop('hold')
            self.direction = angle
            sleep(1)

    #사선 이동, target_x는 목표 지점의 x좌표, target_y는 목표 지점의 y좌표
    def adjust(self, target_x, target_y, speed):
        dx = target_x - self.location_x
        dy = target_y - self.location_y
        dx_zero = False
        dy_zero = False
        if dx == 0:
            dx_zero = True
            dx = 0.000001
        if dy == 0:
            dy_zero = True

        if (dx_zero and dy_zero) == False:
            turn_speed = speed
            if turn_speed > self.wheel.TURN_SPEED:
                turn_speed = self.wheel.TURN_SPEED   
            goal_distance = math.sqrt(dx**2 + dy**2)
            goal_angle = angle_to_machine(math.atan(dy/dx))
            if (target_y != round(target_y)) and (math.log10(abs(goal_angle - round(goal_angle))) < -3):
                goal_angle = round(goal_angle)
            if target_x < self.location_x:
                goal_angle = angle_range(goal_angle + 180)
            self.turn(goal_angle, turn_speed)
            self.run(goal_distance, speed)

    #직각 이동, prior_direction은 가로/세로 이동 순서
    def locate(self, target_x, target_y, prior_direction):
        if prior_direction == 'x':
            self.adjust(target_x, self.location_y, self.wheel.RUN_SPEED)
            self.adjust(target_x, target_y, self.wheel.RUN_SPEED) 
        elif prior_direction == 'y':
            self.adjust(self.location_x, target_y, self.wheel.RUN_SPEED)
            self.adjust(target_x, target_y, self.wheel.RUN_SPEED)

    #검은 선을 이용한 초기 방향 설정
    def set_initial_direction(self):
        self.wheel.left_run(self.wheel.ADJUST_SPEED)
        self.wheel.right_run(self.wheel.ADJUST_SPEED)
        self.color.set_mode('COL-REFLECT')
        left_running, right_running = True, True
        while left_running or right_running:
            if self.color.left_get_value() <= 3:
                self.wheel.left_stop('hold')
                left_running = False
            if self.color.right_get_value() <= 2:
                self.wheel.right_stop('hold')
                right_running = False

    #해당 좌표에 있는 상점의 색을 저장함
    def set_store_color(self):
        self.color.set_mode('COL-COLOR')
        middle_value = self.color.middle_get_value()
        self.field.store_color[int(math.floor(self.location_y))][int(math.floor(self.location_x))] = self.color.COLOR_WORD[middle_value]

    #해당 좌표에서 승객을 한 명 내림
    def drop_passenger(self):    
        self.run(self.passenger.LOCATION_Y / self.field.BLOCK_LENGHT, self.wheel.ADJUST_SPEED)
        standard_gate_angle = self.passenger.gate_get_position()
        if self.passenger.PASSENGER_OUT == 0:
            self.passenger.gate_run(self.passenger.GATE_SPEED)
            while True:
                if abs(self.passenger.gate_get_position() - standard_gate_angle) > self.passenger.GATE_ANGLE:
                    break
            self.passenger.gate_stop('hold')
        else:
            standard_roller_angle = self.passenger.roller_get_position()
            self.passenger.roller_run(self.passenger.ROLLER_SPEED)
            while True:
                if abs(self.passenger.roller_get_position() - standard_roller_angle) > self.passenger.ROLLER_ANGLE:
                    break
            self.passenger.roller_stop('hold')
        self.run(self.passenger.LOCATION_Y / self.field.BLOCK_LENGHT * -1, self.wheel.ADJUST_SPEED)
        self.passenger.PASSENGER_OUT += 1
        sleep(1)