from OpenGL.GL import *
from nptyping import NDArray, Shape, Float32, UInt32


class Mesh:
    def __init__(
        self,
        vertices_flatten: NDArray[Shape["Any"], Float32],
        faces_flatten: NDArray[Shape["Any"], UInt32],
    ):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.position_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.position_buffer)
        glBufferData(
            GL_ARRAY_BUFFER,
            vertices_flatten.itemsize * len(vertices_flatten),
            vertices_flatten,
            GL_STATIC_DRAW,
        )

        self.index_buffer = glGenBuffers(1)
        self.indices_size = len(faces_flatten)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.index_buffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            faces_flatten.itemsize * self.indices_size,
            faces_flatten,
            GL_STATIC_DRAW,
        )

        # positions
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE, vertices_flatten.itemsize * 3, ctypes.c_void_p(0)
        )

        glBindVertexArray(0)
