import trimesh
import numpy as np
from src.mesh2depth.convert import convert
import matplotlib.pyplot as pt

if __name__ == "__main__":
    bunny = trimesh.load('./assets/stanford-bunny.obj')

    param1 = {
        'cam_pos': [1, 0.1, 0],
        'cam_lookat': [0, 0.1, 0],
        'cam_up': [0,1,0],
        'x_fov': 0.785,
        'near': 0.01,
        'far': 10,
        'height': 512,
        'width': 512
        }
    param2 = {
        'cam_pos': [-0.5, 0.1, 0],
        'cam_lookat': [0, 0.1, 0],
        'cam_up': [0,1,0],
        'x_fov': 0.785,
        'near': 0.01,
        'far': 10,
        'height': 1024,
        'width': 1024
    }

    print(f'min_x:{np.min(bunny.vertices[:, 0])}, max_x:{np.max(bunny.vertices[:, 0])}')
    print(f'min_y:{np.min(bunny.vertices[:, 1])}, max_y:{np.max(bunny.vertices[:, 1])}')
    print(f'min_z:{np.min(bunny.vertices[:, 2])}, max_z:{np.max(bunny.vertices[:, 2])}')
    depth_maps = convert(vertices=np.asarray(bunny.vertices),
                        faces=np.asarray(bunny.faces),
                        params=[param1, param2])

    pt.imshow(depth_maps[0], interpolation='none')
    pt.colorbar()
    pt.show()