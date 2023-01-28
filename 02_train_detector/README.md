# Step 2. Train the Object Detection Model

It's time to train a model!

First, we need to set up the [``data.yaml``](data.yaml) file. Replace the ``XX`` in the training and validation data paths with the absolute path to those directories containing both the images and YOLO-compatible annotation files.

With this, navigate to the [``yolov5``](https://github.com/ultralytics/yolov5/tree/064365d8683fd002e9ad789c1e91fa3d021b44f0) directory and use the following one-liner to kick off a training run:

```bash
python train.py --data ../data.yaml --epochs 100 --weights '' --cfg yolov5s.yaml --batch-size -1
```

If you want to skip this step and instead use the model weights from my training run, you can download them [here](https://thisboredapedoesnotexist.s3.amazonaws.com/super-mario-64-ds-autoplayer/best.pt).

Once you have a trained model, make note of where the weights are stored, as you'll need this for the next step, [``03_play_game``](../03_play_game)!
