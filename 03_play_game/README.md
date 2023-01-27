# Step 3. Play the Game!

Finally, the fun part!

First, ensure you have a DS emulator installed. I found great success with DeSmuME (download link [here](https://github.com/TASEmulators/desmume/releases)).

You'll also need the ROM file for Super Mario 64 DS. To avoid any legal issues, let's just say that a Google search should help you find this file very easily 😉

With the emulator installed and the ROM file downloaded, you should be able to open the ROM in the emulator and see the Nintendo logo, followed by a 3D model of a star instructing you to tap it! If so, this is great - you have done everything right!

Before running the script, ensure that the emulator window is visible and at the forefront of your screen (if any other window is blocking it, the Python program won't work correctly).

Using the weights from the model trained in the previous step, ``02_train_detector``, run the following command in a terminal window to start the Python program:

```bash
python run.py --yolo_object_detection_model_weights=custom/path/to/weights.pt
```

And voila - the game should now be playing itself! 🎉

See the video below for the first hour of my run using this very script:

[![](https://img.youtube.com/vi/IXq1frVs8ME/0.jpg)](https://www.youtube.com/watch?v=IXq1frVs8ME)

Enjoy!

-----

NOTE: If you don't have a Mac device, this code will, unfortunately, not work. If you have a Mac device but not [one with Apple silicon](https://support.apple.com/en-us/HT211814), change the following line in ``run.py`` from:

```python
...
    device='mps',
...
```

to

```python
...
    device='cpu',
...
```
