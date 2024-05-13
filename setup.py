from setuptools import setup, find_packages

setup(
    name='paradi',
    version='{{ VERSION_PLACEHOLDER }}',
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0"
    ],
    python_requires='>=3.10',
    author='Julien Crambes',
    author_email='julien.crambes@gmail.com',
)
