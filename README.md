# CSGO-Aimbot

This is my attempt of making a CSGO Aim assist tool using Python, OpenCV and Haar Cascade Classifiers. This aimbot only works well against Counter Terrorists (as their color contrasts better against backgrounds than Terrorists).

You play normally as you would in CS:GO, but when you want to snap to a player, click the key that you set in the `AIMBOT_CHARACTER` constant (default is `l`).

To quit the aimbot, press the QUIT_KEY key (default is `k`).

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

To attempt to filter away incorrectly identified objects from the model (as shown below):

![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/53878605/134783825-81e92074-bfe0-49f1-bc6d-3d54a31bb2a3.gif)


- Only consider objects within a certain region in the screen (the sky, ground, gun often gets incorrectly chosen)
- Check if the middle of the object is a counter terrorist color by calculating its hsp value (which is a measure of brightness) and checking for other patterns I found through testing the pixel colors of CTs

After Filtering, the model boxes look like this:

![ezgif com-gif-maker](https://user-images.githubusercontent.com/53878605/134783666-fcea0f98-e4c3-416a-ba7e-914071605190.gif)

### Choosing Enemy to snap to
- The closest rectangle to the crosshair is what I decided to snap to. That's due to the fact if a player has good crosshair placement such that the crosshair is near possible CT's, it is more probable that it will snap to a CT and not a false positive.

With only selecting the closest rectangle, the below is what's considered:

![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/53878605/134783869-7ea67536-7f42-459e-bc26-c48f3eae4a94.gif)

### CSGO Settings

I have my sensitivity set to 2.5. If you want a different sensitivity, you might need to fiddle with the mouse move multiplier on x and y.

Make sure `Raw Input` and `Mouse acceleration` is set to off.

Its a good idea to bind decal clearing to movement so the aimbot doesn't get confused by blood splatter.

To get better results, change your gun position to be lower and more to the right so it doens't take up as much of the screen.


