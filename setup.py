from setuptools.command.build_ext import build_ext as _build_ext

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


class build_ext(_build_ext):
    'to install numpy'
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


config = {
    'cmdclass': {'build_txt': build_ext},  # numpy hack
    'setup_requires': ['numpy'],           # numpy hack
    'name': 'nntoolkit',
    'version': '0.1.29',
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': ['nntoolkit'],
    'scripts': ['bin/nntoolkit'],
    'platforms': ['Linux', 'MacOS X', 'Windows'],
    'url': 'https://github.com/MartinThoma/nntoolkit',
    'license': 'MIT',
    'description': 'Neural Network Toolkit',
    'long_description': ("A tookit for training feed-forward neural networks. "
                         "nntoolkit is designed to be used from both, "
                         "within Python scripts and from the shell. "
                         "See http://pythonhosted.org/nntoolkit/ for the "
                         "documentation."),
    'install_requires': [
        "argparse",
        "theano",
        "nose",
        "natsort",
        "PyYAML",
        "h5py",
        "numpy",
        "Cython"
    ],
    'keywords': ['Neural Networks', 'Feed-Forward', 'NN', 'MLP'],
    'download_url': 'https://github.com/MartinThoma/nntoolkit',
    'classifiers': ['Development Status :: 3 - Alpha',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Topic :: Scientific/Engineering :: Artificial Intelligence',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': False,
    'test_suite': 'nose.collector'
}

setup(**config)
