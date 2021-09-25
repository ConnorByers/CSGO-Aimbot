# CSGO-Aimbot

This is my attempt of making a CSGO Aim assist tool using Python, OpenCV and Haar Cascade Classifiers. This aimbot only works well against Counter Terrorists (as their color constrasts better against backgrounds than Terrorists).

![singlerec (online-video-cutter com) (1)](https://user-images.githubusercontent.com/53878605/134618145-16fe2ada-be52-4fe7-b184-890f1f2510ad.gif)

### How it works

A Haar Cascade Classifier is an object detection method that trains on "positive" and "negative" images and creates a model that takes an image and outputs an array of rectangles which represents where it thinks a certain type of object exists (which is defined by what you choose to the desired object in the positive images).

In `trainingdatageneration.py`, it takes screenshots of a certain part of your screen, converts them to grayscale and outputs them into either a positive or negative folder, depending on the button pressed (which can be done while playing CSGO normally, no need to tab out).

After getting screenshots and trying for a 2:1 ratio of positive to negative images, which I found to be the optimal choice online, you need to annotate the positive files. This is easily done using opencv's cmd line tool `opencv_annotation`. More info can be found here: https://docs.opencv.org/master/dc/d88/tutorial_traincascade.html

Create empty `positives.txt` and `negatives.txt` files

After installing, run `opencv_annotation --annotations=positives.txt --images=positive/` and follow instructions given.

Then, use `negfilegeneration.py` which will fill up your negatives.txt file with a list of all negative pictures.

Note: You will need to replace all the backslashes with forward slashes in your positive and negative folders.

Run `opencv_createsamples -info positives.txt -w 24 -h 24 -num {NUMBER HIGHER THAN # objects in postiives) -vec positives.vec`
The -w and -h are the mininum length of an object. See http://manpages.ubuntu.com/manpages/bionic/man1/opencv_createsamples.1.html for more info.

Run `opencv_traincascade -data cascade/ -v positives.vec -bg neg.txt -w <same as above> -h <same as above> -numPos <number below # objects> -numNeg <number of negatives, aiming for 2:1 ratio) -numStages <play around with this>`

### Filtering

To attempt to filter away incorrectly identified objects from the model, it

- Only considers objects within a certain region in the screen (the sky, ground, gun often gets incorrectly chosen)
- Checks if the middle of the object is a counter terrorist color by gettings its hsp value (which is a measure of brightness) and other patterns I found through checking the pixel colors

### Choosing Enemy to snap to
- For simplicity sake, the closest rectangle was chosen
