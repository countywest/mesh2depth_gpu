import numpy as np
from typing import List, Dict
from mesh2depth_gpu.camera import get_camera
from mesh2depth_gpu.mesh import Mesh
from mesh2depth_gpu.render import Renderer
from OpenGL.GL import *
from nptyping import NDArray, Shape, Float32, UInt32


def convert(
    vertices: NDArray[Shape["Any, 3"], Float32],
    faces: NDArray[Shape["Any, 3"], UInt32],
    params: List[Dict],
    empty_pixel_value: float = np.nan,
    gpu_id: int = 0,
):
    """
    Args:
        vertices, faces: mesh geometry data
        params: list of camera params dictionaries
                following two formats are allowed for the dictionary
                {
                    'cam_pos': List[float],
                    'cam_lookat': List[float],
                    'cam_up': List[float],
                    'x_fov': float,
                    'near': float,
                    'far': float,
                    'height': int,
                    'width': int
                }
                or
                {
                    'K': np.ndarray[(3,3), np.float32],
                    'm2c': np.ndarray[(4,4), np.float32],
                    'near': float,
                    'far': float,
                    'height': int,
                    'width': int
                }
        empty_pixel_value: float
        gpu_id: int, device id. changing gpu_id is allowed only for the linux system.
    Return:
        depthmaps: list of depth map w.r.t cameras
    """
    cameras = [get_camera(param) for param in params]
    renderer = Renderer(gpu_id)
    mesh = Mesh(
        vertices_flatten=np.reshape(vertices, -1).astype(np.float32),
        faces_flatten=np.reshape(faces, -1).astype(np.uint32),
    )
    renderer.set_target(mesh)

    depthmaps = []
    for _, camera in enumerate(cameras):
        depth, empty = renderer.render(camera)
        depth[empty] = empty_pixel_value
        depthmaps.append(depth)

        del camera

    renderer.destroy()
    return depthmaps
