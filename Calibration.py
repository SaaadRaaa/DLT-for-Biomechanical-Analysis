import numpy as np


def Normalization(nd, x):
    '''
    Normalization of coordinates (centroid to the origin and mean distance of sqrt(2 or 3).

    Parameters
    --------------
    nd : integer
        Number of dimensions (2 for 2D; 3 for 3D).
    x : numpy array
        The data to be normalized (directions at different columns and points at rows).

    Returns
    --------------
    Tr: the transformation matrix (translation plus scaling)
    x: the transformed data
    '''

    m, s = np.mean(x, 0), np.std(x)
    if nd == 2:
        Tr = np.array([[s, 0, m[0]], [0, s, m[1]], [0, 0, 1]])
    else:
        Tr = np.array([[s, 0, 0, m[0]], [0, s, 0, m[1]],
                       [0, 0, s, m[2]], [0, 0, 0, 1]])

    Tr = np.linalg.inv(Tr)
    x = np.dot(Tr, np.concatenate((x.T, np.ones((1, x.shape[0])))))
    x = x[0:nd, :].T

    return Tr, x


def DLTcalib(nd, xyz, uv):
    '''
    Camera calibration by DLT using known object points and their image points.
    This code performs 2D or 3D DLT camera calibration with any number of views (cameras).
    For 3D DLT, at least two views (cameras) are necessary.

    Parameters
    --------------
    nd : integer
        The number of dimensions of the object space: 3 for 3D DLT and 2 for 2D DLT.
    xyz : list
        The coordinates in the object 3D or 2D space of the calibration points.
    uv : list
        The coordinates in the image 2D space of these calibration points.

    The coordinates (x,y,z and u,v) are given as columns and the different points as rows.
    For the 2D DLT (object planar space), only the first 2 columns (x and y) are used.
    There must be at least 6 calibration points for the 3D DLT and 4 for the 2D DLT.

    Returns
    --------------
    L : numpy array
        Array of the 8 or 11 parameters of the calibration matrix.
    err : float
        Error of the DLT (mean residual of the DLT transformation in units of camera coordinates).
    '''

    # Convert all variables to numpy array:
    xyz = np.asarray(xyz)
    uv = np.asarray(uv)
    # number of points:
    n = xyz.shape[0]
    # Check the parameters:
    if uv.shape[0] != n:
        raise ValueError(
            'xyz (%d points) and uv (%d points) have different number of points.' % (n, uv.shape[0]))
    if (nd == 2 and xyz.shape[1] != 2) or (nd == 3 and xyz.shape[1] != 3):
        raise ValueError('Incorrect number of coordinates (%d) for %dD DLT (it should be %d).' % (
            xyz.shape[1], nd, nd))
    if (nd == 3 and n < 6) or (nd == 2 and n < 4):
        raise ValueError(
            '%dD DLT requires at least %d calibration points. Only %d points were entered.' % (nd, 2*nd, n))

    # Normalize the data to improve the DLT quality (DLT is dependent of the system of coordinates).
    # This is relevant when there is a considerable perspective distortion.
    # Normalization: mean position at origin and mean distance equals to 1 at each direction.
    Txyz, xyzn = Normalization(nd, xyz)
    Tuv, uvn = Normalization(2, uv)

    A = []
    if nd == 2:  # 2D DLT
        for i in range(n):
            x, y = xyzn[i, 0], xyzn[i, 1]
            u, v = uvn[i, 0], uvn[i, 1]
            A.append([x, y, 1, 0, 0, 0, -u*x, -u*y, -u])
            A.append([0, 0, 0, x, y, 1, -v*x, -v*y, -v])
    elif nd == 3:  # 3D DLT
        for i in range(n):
            x, y, z = xyzn[i, 0], xyzn[i, 1], xyzn[i, 2]
            u, v = uvn[i, 0], uvn[i, 1]
            A.append([x, y, z, 1, 0, 0, 0, 0, -u*x, -u*y, -u*z, -u])
            A.append([0, 0, 0, 0, x, y, z, 1, -v*x, -v*y, -v*z, -v])

    # convert A to array
    A = np.asarray(A)
    # Find the 11 (or 8 for 2D DLT) parameters:
    U, S, Vh = np.linalg.svd(A)
    # The parameters are in the last line of Vh and normalize them:
    L = Vh[-1, :] / Vh[-1, -1]
    # Camera projection matrix:
    H = L.reshape(3, nd+1)
    # Denormalization:
    H = np.dot(np.dot(np.linalg.pinv(Tuv), H), Txyz)
    H = H / H[-1, -1]
    L = H.flatten()
    # Mean error of the DLT (mean residual of the DLT transformation in units of camera coordinates):
    uv2 = np.dot(H, np.concatenate((xyz.T, np.ones((1, xyz.shape[0])))))
    uv2 = uv2/uv2[2, :]
    # mean distance:
    err = np.sqrt(np.mean(np.sum((uv2[0:2, :].T - uv)**2, 1)))

    return L, err
