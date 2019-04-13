import time
from queue import Queue
import numpy as np
from drone_autonomous_escape import DroneControl


class TrackObject(object):

    def __init__(self, drone):
        # drone init
        self.drone = drone
        self.drone_control = DroneControl(self.drone)

        # target init
        self.coords = None
        self.x = 0
        self.y = 0
        self.z = 0
        self.Yaw = 0
        self.Yaw_save = 0
        self.reach_goal = False
        self.landing = False
        self.fast_land = False
        self.once_land = True

        # to avoid jumps in coords
        cap = 50
        self.pre_x = Queue(maxsize=cap)
        self.pre_y = Queue(maxsize=cap)
        self.pre_z = Queue(maxsize=cap)
        self.pre_Yaw = Queue(maxsize=cap)

        # 30 cm from target
        self.goal = 68
        self.min_angle = 10
        self.max_angle = 50
        self.min_x = 20
        self.min_y = 20
        self.min_z = 60

        self.new_track = False
        self.has_saw = False
        # height deter

        self.global_height = 0
        self.backup_height = 0
        self.once_height = True

        # if cant see target  dont move
        # if cant see target for x sec  ,to avoid unstable detection
        self.count_to_backwards = 0.3
        self.start_counter_backwards = 0
        self.finish_counter_backwards = self.count_to_backwards

        # to write file
        self.file_flag = False
        self.file = None
        self.flag_count_write = True
        self.count_to_write = 2
        self.start_write = 0
        self.finish_write = 0
        self.forward_log = 0
        self.backward_log = 0
        self.right_log = 0
        self.left_log = 0
        self.up_log = 0
        self.down_log = 0
        self.clockwise_log = 0
        self.counter_clockwise_log = 0

    def main(self):
        if self.reach_goal:
            self.hard_land()
        else:
            self.track()

    # algorithm

    def track(self):

        if self.new_track:
            print("point: ", (self.x), (self.y), (self.z), (self.Yaw))
            if not self.side_check():
                self.follow_right_left()
            if not self.height_check():
                self.follow_height()
            if self.side_check() and self.height_check():
                self.follow_forward()
            # if self.Yaw_check() and self.side_check():
            #     self.follow_forward()

    def hard_land(self):
        self.fast_land = True
        self.drone_control.stop_time = 0
        if 10 < self.global_height or (40 < self.z and self.new_track):
            self.drone_control.forward(self.goal)
            self.forward_log = self.goal
            self.drone_control.down(999)
            self.down_log = 999
        else:
            self.landing = True
            self.drone.land()

    # update coords

    def update_coords(self, coords):
        if not self.new_track:
            return
        # queue is full need to empty
        if self.pre_x.full():
            self.pre_x.get()
            self.pre_y.get()
            self.pre_z.get()
            self.pre_Yaw.get()
        else:
            self.pre_x.put(int(coords[0]))
            self.pre_y.put(int(coords[1]))
            self.pre_z.put(int(coords[2]))
            self.pre_Yaw.put(int(coords[3]))

        self.x = self.most_common(self.pre_x)
        self.y = self.most_common(self.pre_y) - 20
        self.z = self.most_common(self.pre_z) + 3
        self.Yaw = self.most_common(self.pre_Yaw)
        # self.Yaw=self.angle_from_rot()

    def most_common(self, lst):
        lst = (list(lst.queue))
        lst = np.asarray([lst])
        return np.median(lst)

    def is_new(self, new_track):

        if new_track:
            self.has_saw = new_track
            self.start_counter_backwards = time.time()
            self.finish_counter_backwards = 0
            self.new_track = True

            if self.x == 0 and self.y == 0 and self.z == 0: return
            self.box_update()

            if self.goal < self.z - 10:
                self.reach_goal = False
            else:
                self.reach_goal = True

        else:
            if self.has_saw:
                if not self.reach_goal:
                    self.x = 0
                    self.y = 0
                    self.z = 0
                self.finish_counter_backwards = time.time()
                if self.finish_counter_backwards - self.start_counter_backwards > self.count_to_backwards:
                    self.new_track = False

    # adjust drone to target

    def box_update(self):
        if not self.new_track: return
        half = (self.z + self.goal) / 2
        qut = (half + self.goal) / 2
        if 4 * self.goal < self.z:
            self.min_y = 60
            self.min_x = 50
        elif 2 * self.goal <= self.z <= 4 * self.goal:
            self.min_y = 40
            self.min_x = 40

        elif self.z < 2 * self.goal:
            self.min_y = 50
            self.min_x = 30

    def spot_target(self):
        return self.new_track

    def orbit_move(self):
        # if left and left or right and right
        if self.Yaw * self.x < 0:
            self.save_Yaw = self.Yaw
            while not self.Yaw_check():
                self.drone_control.forward(3)
                if self.save_Yaw < 0:
                    self.drone_control.yaw(-1)
                else:
                    self.drone_control.yaw(1)
        #
        #
        # else:
        #      dist = (np.pi * self.Yaw * self.z) / 180
        #      if dist<0: ##rot left
        #          self.drone_control.left(-1*dist)
        #      else:
        #          self.drone_control.right(dist)
        #
        # else:
        #      if not self.side_check():
        #          self.follow_rightLeft()
        #
        #      else:
        #          dist=(np.pi*self.Yaw*self.z)/180
        #          if dist<0: ##rot left
        #              self.drone_control.right(-1*dist)
        #          else:
        #              self.drone_control.left(dist)
        #          if not self.Yaw_check():
        #              self.follow_rotation()
        #

    def follow_forwardBackward(self):
        if not self.new_track: return
        if self.goal < self.z:
            self.drone_control.forward(self.z - self.goal)
            self.forward_log = self.z - self.goal
        else:
            self.drone_control.backward((self.goal - self.z))
            self.backward_log = (int((self.goal - self.z)))

    def follow_forward(self):
        if not self.new_track: return
        if self.goal <= self.z:
            self.drone_control.forward(5 + self.z - self.goal)
            self.forward_log = 5 + self.z - self.goal

    def Yaw_check(self):
        """ if angle less then min_ang return ok

        :return:
        """
        # ang<x<ang
        check_left = -1 * self.max_angle < self.Yaw < -1 * self.min_angle
        check_right = self.min_angle < self.Yaw < self.max_angle
        return not (check_left or check_right)

    def side_check(self):
        """ if inside -x ___ x return ok

        :return:
        """
        return -1 * self.min_x < self.x < self.min_x

    def height_check(self):
        """ if inside -y ___ y return ok

        :return:
        """
        return -1 * self.min_y < self.y < self.min_y

    def follow_height(self):
        if not self.new_track:
            return
        if 0 < self.y:
            self.drone_control.up(self.y)
            self.up_log = self.y
        else:
            self.drone_control.down(-1 * self.y)
            self.down_log = -1 * self.y

    def follow_right_left(self):
        if not self.new_track: return
        if 0 < self.x:
            self.drone_control.right(self.x)
            self.right_log = self.x
        else:
            self.drone_control.left(-1 * self.x)
            self.left_log = -1 * self.x

    def height_deter(self, height):
        self.update_height()
        # if self.once_height:
        #     self.once_height=False
        #     self.backup_height=self.global_height
        #
        # if  self.global_height!=height and self.backup_height!=height:
        height = height - self.global_height

        if 0 < height:
            self.drone_control.up(height)
            self.up_log = height
            self.backup_height = height
        else:
            self.drone_control.down(-1 * height)
            self.down_log = -1 * height
            self.backup_height = -1 * height

    def follow_rotation(self):
        if not self.new_track: return
        self.drone_control.yaw(self.Yaw)
        rot_status = self.Yaw
        if rot_status < 0:
            self.clockwise_log = rot_status
        else:
            self.counter_clockwise_log = rot_status

    def angle_from_rot(self):
        angle = np.arctan2(self.z, self.x)
        angle = np.degrees(angle)

        if 0 < self.x:
            angle = 90 - angle
            return angle

        else:
            angle = angle - 90
            return angle

    # file writing

    def set_export_data(self, name):
        self.file = open(name + ".txt", "w+")
        self.file_flag = True

    def finish_export_data(self):
        if self.file_flag:
            self.file.close()

    def export_data(self):
        if self.file_flag:

            if self.flag_count_write:
                self.start_write = time.time()
                self.flag_count_write = False
                self.finish_write = 0
            else:
                self.finish_write = time.time()

            if self.finish_write - self.start_write > self.count_to_write:  ##write every x sec
                self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA, self.handler)
                self.flag_count_write = True

    def handler(self, event, sender, data, **args):
        drone = sender
        if event is drone.EVENT_FLIGHT_DATA:
            self.file.write(
                "fly_time|" + "height|" + "east_speed|" + "north speed|" + "forward|" + "backward|" + "right|" + "left|" + "up|" + "down|" + "clockwise|" + "counter_clockwise|" + "target|" + "reach_goal|" + "landing|")
            self.file.write(str(int(data.fly_time)) + "\n")
            self.file.write(str(data.height * 10) + "|")
            self.file.write(str(data.east_speed) + "|")
            self.file.write(str(data.north_speed) + "|")
            self.file.write(str(int(self.forward_log)) + "|")
            self.file.write(str(int(self.backward_log)) + "|")
            self.file.write(str(int(self.right_log)) + "|")
            self.file.write(str(int(self.left_log)) + "|")
            self.file.write(str(int(self.up_log)) + "|")
            self.file.write(str(int(self.down_log)) + "|")
            self.file.write(str(int(self.clockwise_log)) + "|")
            self.file.write(str(int(self.counter_clockwise_log)) + "|")
            self.file.write("(" + str(int(self.x)) + "," + str(int(self.y)) + "," + str(int(self.z)) + ") |")
            self.file.write(str(self.reach_goal) + "|")
            self.file.write(str(self.new_track) + "|")
            self.file.write(str(self.landing) + "\n")

            self.forward_log = 0
            self.backward_log = 0
            self.right_log = 0
            self.left_log = 0
            self.up_log = 0
            self.down_log = 0
            self.clockwise_log = 0
            self.counter_clockwise_log = 0

    # update heught
    def update_height(self):
        self.drone.subscribe(self.drone.EVENT_FLIGHT_DATA, self.handler_height)

    def handler_height(self, event, sender, data, **args):
        drone = sender
        if event is drone.EVENT_FLIGHT_DATA:
            self.global_height = data.height * 10
