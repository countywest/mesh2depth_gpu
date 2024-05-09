import numpy as np
from typing import List
import glm
import math
import pyrr

class Camera:
    projection: glm.mat4
    view: glm.mat4
    near: float
    far: float
    height: int
    width: int

    def __init__(self,
                 K: np.ndarray[(3,3), np.float32]=np.eye(3), # intrinsic
                 w2c: np.ndarray[(4,4), np.float32]=np.eye(4), # cv
                 near: float=0.01,
                 far: float=100,
                 height: int=256,
                 width: int=256):
        c2w = np.linalg.inv(w2c) # [right | down | front | t]
        c2w_gl = np.copy(c2w)
        c2w_gl[:3, 1] = -c2w_gl[:3, 1] # up
        c2w_gl[:3, 2] = -c2w_gl[:3, 2] # front
        w2c_gl = np.linalg.inv(c2w_gl)
        self.view = glm.mat4(w2c_gl)

        self.near = near
        self.far = far
        self.height = height
        self.width = width

        # ====================
        # intrinsic2projection
        # ====================
        fx = K[0,0]
        fy = K[1,1]
        cx = K[0,2]
        cy = K[1,2]
        projection_np = np.zeros((4, 4))

        # Set diagonal elements
        projection_np[0, 0] = 2 * fx / width
        projection_np[1, 1] = 2 * fy / height
        projection_np[2, 2] = -(far + near) / (far - near)

        # Set off-diagonal elements
        projection_np[0, 2] = 2 * cx / width - 1
        projection_np[1, 2] = 2 * cy - height - 1
        projection_np[3, 2] = 1.0
        projection_np[2, 3] = -2 * far * near / (far - near)
        self.projection = glm.mat4(projection_np)

    def set(self,
            cam_pos: List[float],
            cam_lookat: List[float],
            cam_up: List[float],
            x_fov: float,
            near: float,
            far: float,
            height: int,
            width: int):
        """
        Set camera params with other representations (same as https://github.com/daeyun/mesh-to-depth/tree/master?tab=readme-ov-file#example)
        """
        cam_pos = glm.vec3(cam_pos)
        target_pos = glm.vec3(cam_lookat)
        up_vec = glm.vec3(cam_up)
        self.view = glm.lookAt(cam_pos, target_pos, up_vec)

        self.near = near
        self.far = far
        self.height = height
        self.width = width
        aspect_ratio = width / height
        y_fov = math.atan(math.tan(x_fov / 2) / aspect_ratio) * 2
        self.projection = glm.perspective(y_fov, self.width/self.height, self.near, self.far)