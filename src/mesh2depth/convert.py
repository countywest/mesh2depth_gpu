import numpy as np
from typing import List, Dict
from src.mesh2depth.camera import get_camera
from src.mesh2depth.mesh import Mesh
from src.mesh2depth.render import Renderer
from PIL import Image
from OpenGL.GL import *
from nptyping import NDArray, Shape, Float32, UInt32

def convert(vertices: NDArray[Shape["Any, 3"], Float32],
            faces: NDArray[Shape["Any, 3"], UInt32],
            params: List[Dict],
            empty_pixel_value: float = np.nan):
    """
    Args:
        vertices, faces: mesh data
        cameras: list of Camera params
        empty_pixel_value: float
    Return:
        depthmaps: list of depth map w.r.t cameras
    """
    cameras = [get_camera(param) for param in params]
    renderer = Renderer()
    mesh = Mesh(vertices_flatten=np.reshape(vertices, -1).astype(np.float32),
                faces_flatten=np.reshape(faces, -1).astype(np.uint32))
    renderer.set_target(mesh)

    #dummy_camera = Camera()
    #renderer.render(dummy_camera)

    depthmaps = []
    for _, camera in enumerate(cameras):
        depth, empty = renderer.render(camera)
        depth[empty] = empty_pixel_value
        depthmaps.append(depth)

    renderer.terminate()
    return depthmaps