import numpy as np
import calibmarker
from Calibration import DLTcalib
from Reconstruction import DLTrecon

# List of image paths
image_paths = ["D:/MaCodes/DLT/cam1.JPG",
               "D:/MaCodes/DLT/cam2.JPG"]

xyz = [[44, 0, 37], [44, 0, 0], [0, 0, 38],
       [0, 46, 0], [0, 46, 38], [44, 45, 37]]

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

if nc != len(uv):
    raise ValueError("Invalid number of cameras.")

XYZ = np.zeros((len(xyz), nd))
for i in range(len(uv[0])):
    XYZ[i, :] = DLTrecon(nd, nc, Ls, [uv[j][i] for j in range(nc)])
print('Reconstruction of the same %d points based on %d views and the camera calibration parameters:' % (len(xyz), nc))
print(XYZ)
print('Mean error of the point reconstruction using the DLT (error in cm):')
print(np.mean(np.sqrt(np.sum((np.array(XYZ) - np.array(xyz))**2, 1))))
