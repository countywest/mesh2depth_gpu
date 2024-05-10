from OpenGL.GL import *
import numpy as np
from src.mesh2depth.camera import Camera
from src.mesh2depth.mesh import Mesh
from src.mesh2depth.shader import Shader
from src.mesh2depth.depthmap import DepthMap
import glfw
import platform
import os
from nptyping import NDArray, Shape, UInt8

class Renderer:
    def __init__(self):
        if not glfw.init():
            print("Cannot initialize GLFW")
            exit()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        if platform.system() == "Darwin":
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
            glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, GL_FALSE) # to make framebuffer size and window size equal

        self.window = glfw.create_window(256, 256, "dummy", None, None)
        glfw.make_context_current(self.window)

        self.shader = Shader(vs_path=os.path.join(os.path.dirname(__file__), 'shaders', 'mesh.vert'),
                             fs_path=os.path.join(os.path.dirname(__file__), 'shaders', 'mesh.frag'))

        glEnable(GL_DEPTH_TEST)

    def terminate(self):
        glfw.terminate()

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

        buffer = np.reshape(buffer, (camera.height, camera.width)) # (h, w)
        buffer = np.flip(buffer, axis=0)

        # linearize
        z = buffer * 2 - 1
        depth = 2 * camera.near * camera.far / (camera.far + camera.near - z * (camera.far - camera.near))
        empty = buffer == 1.0
        return depth, empty