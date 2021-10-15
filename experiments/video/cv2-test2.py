import cv2

path_to_vid = "../data/"

def play_vid(vid_filename):
    cap = cv2.VideoCapture(path_to_vid + vid_filename )
    if (cap.isOpened()== False):
        print("Error opening video stream or file")
    else:
        while(cap.isOpened()):
          # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                capname = "cap"
                cv2.namedWindow(capname, cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow(capname, frame)
                k = cv2.waitKey(33)
                if k==27:    # Esc key to stop
                    break
                elif k==-1:  # normally -1 returned,so don't print it
                    continue
            else:
                break

play_vid("070_SHARP_Titles_Flower_Titles.mp4")
