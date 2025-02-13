from OpenGL.GL import *
from typing import Dict, Tuple
import numpy as np

_Resolution = Tuple[int, int]  # (height, width)


class DepthMap:
    gl_depth_texture_pool: Dict[_Resolution, np.uint32] = {}

    def __init__(self, width: int, height: int, fbo: np.uint32):
        self.width = width
        self.height = height

        resolution = (self.height, self.width)
        if resolution in self.gl_depth_texture_pool.keys():
            self.depth_texture = self.gl_depth_texture_pool[resolution]
            return

        self.depth_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.depth_texture)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_DEPTH_COMPONENT,
            self.width,
            self.height,
            0,
            GL_DEPTH_COMPONENT,
            GL_FLOAT,
            None,
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depth_texture, 0
        )
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.gl_depth_texture_pool[resolution] = self.depth_texture

    @classmethod
    def destroy_textures(cls):
        depth_textures = list(cls.gl_depth_texture_pool.values())
        glDeleteTextures(1, depth_textures)
