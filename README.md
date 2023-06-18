[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4722445.svg)](https://doi.org/10.5281/zenodo.4722445)

# **EEG_blink_detector**
An Algorithm using CNN (Convolutional Neural Network) for detecting blink pattern in EEG signal. The Network training code, data cleaning and preparation used for this study are available in this repository and are part of the paper [EEG Multipurpose Eye Blink Detector using convolutional neural network](https://rsdjournal.org/index.php/rsd/article/view/22712). The paper is also available in the [arxiv repository](https://arxiv.org/abs/2107.14235).

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
    <li><a href="#abstract">Abstract</a></li>
    <li><a href="#code">Code</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>
  
## **Abstract**

The electrical signal emitted by the eyes movement produces a very strong artifact on EEG signal due to its close proximity to the sensors and abundance of occurrence. In the context of detecting eye blink artifacts in EEG waveforms for further removal and signal purification, multiple strategies where proposed in the literature. Most commonly applied methods require the use of a large number of electrodes, complex equipment for sampling and processing data. The goal of this work is to create a reliable and user independent algorithm for detecting and removing eye blink in EEG signals using CNN (convolutional neural network). For training and validation, three sets of public EEG data were used. All three sets contain samples obtained while the recruited subjects performed assigned tasks that included blink voluntarily in specific moments, watch a video and read an article. The model used in this study was able to have an embracing understanding of all the features that distinguish a trivial EEG signal from a signal contaminated with eye blink artifacts without being overfitted by specific features that only occurred in the situations when the signals were registered.

## **Code**

The datasets used in this project are stored in the data folder. The code used to read and treat the raw data is in the preprocessing_functions file. The following steps performed in the datasets and described in the paper are present in the processing_data notebook along with a ipywidget to facilitate data visualization. The CNN models, tuner and results analysis are in the CNN_an_results notebook. 

## **Installation**

1. Install and/or update <a href="https://www.anaconda.com/products/individual">anaconda</a>

2. Clone this <a href="https://github.com/Atzingen/EEG_blink_detector">repository</a>

```sh
git clone https://github.com/Atzingen/EEG_blink_detector.git
```

3. Create the enviroment using the requirements.txt file

  ```sh
  conda create --name eeg --file requirements.txt

  conda activate eeg
  ```

4. Open the notebooks to test the dataset
 
  ```sh
  cd <this_repo_folder>
  jupyuter lab
  ```

  <!-- CONTRIBUTING -->
## **Contributing**

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## **License**
Distributed under the MIT License. See `LICENSE` for more information.

## **Contact**

Gustavo Voltani von Atzingen - gustavo.von.atzingen@gmail.com

Amanda Iaquinta - a.ferrari.iaquinta@gmail.com

Jéssica Toledo - jtoledo@quickium.com
