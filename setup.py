try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'nntoolkit',
    'version': '0.1.24',
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'packages': ['nntoolkit'],
    'scripts': ['bin/nntoolkit'],
    # 'package_data': {'nntoolkit': ['templates/*', 'misc/*']},
    'url': 'https://github.com/MartinThoma/nntoolkit',
    'license': 'MIT',
    'description': 'Neural Network Toolkit',
    'long_description': """A tookit for training feed-forward neural
        networks.""",
    'install_requires': [
        "argparse",
        "theano",
        "nose",
        "natsort",
        "PyYAML",
        "matplotlib"
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
                    'Topic :: Scientific/Engineering :: Artificial Intelligence',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': False,
    'test_suite': 'nose.collector'
}

setup(**config)
