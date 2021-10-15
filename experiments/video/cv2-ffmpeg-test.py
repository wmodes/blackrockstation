import cv2
import numpy as np
#ffpyplayer for playing audio
from ffpyplayer.player import MediaPlayer
from screeninfo import get_monitors

video_path="../data/070_SHARP_Titles_Flower_Titles.mp4"

monitor_factor = 1

def playVideo(video_path):
    cap = cv2.VideoCapture(video_path)
    monitor = get_monitors()[0]
    # print(str(monitor))
    # print(type(monitor))
    screen_width = monitor.width * monitor_factor
    screen_height = monitor.height * monitor_factor
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
    else:
        player = MediaPlayer(video_path)
        while(cap.isOpened()):
            grabbed, frame = cap.read()
            audio_frame, val = player.get_frame()
            if not grabbed:
                print("End of video")
                break
            if cv2.waitKey(28) & 0xFF == ord("q"):
                break
            winname = "Video"
            cv2.namedWindow(winname, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            # resized_frame = cv2.resize(frame, (2880, 1800))
            cv2.imshow(winname, frame)
            if val != 'eof' and audio_frame is not None:
                #audio
                img, t = audio_frame
    cap.release()
    cv2.destroyAllWindows()

playVideo(video_path)
