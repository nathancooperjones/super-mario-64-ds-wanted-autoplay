# Step 1. Generating Training Data

<p align="center">
  <img src="https://user-images.githubusercontent.com/31417712/215226689-85b2addd-ef27-445c-aedd-3dbf6c28e516.png">
</p>

This directory contains the notebook to generate the training data necessary for the object detection model, ``generate-data.ipynb``.

The parameters in this notebook are the exact ones I used to generate the dataset I used for my model training run, but due to the random nature of how some of the parameters are chosen, your run might not _exactly_ be the same as mine, but it should be close enough that it won't make too much of a difference when modeling.

The output of the notebook will be a directory called ``data/`` in this directory's parent directory (``..``). It will contain COCO-compatible annotations in a single ``annotations.json`` file as well as each of the generated images in a directory ``images/``.

While these are perfectly valid COCO annotations, the YOLOv5 model needs the annotations to be in... well... YOLO format. Luckily, the codebase ``COCO2YOLO`` helps do the conversion really easily.

After executing the notebook, navigate your terminal to this directory and execute the following:

```bash
pwd  # should be this directory: */01_generate_data

cd COCO2YOLO
python COCO2YOLO.py -j ../../data/annotations.json -o ../../
```

This should create YOLO annotation text files in the ``images`` directory (I know, not super intuitive, but I got a bit lazy here and felt like this was fine enough). Now, for each image in the directory, a corresponding text file with the same name should be present. If so, this is good - we can continue onwards! If not, please feel free to open up a GitHub Issue and we can troubleshoot it together.

We are _almost_ done now, I swear. The last thing we should do is create training and validation datasets. This can be any size you want - for me, I just used the last 500 images to be the validation dataset and the rest to be the training dataset. However you decide to do it, make sure every image in a folder has its corresponding text annotation file. By the end of all of this, your ``data/`` directory should look like this:

```
data
└── images
    ├── image_00001.png
    ├── image_00001.png
    ├── image_00002.png
    ├── image_00002.txt
    └── ...
└── train
    ├── image_00001.png
    ├── image_00001.png
    ├── image_00002.png
    ├── image_00002.txt
    ├── ...
    ├── image_14500.png
    └── image_14500.txt
└── val
    ├── image_14501.png
    ├── image_14501.png
    ├── image_14502.png
    ├── image_14502.txt
    ├── ...
    ├── image_15000.png
    └── image_15000.txt
└── annotations.json
```

If you have everything in order, congratulations - the hardest step is done! You can now continue on to the next step: ``02_train_detector``.
