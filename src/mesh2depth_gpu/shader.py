from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm


def compile_shader(vertex_shader: str, fragment_shader: str):
    v_shader = OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
    f_shader = OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    ID = glCreateProgram()
    glAttachShader(ID, v_shader)
    glAttachShader(ID, f_shader)
    glLinkProgram(ID)
    glGetProgramInfoLog(ID)
    glDeleteShader(v_shader)
    glDeleteShader(f_shader)
    return ID


class Shader:
    def __init__(self, vs_path: str, fs_path: str):
        self.vertex_shader = self.load(
            vs_path
        )  # os.path.join(os.path.dirname(__file__), 'shaders', 'mesh.vert'))
        self.fragment_shader = self.load(
            fs_path
        )  # os.path.join(os.path.dirname(__file__), 'shaders', 'mesh.frag'))
        self.shader_program = compile_shader(self.vertex_shader, self.fragment_shader)

    def load(self, path: str):
        shader_source = ""
        with open(path) as f:
            shader_source = f.read()
        return str.encode(shader_source)

    def set_int(self, uniform_variable_name: str, value: int):
        uniform_loc = glGetUniformLocation(self.shader_program, uniform_variable_name)
        glUniform1i(uniform_loc, value)

    def set_float(self, uniform_variable_name: str, value: float):
        uniform_loc = glGetUniformLocation(self.shader_program, uniform_variable_name)
        glUniform1f(uniform_loc, value)

    def set_vec3(self, uniform_variable_name: str, vec3: glm.vec3):
        uniform_loc = glGetUniformLocation(self.shader_program, uniform_variable_name)
        glUniform3fv(uniform_loc, 1, glm.value_ptr(vec3))

    def set_matrix3x3(self, uniform_variable_name: str, matrix3x3: glm.mat3):
        uniform_loc = glGetUniformLocation(self.shader_program, uniform_variable_name)
        glUniformMatrix3fv(uniform_loc, 1, GL_FALSE, glm.value_ptr(matrix3x3))

    def set_matrix4x4(self, uniform_variable_name: str, matrix4x4: glm.mat4):
        uniform_loc = glGetUniformLocation(self.shader_program, uniform_variable_name)
        glUniformMatrix4fv(uniform_loc, 1, GL_FALSE, glm.value_ptr(matrix4x4))

    def use(self):
        glUseProgram(self.shader_program)
