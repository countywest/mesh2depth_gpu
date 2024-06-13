from setuptools import setup
from src.mesh2depth_gpu import __version__
setup(
    name='mesh2depth_gpu',
    version=__version__,
    author='Hyeontae Son',
    author_email='countywest@naver.com',
    description='Fast depthmap generation using headless rendering',
    license='MIT',
    platforms=['any'],
    packages=['mesh2depth_gpu'],
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'PyOpenGL',
        'PyGLM',
        'trimesh',
        'nptyping',
        'glcontext'
    ]
)