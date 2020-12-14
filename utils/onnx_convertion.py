import sys
import os

print(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'hrnet'))
sys.path.append(os.path.join(os.getcwd(), 'hrnet', 'models'))

print(sys.path)

print(os.getcwd())
if not os.getcwd().endswith("hrnet"):
    os.chdir(os.getcwd() + "/hrnet")
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())
    print(os.getcwd())
    print(sys.path)
from models.hrnet import HRNet
model = HRNet(c=48, nof_joints=17)
if os.getcwd().endswith("hrnet"):
    os.chdir("".join(os.getcwd()[:-len("/hrnet")]))
print(os.getcwd())


import onnx
import onnxruntime

from prettytable import PrettyTable
import torch
import json
import cv2
import numpy as np

ONNX_PATH = "./my_model.onnx"



def count_parameters(model):
    table = PrettyTable(["Modules", "Parameters"])
    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad: continue
        param = parameter.numel()
        table.add_row([name, param])
        total_params+=param
    print(table)
    print(f"Total Trainable Params: {total_params}")
    return total_params

def convertToONNX():
    checkpoint_path = "./weights/pose_hrnet_w48_384x288.pth"

    model = HRNet(c=48, nof_joints=17)
    checkpoint = torch.load(checkpoint_path, map_location=torch.device("cpu"))
    model.load_state_dict(checkpoint)
    count_parameters(model)

    x = torch.randn(1, 3, 384, 288, requires_grad=True)

    torch.onnx.export(
        model=model,
        args=x,
        f=ONNX_PATH,  # where should it be saved
        verbose=False,
        export_params=True,
        do_constant_folding=False,  # fold constant values for optimization
        # do_constant_folding=True,   # fold constant values for optimization
        input_names=['input'],
        output_names=['output']
    )

    onnx_model = onnx.load(ONNX_PATH)
    onnx.checker.check_model(onnx_model)



def inferenceONNXModel(img_path=r"C:\Users\m\Desktop\Pose Estimation\simple-HRNet\scripts\leo.jpeg"):
    img = cv2.imread(r"C:\Users\m\Desktop\Pose Estimation\simple-HRNet\scripts\leo.jpeg")

    data = json.dumps({'data': img.tolist()})
    data = np.array(json.loads(data)['data']).astype('float32')

    print("\n\n\n\n\n\n", data.shape)

    session = onnxruntime.InferenceSession(ONNX_PATH, None)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    print(input_name)
    print(output_name)
    result = session.run([output_name], {input_name: data})
    prediction = int(np.argmax(np.array(result).squeeze(), axis=0))
    print(prediction)


if __name__ == '__main__':
    # convertToONNX()
    convertToONNX()
