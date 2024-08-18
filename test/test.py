import trimesh
import numpy as np
import mesh2depth_gpu
import matplotlib.pyplot as plt


def test_bunny():
    # load bunny mesh
    bunny = trimesh.load("./assets/stanford-bunny.obj")

    # get bunny aabb
    v_min = np.min(bunny.vertices, axis=0)
    v_max = np.max(bunny.vertices, axis=0)

    # aabb center & radius
    center = (v_min + v_max) / 2.0
    radius = np.linalg.norm(v_max - v_min) / 2.0

    # fov
    x_fov = 45 / 180 * np.pi  # radian

    # set camera params, image resolution
    param1 = {
        "cam_pos": (center + 2 * radius * np.array([-1, 0, 0])).tolist(),
        "cam_lookat": center.tolist(),
        "cam_up": [0, 1, 0],
        "x_fov": x_fov,
        "near": radius * 0.01,
        "far": radius * 10,
        "height": 1024,
        "width": 1024,
    }

    param2 = {
        "cam_pos": (center + 2 * radius * np.array([1, 0, 0])).tolist(),
        "cam_lookat": center.tolist(),
        "cam_up": [0, 1, 0],
        "x_fov": x_fov,
        "near": radius * 0.01,
        "far": radius * 10,
        "height": 1024,
        "width": 1024,
    }

    # query mesh2depth
    depth_maps = mesh2depth_gpu.convert(
        vertices=np.asarray(bunny.vertices),
        faces=np.asarray(bunny.faces),
        params=[param1, param2],
    )

    plt.imshow(depth_maps[0], interpolation="none")
    plt.colorbar()
    plt.savefig("bunny0.png")
    plt.clf()

    plt.imshow(depth_maps[1], interpolation="none")
    plt.colorbar()
    plt.savefig("bunny1.png")
