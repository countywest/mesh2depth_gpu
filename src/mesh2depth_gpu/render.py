from OpenGL.GL import *
import numpy as np
from mesh2depth_gpu.camera import Camera
from mesh2depth_gpu.mesh import Mesh
from mesh2depth_gpu.shader import Shader
from mesh2depth_gpu.depthmap import DepthMap
import os
from nptyping import NDArray, Shape, UInt8
import glcontext
import platform


class Renderer:
    def __init__(self, gpu_id: int = 0):
        system = platform.system().lower()
        if system == "linux":
            os.environ["GLCONTEXT_DEVICE_INDEX"] = str(gpu_id)
            create_ctx = glcontext.get_backend_by_name("egl")
        else:
            create_ctx = glcontext.default_backend()
        self.ctx = create_ctx(glversion=330, mode="standalone")

        self.shader = Shader(
            vs_path=os.path.join(os.path.dirname(__file__), "shaders", "mesh.vert"),
            fs_path=os.path.join(os.path.dirname(__file__), "shaders", "mesh.frag"),
        )

        glEnable(GL_DEPTH_TEST)

    def destroy(self):
        self.ctx.release()

    def set_target(self, target: Mesh):
        self.target = target

    def render(self, camera: Camera) -> NDArray[Shape["Any, Any, 4"], UInt8]:
        depthmap = DepthMap(camera.width, camera.height)

        # render to a framebuffer
        self.shader.use()
        self.shader.set_matrix4x4("view", camera.view)
        self.shader.set_matrix4x4("projection", camera.projection)
        glViewport(0, 0, camera.width, camera.height)
        glBindFramebuffer(GL_FRAMEBUFFER, depthmap.fbo)
        glClear(GL_DEPTH_BUFFER_BIT)

        # draw mesh
        glBindVertexArray(self.target.vao)
        glDrawElements(GL_TRIANGLES, self.target.indices_size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        glBindTexture(GL_TEXTURE_2D, depthmap.depth_texture)
        buffer = glGetTexImage(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, GL_FLOAT)
        glBindTexture(GL_TEXTURE_2D, 0)

        buffer = np.reshape(buffer, (camera.height, camera.width))  # (h, w)
        buffer = np.flip(buffer, axis=0)

        # linearize
        z = buffer * 2 - 1
        depth = (
            2
            * camera.near
            * camera.far
            / (camera.far + camera.near - z * (camera.far - camera.near))
        )
        empty = buffer == 1.0

        # free gpu memory
        depthmap.free()

        return depth, empty
