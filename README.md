Webcam-Face-Detect
==================

This is a quick and hacky script for a small art project. The aim was to count the number of people looking at a piece of art. We decided to proxy this with this face detection algorithm and a webcam positioned behind the artwork. The script simply outputs a counter of the number of faces it has detected so far. The accuracy is not great. If there are bright light sources in the field of view they might be detected as faces. In addition, sometimes the tracking of a face fails such that it is detected multiple times. Nevertheless, the script was good enough for the job :-)


Quick start
-----------
Run the program like this:

python webcam.py haarcascade_frontalface_default.xml

If you want to understand how the code works,  see here: https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/


Update: Now supports OpenCV3. This change has been made by furetosan ( https://github.com/furetosan) and tested on Linux.

To run the OpenCV3 version, run webcam_cv3.py.

