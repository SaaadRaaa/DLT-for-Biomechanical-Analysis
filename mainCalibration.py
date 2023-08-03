import numpy as np
import calibmarker
from Calibration import DLTcalib
from Reconstruction import DLTrecon
import pickle

# List of image paths
image_paths = ["DLT/photos/photo1.JPG"]

xyz = [[0, 0], [48, 0], [0, 57.5], [48, 53.6]]

nd = len(xyz[0])

# Call the returnUV function from calibmarker module to get marker coordinates
uv = calibmarker.returnUV(image_paths)
print(uv)

nc = len(uv)

calib_matrices = []  # List to store calibration matrices

for i in range(len(uv)):
    Li, err = DLTcalib(nd, xyz, uv[i])
    calib_matrices.append(Li)

Ls = []
for matrix in calib_matrices:
    Ls.append(matrix.tolist())  # Convert NumPy array to list
    # Use Ls as needed for further processing
print("Calibration matrices:")
print(Ls)

# Save Ls to a pickle file
with open("calibration_params.pkl", "wb") as f:
    pickle.dump(Ls, f)

if nc != len(uv):
    raise ValueError("Invalid number of cameras.")

XYZ = np.zeros((len(xyz), nd))
for i in range(len(uv[0])):
    XYZ[i, :] = DLTrecon(nd, nc, Ls, [uv[j][i] for j in range(nc)])
print('Reconstruction of the same %d points based on %d views and the camera calibration parameters:' % (len(xyz), nc))
print(XYZ)
print('Mean error of the point reconstruction using the DLT (error in cm):')
print(np.mean(np.sqrt(np.sum((np.array(XYZ) - np.array(xyz))**2, 1))))
