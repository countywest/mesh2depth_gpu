import trimesh
import numpy as np
from src.mesh2depth.camera import Camera
from src.mesh2depth.convert import convert

if __name__ == "__main__":
    bunny = trimesh.load('./assets/stanford-bunny.obj')
    camera1 = Camera()
    camera2 = Camera()
    camera1.set(cam_pos=[2, 0.1, 0], cam_lookat=[0, 0.1, 0], cam_up=[0,1,0],
                x_fov=0.785, near=0.01, far=10,
                height=512, width=512)
    camera2.set(cam_pos=[-2, 0.1, 0], cam_lookat=[0, 0.1, 0], cam_up=[0,1,0],
                x_fov=0.785, near=0.01, far=10,
                height=512, width=512)

    print(f'min_x:{np.min(bunny.vertices[:, 0])}, max_x:{np.max(bunny.vertices[:, 0])}')
    print(f'min_y:{np.min(bunny.vertices[:, 1])}, max_y:{np.max(bunny.vertices[:, 1])}')
    print(f'min_z:{np.min(bunny.vertices[:, 2])}, max_z:{np.max(bunny.vertices[:, 2])}')
    convert(vertices=np.asarray(bunny.vertices),
            faces=np.asarray(bunny.faces),
            cameras=[camera1, camera2, camera1, camera1])