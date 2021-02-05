import sys
import os

sys.path.insert(1, os.getcwd())
sys.path.insert(1, r"C:\Users\m\Desktop\Pose Estimation\simple-HRNet")
sys.path.insert(1, r"C:\Users\m\Downloads")

import json
import cv2
import numpy as np
from urllib.request import urlopen

from hrnet.misc.visualization import showAnns

import time

def read_json(path, save_path):
    counter = 0
    base_path = r'C:\Users\m\Desktop\Pose Estimation\mlserverengine'
    total_path = os.path.join(base_path, path)

    total_exec_time = 0
    total_memory = 0 #
    with open(total_path) as json_file:
        data = json.load(json_file)
        annotations = data["annotations"]
        images = data["images"]
        test_count = 5000
        images = images[0: test_count]
        print("images len", len(images))
        print("annotations len", len(annotations))

        for index, img in enumerate(images):
            print(index)
            start_iter_time = time.time()

            keypoints_arr = []
            for index, ann in enumerate(annotations):
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
            img_downl_start_time = time.time()
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

            print("img time for downl", time.time() - img_downl_start_time)

            img_total_size = 0
            print('len(image.shape)', len(image.shape))

            if len(image.shape) == 3:
                img_total_size = image.shape[0] * image.shape[1] * image.shape[2]
            else :
                img_total_size = image.shape[0] * image.shape[1]

            img_mem = float(img_total_size) / 1024000

            print("img_mem mg", img_mem)

            # img = showAnns(image, keypoints_arr)
            execution_time = time.time() - start_iter_time
            total_exec_time += execution_time
            total_memory += img_mem
            print("execution_time ", execution_time)
            # cv2.imshow("vova", img)
            # cv2.waitKey()
            # break

        print(counter)
        print("\n \n Total_exec_time: ", total_exec_time)
        print("\n \n Total_memory: ", total_memory)

        print("\n \n mean total_exec_time: ", total_exec_time / test_count)
        print("\n \n meain total_memory: ", total_memory/ test_count)


if __name__ == '__main__':
    path = "datasets\person_keypoints_train2017.json"
    save_path = r"C:\Users\m\Desktop\Pose Estimation\Dataset"
    read_json(path, save_path)