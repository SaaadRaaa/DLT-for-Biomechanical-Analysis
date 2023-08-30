import numpy as np


def DLTrecon(nd, nc, Ls, uvs):
    '''
    Reconstruction of object point from image point(s) based on the DLT parameters.
    This code performs 2D or 3D DLT point reconstruction with any number of views (cameras).
    For 3D DLT, at least two views (cameras) are necessary.

    Parameters
    --------------
    nd : integer
        The number of dimensions of the object space: 3 for 3D DLT and 2 for 2D DLT.
    nc : integer
        The number of cameras (views) used.
    Ls : list of numpy arrays
        The camera calibration parameters of each camera (output of DLTcalib function).
        The Ls parameters are given as columns, and the Ls for different cameras are in the list.
    uvs : list of lists
        The coordinates of the point in the image 2D space of each camera.
        The coordinates of the point are given as columns, and the different views are in the list.

    Returns
    --------------
    xyz : numpy array
        Point coordinates in space.
    '''

    # Convert Ls to array:
    Ls = np.asarray(Ls)

    # Check the parameters:
    if Ls.ndim != 2 or Ls.shape[0] != nc:
        raise ValueError("Invalid number of camera calibration parameters.")

    if len(uvs) != nc:
        raise ValueError("Invalid number of image coordinates.")

    if any(len(uv) != 2 for uv in uvs):
        raise ValueError("Invalid number of image coordinates for a camera.")

    if nd == 3 and nc < 2:
        raise ValueError(
            "At least two cameras are needed for 3D point reconstruction.")

    M = []
    for i in range(nc):
        L = Ls[i]
        u, v = uvs[i][0], uvs[i][1]
        if nd == 2:
            M.append([L[0] - u * L[6], L[1] - u * L[7], L[2] - u * L[8]])
            M.append([L[3] - v * L[6], L[4] - v * L[7], L[5] - v * L[8]])
        elif nd == 3:
            M.append([L[0] - u * L[8], L[1] - u * L[9],
                     L[2] - u * L[10], L[3] - u * L[11]])
            M.append([L[4] - v * L[8], L[5] - v * L[9],
                     L[6] - v * L[10], L[7] - v * L[11]])

    # Find the xyz coordinates:
    U, S, Vh = np.linalg.svd(np.asarray(M))
    # Point coordinates in space:
    xyz = Vh[-1, 0:-1] / Vh[-1, -1]
    return xyz
