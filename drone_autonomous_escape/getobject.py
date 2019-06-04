import numpy as np
import threading
import cv2.aruco as aruco
import cv2
import math
import time
import os


class GetObject(object):

    def __init__(self, config):
        # Define Tag
        self.id_to_find = 1
        # [cm]
        self.marker_size = 20
        # Define drone setup
        self.running = False
        self.flag_vid = False
        self.vid = None
        self.t_read = 0
        self.fps_read = 0
        self.t_detect = 0
        self.fps_detect = 0
        self.new_val = False
        self.camera_matrix = np.loadtxt(os.path.join(config.camera_lib_path, config.camera_metrix), delimiter=',')
        self.camera_distortion = np.loadtxt(os.path.join(config.camera_lib_path, config.camera_distortion),
                                            delimiter=',')
        # 180 deg rotation matrix around the x axis
        self.R_flip = np.zeros((3, 3), dtype=np.float32)
        self.R_flip[0, 0] = 1.0
        self.R_flip[1, 1] = -1.0
        self.R_flip[2, 2] = -1.0

        # Define the aruco dictionary
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        self.parameters = aruco.DetectorParameters_create()

        # obj coords
        self.x = 0
        self.y = 0
        self.z = 0
        self.Yaw = 0
        self.pre_Yaw = 0
        self.gap = 20
        self.yaw_once = True
        self.obj_pixel = None

    # ------------------------------------------------------------------------------
    # ------- ROTATIONS https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    # ------------------------------------------------------------------------------
    # Checks if a matrix is a valid rotation matrix.
    def isRotationMatrix(self, R):
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype=R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

    # Calculates rotation matrix to euler angles
    # The result is the same as MATLAB except the order
    # of the euler angles ( x and z are swapped ).
    def rotationMatrixToEulerAngles(self, R):
        assert (self.isRotationMatrix(R))

        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

        singular = sy < 1e-6

        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0

        return np.array([x, y, z])

    def update_fps_read(self):
        t = time.time()
        self.fps_read = 1.0 / (t - self.t_read)
        self.t_read = t

    def update_fps_detect(self):

        t = time.time()
        self.fps_detect = 1.0 / (t - self.t_detect)
        self.t_detect = t

    def set_vid(self, vid):
        self.flag_vid = True
        self.vid = vid

    def update(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._update_thread).start()

    def _update_thread(self):

        if self.flag_vid:
            # Read the camera frame
            frame = self.vid

            self.update_fps_read()

            # min_x, min_y = frame.shape[:2]
            # mid_img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # # use color detector.
            # vid = detector.track_obj(frame=mid_img, min_x=min_x, min_y=min_y, max_x=0, max_y=0)
            # self.vid = cv2.resize(vid, (self.w, self.h))

            # Convert in gray scale
            # remember, OpenCV stores color images in Blue, Green, Red
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #
            # # Find all the aruco markers in the image
            # corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=self.aruco_dict,
            #                                              parameters=self.parameters,
            #                                              cameraMatrix=self.camera_matrix,
            #                                              distCoeff=self.camera_distortion)
            #
            # if len(corners) > 0:
            #     if self.id_to_find in ids:
            #         self.new_val = True
            #         self.has_saw = True
            #         self.update_fps_detect()
            #         # ret = [rvec, tvec, ?]
            #         # array of rotation and position of each marker in camera frame
            #         # rvec = [[rvec_1], [rvec_2], ...]    attitude of the marker respect to camera frame
            #         # tvec = [[tvec_1], [tvec_2], ...]    position of the marker in camera frame
            #         ret = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.camera_matrix,
            #                                               self.camera_distortion)
            #
            #         # Unpack the output, get only the first
            #         rvec, tvec = ret[0][0, 0, :], ret[1][0, 0, :]
            #
            #         # Obtain the rotation matrix tag->camera
            #         R_ct = np.matrix(cv2.Rodrigues(rvec)[0])
            #         R_tc = R_ct.T
            #
            #         # Get the attitude in terms of euler 321 (Needs to be flipped first)
            #         roll_marker, pitch_marker, yaw_marker = self.rotationMatrixToEulerAngles(self.R_flip * R_tc)
            #
            #         self.obj_pixel = corners
            #         self.pre_Yaw = math.degrees(yaw_marker)
            #         if self.yaw_once:
            #             self.yaw_once = False
            #             self.Yaw = self.pre_Yaw
            #         # if abs(self.pre_Yaw-self.Yaw)<self.gap:
            #         self.Yaw = self.pre_Yaw
            #
            #         self.x = tvec[0]
            #         # scale is invese - need up is + , down is -
            #         self.y = -1 * tvec[1]
            #         self.z = tvec[2]
            #
            #     else:
            #         self.new_val = False
            #         self.yaw_once = True
            # else:
            #     self.new_val = False
            # self.running = False

    def get_coords(self):
        if self.flag_vid:
            return self.x, self.y, self.z, self.Yaw

    def is_new(self):
        if self.flag_vid:
            return self.new_val
