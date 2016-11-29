import cv2
import sys
import curses
import cPickle as pickle
import os

from time import sleep

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
ant_faces = []

# How far is a head allowed to have wandered (and/or shrunk/grown) to still
# count as the same head
eps = 50
# How often has a head to be detected, before counting it.
debounce = 10

# Message shown in front of the count
message = "Blicke gefangen: "

# Determines whether the video stream is shown or not.
debug = False

# Set up the counter variable
path = "./counter"
gcount = 0
if os.path.exists(path):
    with open(path) as pickle_handle:
        gcount = pickle.load(pickle_handle)

# ncurses set up
myscreen = curses.initscr()
myscreen.border(0)
y, x = myscreen.getmaxyx()
posr = y // 2
posc = (x - len(message + str(gcount))) // 2
myscreen.addstr(posr, posc, message)
myscreen.nodelay(1)
myscreen.refresh()


def get_faces(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )


def show_stream(frame, faces):
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)


while True:

    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    faces = get_faces(frame)

    if debug:
        show_stream(frame, faces)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    nf = []

    for (x, y, w, h) in faces:
        nf.append({'x': x, 'y': y, 'w': w, 'h': h, 'count': 1, 'found': False})
        for f in ant_faces:
            if (x - f['x'])**2 + (y - f['y'])**2 + (w - f['w'])**2 + (h - f['h'])**2 < eps**2 and not f['found']:
                nf[-1]['count'] = f['count'] + 1
                f['found'] = True

                if nf[-1]['count'] == debounce:
                    gcount += 1
                    with open(path, 'w') as pickle_handle:
                        pickle.dump(gcount, pickle_handle)

    ant_faces = nf

    myscreen.addstr(posr, posc + len(message), str(gcount))
    myscreen.refresh()

    if myscreen.getch() == ord('q'):
        break


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
myscreen.endwin()