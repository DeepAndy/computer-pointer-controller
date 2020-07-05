# Computer Pointer Controller

Human vision performs a variety of tasks to interpret the surrounding environment. Many of them have been researched and automated by deep learning. This project combines several such models from the Intel Distribution of OpenVINO Toolkit to control a mouse pointer using eye gaze. The first step is to identify faces and extract a face from an input video stream captured from a webcam or a video file. Then we extract facial landmarks and find the orientation of the face by means of a head pose estimation model. Knowing the head pose and facial landmarks, we can find the orientation of the eye gaze using a gaze estimation model. Finally, the mouse pointer is moved in the direction of the eye gaze. 


## Project Set Up and Installation

### Install the Intel Distribution of OpenVINO Toolkit

The project requires Intel OpenVINO 2020.1 or newer. Older versions should work too, but it's not guaranteed.
Refer to [this](https://docs.openvinotoolkit.org/2020.1/_docs_install_guides_installing_openvino_linux.html#install-openvino) manual for a step-by-step installation guide.


### Install Python libraries

Creating an isolated environment for the project is recommended. It can be done by the following command:
```
conda create -n computer-pointer-controller python=3.6
``` 

Now activate the environment:
```
conda activate computer-pointer-controller
```

To install necessary Python packages run:
```
pip install -r requirements.txt
```

### Download pre-trained models from OpenVINO Model Zoo

The project requires the following models:
* face-detection-retail-0005
* facial-landmarks-35-adas-0002
* head-pose-estimation-adas-0001
* gaze-estimation-adas-0002

Model files are expected to reside in <project-folder>/models.

For convenience there is a download_models.sh script in the project root folder which automatically installs the OpenVINO Model Downloader requirements and downloads all the necessary models. Assuming that OpenVINO is installed to the default location, simply run:
```
./download_models.sh
```

In case OpenVINO is installed to a different path, the script should be provided with a Model Downloader directory as an argument:
```
./download_models.sh /opt/intel/openvino/deployment_tools/tools/model_downloader
```

Alternatively, these models can be downloaded via Model Downloader (<OPENVINO_INSTALL_DIR>/deployment_tools/open_model_zoo/tools/downloader) one-by-one:
```
./downloader.py --name face-detection-retail-0005 --precisions FP32,FP16,FP32-INT8 --output_dir <project-folder>/models
./downloader.py --name facial-landmarks-35-adas-0002 --precisions FP32,FP16,FP32-INT8 --output_dir <project-folder>/models
./downloader.py --name head-pose-estimation-adas-0001 --precisions FP32,FP16,FP32-INT8 --output_dir <project-folder>/models
./downloader.py --name gaze-estimation-adas-0002 --precisions FP32,FP16,FP32-INT8 --output_dir <project-folder>/models
```

Consult [this](https://docs.openvinotoolkit.org/2020.1/_tools_downloader_README.html) page for additional details about OpenVINO Model Downloader usage.

### Project directory structure

The project tree should finally look like this:
```
├── bin
│   └── demo.mp4
├── download_models.sh
├── models
│   └── intel
│       ├── face-detection-retail-0005
│       ├── facial-landmarks-35-adas-0002
│       ├── gaze-estimation-adas-0002
│       └── head-pose-estimation-adas-0001
├── README.md
├── requirements.txt
└── src
    ├── face_detection.py
    ├── facial_landmarks_detection.py
    ├── gaze_estimation.py
    ├── generic_model.py
    ├── head_pose_estimation.py
    ├── helpers.py
    ├── input_feeder.py
    ├── main.py
    └── mouse_controller.py
```    



## Demo

Before launching the app make sure to activate the project's virtual environment (see "Project Set Up and Installation" section for guidelines on creating the virtual environment). Also you need to have OpenVINO initialized. Assuming the default installation path, it can be done by this command:
```
source /opt/intel/openvino/bin/setupvars.sh -pyver 3.6
```

The main script is located in the _src_ folder. In order to run the application you need to provide the input file:
```
python main.py --input ../bin/demo.mp4
```

Or you can use a webcam stream:
```
python main.py --input cam
```

Other command line arguments are optional. See the "Documentation" section for details.


## Documentation
*TODO:* Include any documentation that users might need to better understand your project code. For instance, this is a good place to explain the command line arguments that your project supports.

## Benchmarks
*TODO:* Include the benchmark results of running your model on multiple hardwares and multiple model precisions. Your benchmarks can include: model loading time, input/output processing time, model inference time etc.

This project can use models in three precisions: FP32, FP16, and FP32-INT8. The only harware available to me is Core i7 4712HQ (4th gen, not officially supported by OpenVINO), so the benchmark includes only CPU results. The table below shows total processing time (in seconds) for different combinations of model precisions and levels of concurrency.

|                 | FP32  | FP16  | FP32-INT8 |
|-----------------|-------|-------|-----------|
| Synchronous (0) | 15.87 | 17.43 | 25.49     |
| Asynchronous (1)| 12.54 | 12.59 | 17.76     |
| Asynchronous (2)| 12.67 | 15.28 | 18.54     |
| Asynchronous (4)| 12.5  | 12.19 | 17.57     |


These results have been obtained in the silent mode (without video output and mouse control) using the "demo.mp4" input file. Each test was run 3 times, the measured time was then averaged. Model loading time for FP32 and FP16 precisions was around 1 second. For FP32-INT8 it was around 4.5 seconds.


## Results
*TODO:* Discuss the benchmark results and explain why you are getting the results you are getting. For instance, explain why there is difference in inference time for FP32, FP16 and INT8 models.

These benchmark results suggest that models in FP32 precision work faster on my hardware. This is probably because CPU is optimized for FP32 precision, lower precision models may incur computational overhead connected with internal upscaling to FP32. However, on different hardware lower precision models may show better performance due to reduced memory usage and faster data transfer. 

Another point to notice is asynchronous inference, which improves performance regardless of the precision used. That said, increasing the number of parallel requests does not seem to speed up things further. This is again hardware-dependent: Xeon processors and newer Core processors are likely to be capable of doing more requests simultaneously. 

As far as accuracy is concerned, no visible differences were noticed between FP32, FP16, and FP32-INT8 models.

