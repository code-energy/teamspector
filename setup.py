from setuptools import find_packages, setup

setup(
    name='teamspector',
    version='0.0.0',
    install_requires=[
        'tqdm',
        'numpy',
        'scipy',
        'pandas',
        'jupyter',
        'pymongo',
        'seaborn',
        'sklearn',
        'networkx',
        'matplotlib',
        'python-dateutil',
    ],
    scripts=[
        'bin/download',
        'bin/extract',
        'bin/preprocess',
    ],
    entry_points={
        "console_scripts": [
            "experiment = teamspector.experiment:main",
        ]
    },
    packages=find_packages()
)
