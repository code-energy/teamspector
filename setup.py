from setuptools import find_packages, setup

setup(name='teamspector',
      version='0.0.0',
      install_requires=[
          'tqdm',
          'numpy',
          'scipy',
          'pandas',
          'jupyter',
          'pymongo',
          'sklearn',
          'networkx',
          'matplotlib',
          'python-dateutil',
      ],
      scripts=[
          'bin/download-imdbws',
          'bin/extract-imdbws',
          'bin/preprocess-imdbws',
          'bin/experiment-imdbws',
      ],
      packages=find_packages())
