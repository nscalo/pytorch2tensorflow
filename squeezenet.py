import torch
import torchvision

#dummy_input = torch.randn(10, 3, 224, 224, device='cpu')
img_size = (224, 224)
dummy_input = torch.zeros((1, 3) + img_size)
model = torchvision.models.squeezenet1_0(pretrained=True).cpu()

input_names = ["actual_input_1"] + ["learned_%d" % i for i in range(16) ]
output_names = ["output1"]

print(input_names)
print(output_names)

torch.onnx.export(model, dummy_input, "./weights/squeezenet.onnx", verbose=True, input_names=input_names, output_names=output_names,opset_version=10)

print('---1---')

import onnx
model = onnx.load("./weights/squeezenet.onnx")
onnx.checker.check_model(model)
onnx.helper.printable_graph(model.graph)


print('---2---')
import onnxruntime as ort
import numpy as np
ort_session = ort.InferenceSession('./weights/squeezenet.onnx')

outputs = ort_session.run(None, {"actual_input_1":np.zeros((1,3)+(224,224)).astype(np.float32)})

print(outputs[0].shape)
print(outputs[0])


