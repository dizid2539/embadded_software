#!/usr/bin/env python3

def short_move(machine, target_x, target_y):
    machine_middle = False
    target_middle = False
    if machine.location_y == 2 or machine.location_y == 3:
        machine_middle = True
    if target_y == 2 or target_y == 3:
        target_middle = True

    if machine_middle and target_middle:
        machine_up_gap = abs(4 - machine.location_y)
        machine_down_gap = abs(1 - machine.location_y)
        target_up_gap = abs(4 - target_y)
        target_down_gap = abs(1 - target_y)

        if machine_up_gap + target_up_gap <= machine_down_gap + target_down_gap:
            machine.locate(target_x, 4, 'y')
            machine.locate(machine.location_x, target_y, 'y')
        else:
            machine.locate(target_x, 1, 'y')
            machine.locate(machine.location_x, target_y, 'y')

    elif machine_middle or target_middle:
        if machine_middle:
            machine.locate(target_x, target_y, 'y')
        else:
            machine.locate(target_x, target_y, 'x')

    else:
        if ((machine.location_y == 4) ^ (target_y == 4)) == False:
            machine.locate(target_x, target_y, 'x')
        else:
            machine_left_gap = abs(machine.location_x - 0)
            machine_right_gap = abs(machine.location_x - 6)
            target_left_gap = abs(target_x - 0)
            target_right_gap = abs(target_x - 6)

            if machine_left_gap + target_left_gap <= machine_right_gap + target_right_gap:
                machine.locate(0, target_y, 'x')
                machine.locate(target_x, machine.location_y, 'x')
            else:
                machine.locate(6, target_y, 'x')
                machine.locate(target_x, machine.location_y, 'x')

def short_distance(location1_x, location1_y, location2_x, location2_y):
    location1_middle = False
    location2_middle = False
    if location1_y == 2 or location1_y == 3:
        location1_middle = True
    if location2_y == 2 or location2_y == 3:
        location2_middle = True

    if location1_middle and location2_middle:
        location1_up_gap = abs(4 - location1_y)
        location1_down_gap = abs(1 -location1_y)
        location2_up_gap = abs(4 - location2_y)
        location2_down_gap = abs(1 - location2_y)
        if location1_up_gap + location2_up_gap <= location1_down_gap + location2_down_gap:
            return location1_up_gap + location2_up_gap + 6
        else:
            return location1_down_gap + location2_down_gap + 6
    
    elif location1_middle or location2_middle:
        return abs(location1_x - location2_x) + abs(location1_y - location2_y)

    else:
        if ((location1_y == 4) ^ (location2_y == 4)) == False:
            return abs(location1_x - location2_x) + abs(location1_y - location2_y)
        else:
            location1_left_gap = abs(location1_x - 0)
            location1_right_gap = abs(location1_x - 6)
            location2_left_gap = abs(location2_x - 0)
            location2_right_gap = abs(location2_x - 6)
            if location1_left_gap + location2_left_gap <= location1_right_gap + location2_right_gap:
                return location1_left_gap + location2_left_gap + abs(location1_y - location2_y)
            else:
                return location1_right_gap + location2_right_gap + abs(location1_y - location2_y)

def TSP_core(route):
    route[1] = 1
    traveled_store = [1,1]
    result = route[:]
    temp_get_info = []
    temp_set_info = []
    for i in range(2, store_quantity):
        if route[i] > traveled_store[0]:
            traveled_store[0] = route[i]
            traveled_store[1] = i

    if traveled_store[0] == store_quantity - 1:
        result[store_quantity] = store_quantity
        result[0] = route_distance[traveled_store[1]-1][store_quantity-1]
        return result
    else:
        for i in range(2, store_quantity):
            if route[i] == 0:
                temp_set_info = route[:]
                temp_set_info[i] = traveled_store[0] + 1
                temp_get_info = TSP_core(temp_set_info)
                temp_distance = route_distance[traveled_store[1]-1][i-1] + temp_get_info[0]
                if temp_distance < result[0]:
                    result = temp_get_info
                    result[0] = temp_distance
        return result
    
def TSP(store_color, target_color):
    global route_distance
    global store_quantity
    store_location = []
    route_distance = []
    result = []
    route = []

    for y in range(4, -1, -1):
        for x in range(7):
            if x == 0 and y == 4:
                store_location.append([0,4])
            elif x == 6 and y == 0:
                store_location.append([6,0])
            elif store_color[y][x] == target_color:
                store_location.append([x,y])
    store_quantity = len(store_location)
    for i in range(store_quantity):
        temp_distance = []
        for j in range(store_quantity):
            temp_distance.append(short_distance(store_location[i][0], store_location[i][1], store_location[j][0], store_location[j][1]))
        route_distance.append(temp_distance[:])
    route.append(10000)
    for i in range(store_quantity):
        route.append(0)
    route = TSP_core(route)
    for i in range(store_quantity):
        for j in range(store_quantity):
            if route[j+1] == i+1:
                result.append(store_location[j][:])
    return result
