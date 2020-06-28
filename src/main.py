from input_feeder import InputFeeder
from face_detection import FaceDetector
from facial_landmarks_detection import EyeDetector
from head_pose_estimation import HeadPoseEstimator
from gaze_estimation import GazeEstimator
from mouse_controller import MouseController
import helpers
import cv2


source = '../bin/demo.mp4'
#source = 'cam'
feed = InputFeeder(source)
faceDetector = FaceDetector(device='CPU', extensions=None)
eyeDetector = EyeDetector(device='CPU', extensions=None)
headPoseEstimator = HeadPoseEstimator(device='CPU', extensions=None)
gazeEstimator = GazeEstimator(device='CPU', extensions=None)
mouseController = MouseController(precision='medium', speed='medium')

for frame in feed.next_frame():
    #face = faceDetector.extract(frame, confidence=0.5)
    face, face_box = faceDetector.extract(frame, confidence=0.5)
    left_eye, right_eye = eyeDetector.extract(face)
    head_pose_angles = headPoseEstimator.estimate(face)
    gx,gy,_ = gazeEstimator.estimate(left_eye, right_eye, head_pose_angles)
    #print(gaze_vector)
    #gx,gy,gz = gazeEstimator.normalize(gaze_vector)
    #gx,gy,gz = gaze_vector

    #if feed.input_type == 'cam':
    #    if head_pose_angles is not None:
    #        
    #        g_mag = math.sqrt(gx*gx+gy*gy+gz*gz) + 1e-4
    #
    #        # Yaw compensation
    #        # (we usually tilt the head)
    #        yaw_rad = head_pose_angles[0]*math.pi/180
    #        gx2 = gx*math.cos(yaw_rad) + g_mag*math.sin(math.acos(gx/g_mag))*math.sin(yaw_rad)
    #        #print(head_pose_angles[0], gx, gx2)
    #        gx = gx2
    #
    #        # pitch compensation                                    
    #        pitch_rad = head_pose_angles[1]*math.pi/180
    #        #gy2 = math.cos(pitch_rad)*gy - g_mag*math.sin(pitch_rad)*math.sin(math.acos(gy/g_mag))
    #        gy2 = gy*math.cos(pitch_rad) + g_mag*math.sin(math.acos(gy/g_mag))*math.sin(pitch_rad)
    #        print(head_pose_angles[1], gy, gy2)
    #        gy = gy2



    #face = draw_vector((gx,gy,gz), face)
    #print('norm:', gazeEstimator.normalize(gaze_vector))    
    #mouseController.move(gaze_vector[0], gaze_vector[1])
    mouseController.move(gx,gy)

    #cv2.waitKey(1)
    #if face is not None and face.size>1:
        #cv2.imshow('face', face)
    #    cv2.imshow('frame', frame)
    #draw_vector(gaze_vector, face)
    output_frame = helpers.draw_gaze_vector(frame, face_box, gx, gy)

    cv2.imshow(source, output_frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

feed.close()
