# mesh2depth_gpu

<a href="https://github.com/countywest/mesh2depth_gpu/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
![versions](https://img.shields.io/badge/python-3.7+-blue.svg)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Fast depthmap generation using PyOpenGL.
Inspired by the CPU-only [mesh-to-depth](https://github.com/daeyun/mesh-to-depth) package, this project aims to generate depth data from 3D triangular meshes in Python scripts while leveraging GPU-acceleration.
On a Linux system, ```mesh2depth_gpu``` supports EGL headless rendering, allowing it to be used without any display device.


## Installation
```sh
pip install mesh2depth_gpu
```

## Example
```python
import numpy as np
import mesh2depth_gpu as m2d

# camera parameters, type1
# same as https://github.com/daeyun/mesh-to-depth except for the 'is_depth' option.
param1 = {
    "cam_pos": [1, 1, 1],
    "cam_lookat": [0, 0, 0],
    "cam_up": [0, 1, 0],
    "x_fov": 0.349, # End-to-end field of view in radians
    "near": 0.01,
    "far": 100.0,
    "height": 1024,
    "width": 1024,
}

# camera parameters, type2
param2 = {
    "K": np.array([
        750.0, 0.0, 512.0,
        0.0, 750.0, 512.0,
        0.0, 0.0, 1.0
    ]).astype(np.float32), # np.array, 3x3 intrinsic matrix
    "m2c": np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, -1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 1.0],
        [0.0, 0.0, 0.0, 1.0]
    ]).astype(np.float32), # np.array, 4x4 extrinsic matrix
    "near": 0.01,
    "far": 100.0,
    "height": 1024,
    "width": 1024,
}

params = [param1, param2]

# load mesh data
vertices = ...  # An array of shape (num_vertices, 3) and type np.float32.
faces = ...  # An array of shape (num_faces, 3) and type np.uint32.

# depthmap generation
depth_maps = m2d.convert(vertices, faces, params, empty_pixel_value=np.nan)
```

## Test
Please follow the instructions in [test](https://github.com/countywest/mesh2depth_gpu/tree/main/test)