
import numpy as np
from urllib.request import urlopen
import cv2

def load_image(url):
    req = urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)  # 'Load it as it is'
    return image

def process_line(line):
    print(line)
    separator = '\t'
    url_index = 1

    splitted_line = line.split(separator)
    return splitted_line[url_index]


def main():
    filepath = r'C:\Users\m\Desktop\Pose Estimation\mlserverengine\datasets\Yoga-82\yoga_dataset_links\Akarna_Dhanurasana.txt'
    lines = []
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line = fp.readline()
            lines.append(line)

    url = process_line(lines[2])
    image = load_image(url)
    print(image)
    cv2.imshow("test", image)


if __name__ == '__main__':
    main()