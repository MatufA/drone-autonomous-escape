import threading
import time


class DroneControl(object):
    """
    high level api  control drone with cm as value, height, forward,backward,left,right and clockwise_spin
    control height with 1 "time sleep": 100 cm = 1 sec
    4d with 1 "time sleep": 300 cm = val per time sec
    control time with "time sleep" as val - 360 deg = 4 sec
    """

    def __init__(self, drone):
        self.drone = drone
        self.val_per_time = 1
        self.stop_time = 2
        self.forward_running = False
        self.forward_val = 0
        self.backward_running = False
        self.backward_val = 0
        self.right_running = False
        self.left_running = False
        self.left_val = 0
        self.up_running = False
        self.up_val = 0
        self.down_running = False
        self.down_val = 0
        self.clockwise_running = False
        self.clockwise_val = 0
        self.counter_clockwise_running = False
        self.counter_clockwise_val = 0
        self.yaw_running = False
        self.yaw_angle = 0
        self.yaw_neg = False
        self.min_angle = 0

    def val_to_height(self, height):
        """ max height to move is 100 cm
    
        :param height: 
        :return: 
        """""
        if height > 100:
            height = 100
        elif height < 0:
            height = 0
        return int(height / self.val_per_time)

    def val_to_down(self, height):
        """ max height to move is 5 cm

        :param height:
        :return:
        """
        if height > 100:
            height = 100
        elif height < 0:
            height = 0
        return int(height / self.val_per_time)

    def val_to_4d(self, dist):
        """ max dist to move is 300 cm

        :param dist:
        :return:
        """
        if 300 < dist:
            dist = 100
        elif dist < 0:
            dist = 0
        return int(dist / (self.val_per_time * 3))

    def val_to_clock(self, deg):
        """ max deg is 90

        :param deg:
        :return:
        """
        if 90 < deg:
            deg = 90
        elif deg < 0:
            deg = 0
        return (10 * deg) / (9 * self.val_per_time)

    def _forward_thread(self):
        self.drone.forward(self.forward_val)
        time.sleep(self.val_per_time)
        self.drone.forward(0)
        # stop
        time.sleep(self.stop_time)
        self.forward_val = 0
        self.forward_running = False

    def forward(self, dist):
        """ control drone forward

        :param dist:
        :return:
        """
        if not self.forward_running:
            self.forward_running = True
            self.forward_val = self.val_to_4d(dist)
            self.forward_thread = threading.Thread(target=self._forward_thread).start()

    def _backward_thread(self):
        self.drone.backward(self.backward_val)
        time.sleep(self.val_per_time)
        self.drone.backward(0)
        time.sleep(self.stop_time)  ##stop
        self.backward_val = 0
        self.backward_running = False

    def backward(self, dist):
        """ control drone forward

        :param dist:
        :return:
        """
        if not self.backward_running:
            self.backward_running = True
            self.backward_val = self.val_to_4d(dist)
            self.backward_thread = threading.Thread(target=self._backward_thread).start()

    def _right_thread(self):
        self.drone.right(self.right_val)
        time.sleep(self.val_per_time)
        self.drone.right(0)
        time.sleep(self.stop_time)  ##stop
        self.right_val = 0
        self.right_running = False

    def right(self, dist):
        """ control drone forward

        :param dist:
        :return:
        """
        if not self.right_running:
            self.right_running = True
            self.right_val = self.val_to_4d(dist)
            self.right_thread = threading.Thread(target=self._right_thread).start()

    def _left_thread(self):
        self.drone.left(self.left_val)
        time.sleep(self.val_per_time)
        self.drone.left(0)
        # stop
        time.sleep(self.stop_time)
        self.left_val = 0
        self.left_running = False

    def left(self, dist):
        """ control drone forward

        :param dist:
        :return:
        """
        if not self.left_running:
            self.left_running = True
            self.left_val = self.val_to_4d(dist)
            self.left_thread = threading.Thread(target=self._left_thread).start()

    def _up_thread(self):
        self.drone.up(self.up_val)
        time.sleep(self.val_per_time / 10)
        self.drone.up(0)
        # stop
        time.sleep(self.stop_time)
        self.up_val = 0
        self.up_running = False

    def up(self, dist):
        """ control drone forward

        :param dist:
        :return:
        """
        if not self.up_running:
            self.up_running = True
            self.up_val = self.val_to_height(dist)
            self.up_thread = threading.Thread(target=self._up_thread).start()

    def _down_thread(self):
        self.drone.down(self.down_val)
        time.sleep(self.val_per_time)
        self.drone.down(0)
        time.sleep(self.stop_time)  ##stop
        self.down_val = 0
        self.down_running = False

    def down(self, dist):
        """ control drone forward

        :param dist:
        :return:
        """
        if not self.down_running:
            self.down_running = True
            self.down_val = self.val_to_height(dist)
            self.down_thread = threading.Thread(target=self._down_thread).start()

    def _clockwise_thread(self):
        self.drone.clockwise(self.clockwise_val)
        time.sleep(self.val_per_time)
        self.drone.clockwise(0)
        time.sleep(self.stop_time)  ##stop
        self.clockwise_val = 0
        self.clockwise_running = False

    def clockwise(self, degree):
        """ control drone clockwie

        :param degree:
        :return:
        """
        if not self.clockwise_running:
            self.clockwise_running = True
            self.clockwise_val = self.val_to_clock(degree)
            self.clockwise_thread = threading.Thread(target=self._clockwise_thread).start()

    def _counter_clockwise_thread(self):
        self.drone.counter_clockwise(self.counter_clockwise_val)
        time.sleep(self.val_per_time)
        self.drone.counter_clockwise(0)
        time.sleep(self.stop_time)  ##stop
        self.counter_clockwise_val = 0
        self.counter_clockwise_running = False

    def counter_clockwise(self, degree):
        """ control drone clockwise

        :param degree:
        :return:
        """
        if not self.counter_clockwise_running:
            self.counter_clockwise_running = True
            self.counter_clockwise_val = self.val_to_clock(degree)
            self.counter_clockwise_thread = threading.Thread(target=self._counter_clockwise_thread).start()

    def _yaw_thread(self):
        if self.yaw_neg:
            self.clockwise(-1 * self.yaw_angle)
        else:
            self.counter_clockwise(self.yaw_angle)
        time.sleep(self.stop_time)  ##stop
        self.yaw_running = False

    def yaw(self, angle):
        """ calc angle  x,z scale, not moving forward

        :param angle:
        :return:
        """
        if not self.yaw_running:
            self.yaw_running = True
            if 0 < angle:
                self.yaw_neg = False
            else:
                self.yaw_neg = True
            self.yaw_angle = angle
            self.yaw_thread = threading.Thread(target=self._yaw_thread).start()

    # def Yaw(self,x,z): ### calc angle  x,z scale, not moving forward
    #     if not self.Yaw_running:
    #         self.Yaw_running=True
    #         angle=np.arctan2(z,x)
    #         angle=np.degrees(angle)
    #
    #         if 0<x:
    #             angle = 90 -angle
    #             self.Yaw_neg=False
    #         else:
    #             angle = angle - 90
    #             self.Yaw_neg=True
    #         if angle < self.min_angle: return
    #         self.Yaw_angle = angle
    #         self.Yaw_thread= threading.Thread(target=self._Yaw_thread).start()

    def get_angle(self):
        """ get angle and clock/counter clock

        :return:
        """
        return self.yaw_angle, self.yaw_neg

    def to_object(self, x, y, z):
        """ calc angle x,z scale and move in y scale and forward

        :param x:
        :param y:
        :param z:
        :return:
        """
        if x != 0:
            self.yaw(x)
        if 0 < y:
            self.up(y)
            self.forward(z)
        else:
            y = -1 * y
            self.down(y)
            self.forward(z)
