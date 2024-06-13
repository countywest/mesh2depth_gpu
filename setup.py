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
    package_data={'mesh2depth_gpu': ['shaders/mesh.frag', 'shaders/mesh.vert']},
    include_package_data=True,
    install_requires=[
        'numpy',
        'PyOpenGL',
        'PyGLM',
        'trimesh',
        'nptyping',
        'glcontext'
    ]
)