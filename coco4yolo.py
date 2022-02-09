import json
import os
import argparse
import shutil
from functools import reduce

parser = argparse.ArgumentParser(description='Convert coco data into yolo format and optionally filter by category')
parser.add_argument('-a', help='COCO annotation file (json)', dest='json_file', required=True)
parser.add_argument('-i', help='path to input folder with images', dest='input_path',required=True)
parser.add_argument('-o', help='path to output folder where images and labels should be placed', dest='output_path',required=True)
parser.add_argument('-c', help='list of subclasses to filter by', dest='classes_filter', nargs='+', required=False)

args = parser.parse_args()

json_file = args.json_file
input_path = args.input_path
output_path = args.output_path
classes_filter = args.classes_filter

def bbox_2_yolo(bbox, img_w, img_h):
    x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
    centerx = x + w / 2
    centery = y + h / 2
    dw = 1 / img_w
    dh = 1 / img_h
    centerx *= dw
    w *= dw
    centery *= dh
    h *= dh
    return centerx, centery, w, h

def load_images_info(images_definition):
    images_info = {}
    for image in images_definition:
        id = image['id']
        file_name = image['file_name']
        if file_name.find('\\') > -1:
            file_name = file_name[file_name.index('\\')+1:]
        w = image['width']
        h = image['height']
        images_info[id] = (file_name, w, h)
    return images_info

if __name__ == '__main__':
    # Make sure all files / paths exist
    if not os.path.exists(json_file):
        raise ValueError("json file not found")
    if not os.path.exists(input_path):
        raise ValueError("input folder does not exist")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Load json definitions
    print("Parsing annotation json...")
    json_definitions = json.load(open(json_file, 'r', encoding='utf-8'))
    print(f"Found {len(json_definitions['images'])} images, {len(json_definitions['categories'])} categories and {len(json_definitions['annotations'])} annotations")

    # Load info about images
    images_info = load_images_info(json_definitions['images'])

    # Filter categories
    category_ids = []
    if classes_filter is not None:
        for filter in classes_filter:
            category_id = None
            for category in json_definitions['categories']:
                if filter == category['name']:
                    category_id = category['id']
                    break
            if category_id is None:
                raise ValueError(f"class {filter} does not exist")
            category_ids.append(category_id)
    else:
        for category in json_definitions['categories']:
            category_ids.append(category['id'])
    print(f"Selecting {len(category_ids)} categories: {category_ids}")

    # Convert annotations
    anno_dict = {}
    for anno in json_definitions['annotations']:
        bbox = anno['bbox']
        image_id = anno['image_id']
        category_id = anno['category_id']

        if category_id in category_ids:
            image_info = images_info.get(image_id)
            image_name = image_info[0]
            img_w = image_info[1]
            img_h = image_info[2]
            yolo_box = bbox_2_yolo(bbox, img_w, img_h)

            anno_info = (image_name, category_id, yolo_box)
            anno_infos = anno_dict.get(image_id)
            if not anno_infos:
                anno_dict[image_id] = [anno_info]
            else:
                anno_infos.append(anno_info)
                anno_dict[image_id] = anno_infos
    print(f"Found {reduce(lambda count, l: count + len(l), anno_dict.values(), 0)} matching annotations after filtering")

    # Set of images to copy later
    file_names = set()
    # Print txt annotation files
    print("Writing annotations to output directory...")
    for idx, (k, v) in enumerate(anno_dict.items()):
        # Store file name for copy later
        file_name_jpg = v[0][0]
        file_names.add(file_name_jpg)

        # Write or append to annotation txt file
        file_name_txt = v[0][0].split(".")[0] + ".txt"
        print(f"({idx + 1}/{len(anno_dict)}) {os.path.join(output_path, file_name_txt)}", end='\r')
        with open(os.path.join(output_path, file_name_txt), 'w', encoding='utf-8') as f:
            for obj in v:
                category_id_coco = obj[1]
                category_id_mapped = category_ids.index(category_id_coco)
                box = ['{:.6f}'.format(x) for x in obj[2]]
                box = ' '.join(box)
                line = str(category_id_mapped) + ' ' + box
                f.write(line + '\n')
    print()
    print(f"Wrote {len(file_names)} annotation files")

    # Copy images
    print(f"Copying source images to output directory...")
    for idx, image in enumerate(file_names):
        from_path = os.path.join(input_path, image)
        to_path = os.path.join(output_path, image)
        print(f"({idx + 1}/{len(file_names)}) {from_path} -> {to_path}", end='\r')
        shutil.copyfile(from_path, to_path)
    print()
    print(f"Copied {len(file_names)} images")

    print("Place the following content into a \".names\" file:")
    if classes_filter is not None:
        for category in classes_filter:
            print(category)
    else:
        for category in json_definitions['categories']:
            print(category['name'])

