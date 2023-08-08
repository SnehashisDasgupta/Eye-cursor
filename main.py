import cv2
import mediapipe as mp
import pyautogui

# capture the first [0-index] device for accessing camera 
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
screen_w, screen_h = pyautogui.size()

# it will capture the frame contineously
while True:
   _, frame = cam.read()
   frame = cv2.flip(frame, 1) # flip the frame vertically
   # detect face in the screen 
   rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   output = face_mesh.process(rgb_frame)
   landmark_points = output.multi_face_landmarks
   # print(landmark_points) 
   frame_h, frame_w, _ = frame.shape # get the height & width of the frame

   if landmark_points:
      landmarks = landmark_points[0].landmark #detect only one face
      # [474, 478] = detects only one eye, not the whole face
      for id, landmark in enumerate(landmarks[474: 478]):
         x = int(landmark.x * frame_w)
         y = int(landmark.y * frame_h)
         cv2.circle(frame, (x, y), 3, (0, 255, 0)) # .circle(frame, centre of circle, size of circle, color)
         # print(x, y)

         if id == 1:
            screen_x = int(landmark.x * screen_w)
            screen_y = int(landmark.y * screen_h)
            pyautogui.moveTo(screen_x, screen_y)

      left = [landmarks[145], landmarks[159]]
      for landmark in left:
         x = int(landmark.x * frame_w)
         y = int(landmark.y * frame_h)
         cv2.circle(frame, (x, y), 3, (0, 255, 255)) # .circle(frame, centre of circle, size of circle, color)

      # if upper and lower lashes of left eye touches each other then it is clicked
      if (left[0].y - left[1].y < 0.004):
         # print('click')
         pyautogui.click()
         pyautogui.sleep(1)

   cv2.imshow('Eye Controller', frame) #show the image
   cv2.waitKey(1)