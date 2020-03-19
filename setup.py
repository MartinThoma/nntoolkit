# Third party modules
from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):
    "To install numpy."

    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy

        self.include_dirs.append(numpy.get_include())


setup(
    cmdclass={"build_txt": build_ext},  # numpy hack
    setup_requires=["numpy"],  # numpy hack
    install_requires=[
        "argparse",
        "Cython",
        "h5py",
        "keras",
        "natsort",
        "numpy",
        "pytest",
        "PyYAML",
    ],
)
