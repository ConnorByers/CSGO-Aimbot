# CSGO-Aimbot

This is my attempt of making a CSGO Aim assist tool using Python, OpenCV and Haar Cascade Classifiers.

![singlerec (online-video-cutter com) (1)](https://user-images.githubusercontent.com/53878605/134618145-16fe2ada-be52-4fe7-b184-890f1f2510ad.gif)

### How it works

A Haar Cascade Classifier is an object detection method that trains on "positive" and "negative" images and creates a model that takes an image and outputs an array of rectangles which represents where it thinks a certain type of object exists (which is defined by what you choose to the desired object in the positive images).

In `trainingdatageneration.py`, it takes screenshots of a certain part of your screen, converts them to grayscale and outputs them into either a positive or negative folder, depending on the button pressed (which can be done while playing CSGO normally, no need to tab out).

After getting screenshots and trying for a 2:1 ratio of positive to negative images, which I found to be the optimal choice online, you need to annotate the poistive files. This is easily done using opencv's cmd line tool `opencv_annotation`. More info can be found here: https://docs.opencv.org/master/dc/d88/tutorial_traincascade.html

Create empty `positives.txt` and `negatives.txt` files

After installing, run `opencv_annotation --annotations=positives.txt --images=positive/` and follow instructions given.

Then, use `negfilegeneration.py` which will fill up your negatives.txt file with a list of all negative pictures.

Note: You will need to replace all the backslashes with forward slashes in your positive and negative folders.

Run `opencv_createsamples -info positives.txt -w 24 -h 24 -num {NUMBER HIGHER THAN # objects in postiives) -vec positives.vec`
The -w and -h are the mininum length of an object. See http://manpages.ubuntu.com/manpages/bionic/man1/opencv_createsamples.1.html for more info.

Run `opencv_traincascade -data cascade/ -v positives.vec -bg neg.txt -w <same as above> -h <same as above> -numPos <number below # objects> -numNeg <number of negatives, aiming for 2:1 ratio) -numStages <play around with this>`

