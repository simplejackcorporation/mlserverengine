import os
import sys
import argparse
import ast
import cv2
import time
import torch
from vidgear.gears import CamGear
import numpy as np


from SimpleHRNet import SimpleHRNet
from misc.visualization import draw_points, draw_skeleton, draw_points_and_skeleton, joints_dict, check_video_rotation
from misc.utils import find_person_id_associations

def main(filename,
         hrnet_m,
         hrnet_c,
         hrnet_j,
         hrnet_weights,
         hrnet_joints_set,
         image_resolution,
         max_batch_size,
         device):


    if device is not None:
        device = torch.device(device)
    else:
        if torch.cuda.is_available():
            torch.backends.cudnn.deterministic = True
            device = torch.device('cuda')
        else:
            device = torch.device('cpu')

    # print(device)

    image_resolution = ast.literal_eval(image_resolution)
    has_display = 'DISPLAY' in os.environ.keys() or sys.platform == 'win32'
    video_writer = None

    # filename = os.path.join(os.getcwd(), filename)
    # print(filename)
    image = cv2.imread(filename)

    model = SimpleHRNet(
        hrnet_c,
        hrnet_j,
        hrnet_weights,
        model_name=hrnet_m,
        resolution=image_resolution,
        multiperson=False,
        return_bounding_boxes=False,
        max_batch_size=max_batch_size,
        device=device
    )

    pts = model.predict(image)

    person_ids = np.arange(len(pts), dtype=np.int32)

    for i, (pt, pid) in enumerate(zip(pts, person_ids)):
        frame = draw_points_and_skeleton(image, pt, joints_dict()[hrnet_joints_set]['skeleton'],
                                         person_index=pid,
                                         points_color_palette='gist_rainbow',
                                         skeleton_color_palette='jet',
                                         points_palette_samples=10)
    if has_display:
        cv2.imshow('frame.png', frame)
        cv2.waitKey(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", "-f", help="open the specified video (overrides the --camera_id option)",
                        type=str, default=None)
    parser.add_argument("--hrnet_m", "-m", help="network model - 'HRNet' or 'PoseResNet'", type=str, default='HRNet')
    parser.add_argument("--hrnet_c", "-c", help="hrnet parameters - number of channels (if model is HRNet), "
                                                "resnet size (if model is PoseResNet)", type=int, default=48)
    parser.add_argument("--hrnet_j", "-j", help="hrnet parameters - number of joints", type=int, default=17)
    parser.add_argument("--hrnet_weights", "-w", help="hrnet parameters - path to the pretrained weights",
                        type=str, default="./weights/pose_hrnet_w48_384x288.pth")
    parser.add_argument("--hrnet_joints_set",
                        help="use the specified set of joints ('coco' and 'mpii' are currently supported)",
                        type=str, default="coco")
    parser.add_argument("--image_resolution", "-r", help="image resolution", type=str, default='(384, 288)')
    parser.add_argument("--max_batch_size", help="maximum batch size used for inference", type=int, default=16)
    parser.add_argument("--device", help="device to be used (default: cuda, if available)."
                                         "Set to `cuda` to use all available GPUs (default); "
                                         "set to `cuda:IDS` to use one or more specific GPUs "
                                         "(e.g. `cuda:0` `cuda:1,2`); "
                                         "set to `cpu` to run on cpu.", type=str, default=None)
    args = parser.parse_args()
    main(**args.__dict__)
    #
    # temp = np.array([cv2.imread(r"C:\Users\m\Desktop\Pose Estimation\simple-HRNet\scripts\leo.jpeg")])
    # print(temp.shape)
    # img = torch.from_numpy(temp).permute((0, 3, 1, 2)).contiguous()
    # print(img.shape)
    #
    # transform = transforms.Compose([
    #     transforms.ToTensor(),
    #     # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    # ])
    # temp2 = transform(temp)
    # print(temp2.shape)
    # print(img.float().div(255)[0, :, :,])
    # print(temp2[0, :, :,])
