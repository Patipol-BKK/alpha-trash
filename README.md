# alphatrash

AlphaTrash is a smart trash can project that uses InceptionV1 model that has been retrained to recognize trash images for automatic trash classification. This repository contains the code for running the system on the Raspberry Pi, including the hardware controls and image recognition functions as well as the script for re-training the InceptionV1 model. A web server code has also been provided which enables AlphaTrash to upload taken images to.

### Links

- [Paper for this project](https://ieeexplore.ieee.org/document/9095775) - published in 2019 IEEE International Conference on Cybernetics and Intelligent Systems (CIS) and IEEE Conference on Robotics, Automation and Mechatronics (RAM)

- [alphatrash-dataset](https://github.com/Patipol-BKK/alphatrash-dataset) - contains 5600+ images of labeled trash from Thailand that was used in the project.

## Raspberry Pi Installation

1. Clone the repository to your Raspberry Pi:

```bash
git clone https://github.com/Patipol-BKK/alphatrash.git
```

2. Navigate to the rpi code directory:
```bash
cd demo-codes/rpi/
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Download the model files, `retrained_graph.pb` and `retrained_labels.txt`, from [releases](https://github.com/Patipol-BKK/alphatrash/releases) and put them in tf_files folder
```
demo-codes/
├── rpi/
│   ├── tf_files/
│   │   ├── retrained_graph.pb
│   │   └── retrained_labels.txt
```
These can also be retrained on you local system to fit with different labels using the scripts in `alphatrash/demo-codes/retrain/` which will be explained in the next section.

5. Run the system using the main_program.py script:

```bash
python run_system.py
```

This will start the hardware controls and image recognition functions. The board will look for signals that signify trash input then take a top-down picture of the trash that has been inserted into the compartment and saved it as image.jpeg within the directory. The operation script classify_operation.py would be called to classify using the trained model.

Alternatively, the image recognition script can be run on its own to classify a set of images. Put all the testing images into a folder and run classify.py using the following script (sample images has already been provided in`test/`):
```bash
python classify.py tf_files/retrained_labels.txt tf_files/retrained_graph.pb path/to/testing_images_folder
```

## Retraining the Model
The scripts for retraining can be found under `demo-codes/retrain/`. To retrain with our dataset, the files can be found in [alphatrash-dataset](https://github.com/Patipol-BKK/alphatrash-dataset). Copy the train folder over from the repository into `demo-codes/retrain/` then run the train.sh script:

```bash
sh train.sh
```
This should download over the base Inceptionv1 model as well as generate `tf_files/` folder which include the model files, `retrained_graph.pb` and `retrained_labels.txt`, as well as tensorboard files.
