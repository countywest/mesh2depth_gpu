import numpy as np
from typing import List, Dict
from mesh2depth_gpu.camera import get_camera
from mesh2depth_gpu.mesh import Mesh
from mesh2depth_gpu.render import Renderer
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

    depthmaps = []
    for _, camera in enumerate(cameras):
        depth, empty = renderer.render(camera)
        depth[empty] = empty_pixel_value
        depthmaps.append(depth)

        del camera

    renderer.destroy()
    return depthmaps