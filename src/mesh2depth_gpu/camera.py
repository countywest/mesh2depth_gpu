import numpy as np
from typing import List, Dict
import glm
import math
from nptyping import NDArray, Shape, Float32
from dataclasses import dataclass
from dacite import from_dict


@dataclass
class Camera:
    projection: glm.mat4
    view: glm.mat4
    near: float
    far: float
    height: int
    width: int


# same as https://github.com/daeyun/mesh-to-depth/tree/master?tab=readme-ov-file#example
@dataclass
class CameraParam1:
    cam_pos: List[float]
    cam_lookat: List[float]
    cam_up: List[float]
    x_fov: float
    near: float
    far: float
    height: int
    width: int

    def to_camera(self) -> Camera:
        cam_pos = glm.vec3(self.cam_pos)
        target_pos = glm.vec3(self.cam_lookat)
        up_vec = glm.vec3(self.cam_up)
        view = glm.lookAt(cam_pos, target_pos, up_vec)

        aspect_ratio = self.width / self.height
        y_fov = math.atan(math.tan(self.x_fov / 2) / aspect_ratio) * 2
        projection = glm.perspective(
            y_fov, self.width / self.height, self.near, self.far
        )

        return Camera(projection, view, self.near, self.far, self.height, self.width)


@dataclass
class CameraParam2:
    K: NDArray[Shape["3, 3"], Float32]  # intrinsic
    m2c: NDArray[Shape["4, 4"], Float32]  # cv
    near: float
    far: float
    height: int
    width: int

    def to_camera(self) -> Camera:
        c2m = np.linalg.inv(self.m2c)  # [right | down | front | t]
        c2m_gl = np.copy(c2m)
        c2m_gl[:3, 1] = -c2m_gl[:3, 1]  # up
        c2m_gl[:3, 2] = -c2m_gl[:3, 2]  # front
        m2c_gl = np.linalg.inv(c2m_gl)
        view = glm.mat4(m2c_gl)

        # ====================
        # intrinsic2projection
        # ====================
        fx = self.K[0, 0]
        fy = self.K[1, 1]
        cx = self.K[0, 2]
        cy = self.K[1, 2]
        projection_np = np.zeros((4, 4))

        # Set diagonal elements
        projection_np[0, 0] = 2 * fx / self.width
        projection_np[1, 1] = 2 * fy / self.height
        projection_np[2, 2] = -(self.far + self.near) / (self.far - self.near)

        # Set off-diagonal elements
        projection_np[0, 2] = 2 * cx / self.width - 1
        projection_np[1, 2] = 2 * cy - self.height - 1
        projection_np[3, 2] = 1.0
        projection_np[2, 3] = -2 * self.far * self.near / (self.far - self.near)
        projection = glm.mat4(projection_np)

        return Camera(projection, view, self.near, self.far, self.height, self.width)


def get_camera(params: Dict) -> Camera:
    """
    Args:
        params: a dictionary of camera parameters
    Return:
        camera instance
    """
    if "cam_pos" in params.keys():
        camera_param = from_dict(data_class=CameraParam1, data=params)
    else:
        camera_param = from_dict(data_class=CameraParam2, data=params)

    camera = camera_param.to_camera()
    return camera
