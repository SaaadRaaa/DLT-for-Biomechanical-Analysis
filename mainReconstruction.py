import csv
import pickle
from Reconstruction import DLTrecon
import markerdet

# List of video paths
video_paths = ["D:\MaCodes\DLT\moy.MOV"]
minArea = 20
marker_threshold = 100  # Adjust this threshold based on marker visibility


# Load the calibration matrices (Ls) from the pickle file
with open("calibration_params.pkl", "rb") as f:
    Ls = pickle.load(f)

nd = 0
if len(Ls[0]) == 9:
    nd = 2
elif len(Ls[0]) == 12:
    nd = 3
if nd != 2 and nd != 3:
    raise ValueError(
        "Invalid number of dimensions (nd) in the calibration matrices.")


uv = markerdet.returnUV(video_paths, marker_threshold, minArea)
# Check if the number of cameras (views) used for calibration matches the number of detected marker sets
nc = len(uv[0])
if nc != len(Ls):
    raise ValueError("Invalid number of cameras (views).")

# Perform 2D or 3D point reconstruction based on the number of dimensions (nd)
if nd == 2:
    # Perform 2D point reconstruction for each frame
    XY = []
    for frame in uv:
        frame_XY = []
        for i in range(len(frame[0])):
            frame_XY.append(
                DLTrecon(nd, nc, Ls, [view[i] for view in frame])[::-1])
        XY.append(frame_XY)

    # Save reconstructed points to CSV file
    csv_file = "XY.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ["Frame Number"]
        for i in range(len(XY[0])):
            header.append(f"Marker {i + 1} (X, Y)")
        writer.writerow(header)
        for frame_idx, frame_XY in enumerate(XY, start=1):
            row = [frame_idx]
            for point in frame_XY:
                formatted_point = f"({point[0]:.2f}, {point[1]:.2f})"
                row.append(formatted_point)
            writer.writerow(row)

    print("Reconstructed points saved to XY.csv")

elif nd == 3:
    # Perform 3D point reconstruction for each frame
    XYZ = []
    for frame in uv:
        frame_XYZ = []
        for i in range(len(frame[0])):
            frame_XYZ.append(
                DLTrecon(nd, nc, Ls, [view[i] for view in frame])[::-1])
        XYZ.append(frame_XYZ)

    # Save reconstructed points to CSV file
    csv_file = "XYZ.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ["Frame Number"]
        for i in range(len(XYZ[0])):
            header.append(f"Marker {i + 1} (X, Y, Z)")
        writer.writerow(header)
        for frame_idx, frame_XYZ in enumerate(XYZ, start=1):
            row = [frame_idx]
            for point in frame_XYZ:
                formatted_point = f"({point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f})"
                row.append(formatted_point)
            writer.writerow(row)

    print("Reconstructed points saved to XYZ.csv")

else:
    raise ValueError(
        "Invalid number of dimensions (nd). Only 2D and 3D reconstructions are supported.")
