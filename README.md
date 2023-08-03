# DLT-for-Biomechanical-Analysis
Usage of direct linear transformation (camera calibration and point reconstruction) for accurate motion analysis in biomechanical applications.

This repository contains the implementation of the Direct Linear Transform (DLT) algorithm for camera calibration, enabling accurate measurement and analysis of motion in biomechanics research. The DLT method provides a robust and efficient solution for calibrating multiple cameras, allowing accurate reconstruction of object points from image points.

## Features
- Camera calibration for multiple cameras using DLT algorithm
- 2D and 3D point reconstruction from recorded videos
- Marker detection in images and videos for calibration and tracking
- Error analysis and validation

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SaaadRaaa/DLT-for-Biomechanical-Analysis.git

## Usage

### Calibration.py
This file contains functions for camera calibration using the Direct Linear Transform (DLT) algorithm. Calibration is the process of determining the intrinsic and extrinsic camera parameters required to map image points to real-world coordinates. The functions in this file are designed to handle both 2D and 3D calibration.

**Usage:**
1. Import the `Calibration` module in your Python script.
2. Prepare calibration points in real-world coordinates (`xyz`) and their corresponding image points (`uv`) collected from images of a calibration pattern.
3. Call the `DLTcalib` function with the `nd`, `xyz`, and `uv` as arguments to obtain the camera calibration matrices (`Ls`).
4. The calibration matrices (`Ls`) can be saved and used for 2D or 3D point reconstruction.

### Reconstruction.py
This file contains a function for reconstructing object points from image points based on the DLT parameters obtained during calibration. Reconstruction involves mapping image points captured by multiple cameras to their corresponding real-world 2D or 3D coordinates.

**Usage:**
1. Import the `Reconstruction` module in your Python script.
2. Load the camera calibration matrices (`Ls`) previously obtained during the calibration phase.
3. Prepare a list of pixel coordinates (`uv`) collected from multiple cameras for each frame in a video.
4. Call the `DLTrecon` function with the `nd`, `nc`, `Ls`, and `uv` as arguments to obtain the reconstructed object points (`XYZ`) for each frame.
5. The reconstructed points can be used for further biomechanical analysis.

### calibmarker.py
This file contains functions for detecting markers in images using a mouse-driven interactive approach. The user is prompted to manually mark the position of markers in each image by clicking on them. These pixel coordinates will be later used for camera calibration.

**Usage:**
1. Import the `calibmarker` module in your Python script.
2. Prepare a list of image paths (`image_paths`) containing images of the calibration pattern with visible markers.
3. Call the `returnUV` function with `image_paths` as an argument to start the marker detection process.
4. The function will display the images, and the user needs to click on the markers using the mouse to record their pixel coordinates.
5. The pixel coordinates of the markers will be saved as a list of lists (`uv`), which can be used for camera calibration.

### mainCalibration.py
This is the main script for camera calibration using the DLT algorithm. It utilizes functions from `Calibration.py` and `calibmarker.py` to perform the calibration process.

**Usage:**
1. Import the required modules and functions.
2. Prepare a list of image paths (`image_paths`) containing images of the calibration pattern with visible markers.
3. Define the real-world coordinates of the calibration points (`xyz`) and the number of dimensions (`nd`) of the object space.
4. Call the `returnUV` function from `calibmarker.py` to obtain the pixel coordinates of the detected markers for each image.
5. Use the pixel coordinates and real-world coordinates to perform camera calibration using the `DLTcalib` function from `Calibration.py`.
6. The calibration matrices (`Ls`) will be saved and can be used for further 2D or 3D point reconstruction.

### mainReconstruction.py
This is the main script for reconstructing object points from video frames using DLT parameters obtained during calibration. It utilizes functions from `Reconstruction.py` and `markerdet.py` to detect markers in the video frames.

**Usage:**
1. Import the required modules and functions.
2. Load the camera calibration matrices (`Ls`) obtained during the calibration phase.
3. Prepare a list of video paths (`video_paths`) containing video footage of the markers in motion.
4. Call the `returnUV` function from `markerdet.py` to detect the markers in each video frame and obtain their pixel coordinates.
5. Use the pixel coordinates and calibration matrices (`Ls`) to perform 2D or 3D point reconstruction using the `DLTrecon` function from `Reconstruction.py`.
6. The reconstructed points for each frame will be saved as a CSV file containing frame numbers and their corresponding 2D or 3D coordinates.


## Contributing

Contributions to this project are highly encouraged and appreciated. If you find any bugs, have feature suggestions, or want to improve the existing code, please follow these guidelines to contribute:

1. **Fork** the repository to your own GitHub account.
2. Create a new **branch** from the main branch for your changes.
3. Make your desired changes, improvements, or bug fixes in your branch.
4. **Test** your changes thoroughly to ensure they work as expected.
5. **Commit** your changes with clear and descriptive commit messages.
6. **Push** your changes to your GitHub repository.
7. Create a **pull request (PR)** from your branch to the main branch of this repository.
8. Provide a clear and detailed description of your changes in the PR, explaining why they are beneficial.
9. **Reviewers** will examine your PR, provide feedback, and work with you to finalize the changes.
10. Once **approved**, your changes will be **merged** into the main branch.

## Issues

If you encounter any issues with the code or have questions about the project, feel free to [create an issue](https://github.com/SaaadRaaa/DLT-for-Biomechanical-Analysis/issues). Provide a detailed description of the problem you are facing, and we will be happy to assist you.

## Contact

For any other inquiries or feedback, you can contact the author:

- **GitHub**: [SaaadRaaa](https://github.com/SaaadRaaa)
- **Email**: [sadraamirabadi@gmail.com](mailto:sadraamirabadi@gmail.com)

