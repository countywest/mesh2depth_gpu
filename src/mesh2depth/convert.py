import numpy as np
from typing import List
from src.mesh2depth.camera import Camera

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