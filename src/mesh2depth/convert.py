import numpy as np
from typing import List
from src.mesh2depth.camera import Camera
from src.mesh2depth.mesh import Mesh
from src.mesh2depth.render import Renderer
from PIL import Image
from OpenGL.GL import *

def convert(vertices: np.ndarray[(int, 3), np.float32],
            faces: np.ndarray[(int, 3), np.uint32],
            cameras: List[Camera],
            empty_pixel_value: float = np.nan):
    """
    Args:
        vertices, faces: mesh data
        cameras: list of Camera params
        empty_pixel_value: float
    Return:
        depthmaps: list of depth map w.r.t cameras
    """
    renderer = Renderer()
    mesh = Mesh(vertices_flatten=np.reshape(vertices, -1).astype(np.float32),
                faces_flatten=np.reshape(faces, -1).astype(np.uint32))
    renderer.set_target(mesh)

    dummy_camera = Camera()
    renderer.render(dummy_camera)

    for _, camera in enumerate(cameras):
        depth, empty = renderer.render(camera)
        depth[empty] = empty_pixel_value

    renderer.terminate()