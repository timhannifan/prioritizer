from setuptools import find_packages, setup

setup(
    name="prioritizer",
    version="0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['prioritizer = prioritizer.cli:run'],
    },
)
