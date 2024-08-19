from setuptools import setup
import os
import sys

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_DIR, "src", "mesh2depth_gpu"))
from version import __version__

setup(
    name="mesh2depth_gpu",
    version=__version__,
    author="Hyeontae Son",
    author_email="countywest@naver.com",
    description="Fast depthmap generation using headless rendering",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    platforms=["any"],
    packages=["mesh2depth_gpu"],
    package_dir={"": "src"},
    package_data={"mesh2depth_gpu": ["shaders/mesh.frag", "shaders/mesh.vert"]},
    include_package_data=True,
    install_requires=["numpy", "PyOpenGL", "PyGLM", "nptyping", "glcontext", "dacite"],
)
