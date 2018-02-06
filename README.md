# ai10_keras
Re-doing ai10 w/ keras for ease of use

## Prerequisites
 * tensorflow
 * keras
 * numpy
 
No requirements.txt file because all are difficult to set up anyway, you should do it yourself. I recommend using miniconda.

## Usage
 * ai10_log2oth.py - turns "raw" game data into a usable numpy array
 * ai10_train.py - trains a keras model
 * parallel_client.py - runs ai10 against the previous (still current?) best ai5
All other files are dependencies of one of the files above