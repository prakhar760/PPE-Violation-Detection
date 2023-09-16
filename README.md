# PPE-Violation-Detection

 An Object Detection Project for detecting PPE violations at construction sites in which the user gets an interactive UI to upload video or live inference. A bounding box is created on people labelling them with "no helmet", "no jacket", "safe", "unsafe" and sends an alert email. 

## Stages

- Images collected by students wearing PPE kit for construction workers in various circumstances.

- Images annotated using Roboflow, an online annotation tool mainly for object detection and segmentation. 

- Yolov7 pre-trained model weights used for transfer learning to train the PPE Violation Detection model. data.pt were the weights obtained out of custom training.
