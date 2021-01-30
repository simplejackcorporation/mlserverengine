import sys
import os

sys.path.insert(1, os.getcwd())
sys.path.insert(1, r"C:\Users\m\Desktop\Pose Estimation\simple-HRNet")
sys.path.insert(1, r"C:\Users\m\Downloads")

import json
import cv2
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from urllib.request import urlopen

from misc.visualization import showAnns

def read_json(path, save_path):
    counter = 0
    with open(path) as json_file:
        data = json.load(json_file)
        annotations = data["annotations"]
        images = data["images"]

        for index, img in enumerate(images):
            keypoints_arr = []
            for ann in annotations:
                if "image_id" not in ann:
                    continue

                if img["id"] == ann["image_id"]:
                    kp = np.array(ann['keypoints'])
                    kp = kp.reshape((int(len(kp) / 3), 3))
                    non_zero_items = [(item[1], item[0]) for item in kp if item[1] > 0 and item[0] > 0]

                    if len(non_zero_items) < 9:
                        continue
                    keypoints_arr.append(kp)

            if len(keypoints_arr) == 0:
                continue
            counter += 1

            coco_url = img["coco_url"]
            req = urlopen(coco_url)
            # # print(ann)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            image = cv2.imdecode(arr, -1)  # 'Load it as it is'
            # img_save_path = os.path.join(save_path, "temp.jpeg")
            # print("img_save_path" , img_save_path)
            # cv2.imwrite(img_save_path, image)
            # # break
            # # print(image.shape)
            #
            img = showAnns(image, keypoints_arr)
            cv2.imshow("vova", img)
            cv2.waitKey()
            # break

        print(counter)


if __name__ == '__main__':
    path = "datasets/person_keypoints_train2017.json"
    save_path = r"C:\Users\m\Desktop\Pose Estimation\Dataset"
    read_json(path, save_path)