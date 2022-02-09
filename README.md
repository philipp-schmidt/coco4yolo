# coco4yolo

## Download COCO

Download annotations and images from COCO website

```bash
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
wget http://images.cocodataset.org/zips/train2017.zip
wget http://images.cocodataset.org/zips/val2017.zip

unzip annotations_trainval2017.zip
unzip train2017.zip
unzip val2017.zip
```

## Convert to YOLO format

The script will read annotations from the json file and write them into the output folder in yolo txt format. Optional filtering by category can be applied. It will then copy all relevant images to the output folder as well. Only images for which at least a single annotation remains after filtering are copied. 

Input directory and annotation directory remain unchanged at all times. Output folder will be created if it does not exist.

To only include specific COCO categories by name (e.g. car, truck, bus, motorcycle, bicycle):

```
$ python3 coco4yolo.py -a annotations/instances_train2017.json -i train2017 -o train2017_out -c car truck bus motorcycle bicycle

Parsing annotation json...
Found 118287 images, 80 categories and 860001 annotations
Selecting 5 categories: [3, 8, 6, 4, 2]
Found 75747 matching annotations after filtering
Writing annotations to output directory...
(19759/19759) train2017_out/000000515743.txt
Wrote 19759 annotation files
Copying source images to output directory...
(19759/19759) train2017/000000108303.jpg -> train2017_out/000000108303.jpg
Copied 19759 images
Place the following content into a ".names" file:
car
truck
bus
motorcycle
bicycle
```

To instead convert all COCO categories:

```
$ python3 coco4yolo.py -a annotations/instances_train2017.json -i train2017 -o train2017_out
Parsing annotation json...
Found 118287 images, 80 categories and 860001 annotations
Selecting 80 categories: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 85, 86, 87, 88, 89, 90]
Found 860001 matching annotations after filtering
Writing annotations to output directory...
(117266/117266) train2017_out/000000176470.txt
Wrote 117266 annotation files
Copying source images to output directory...
(117266/117266) train2017/000000023368.jpg -> train2017_out/000000023368.jpg
Copied 117266 images
Place the following content into a ".names" file:
person
bicycle
car
motorcycle
airplane
bus
train
truck
boat
traffic light
fire hydrant
stop sign
parking meter
bench
bird
cat
dog
horse
sheep
cow
elephant
bear
zebra
giraffe
backpack
umbrella
handbag
tie
suitcase
frisbee
skis
snowboard
sports ball
kite
baseball bat
baseball glove
skateboard
surfboard
tennis racket
bottle
wine glass
cup
fork
knife
spoon
bowl
banana
apple
sandwich
orange
broccoli
carrot
hot dog
pizza
donut
cake
chair
couch
potted plant
bed
dining table
toilet
tv
laptop
mouse
remote
keyboard
cell phone
microwave
oven
toaster
sink
refrigerator
book
clock
vase
scissors
teddy bear
hair drier
toothbrush
```
