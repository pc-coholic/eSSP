try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='eSSP',
    version='1.0.2',
    description='Basic eSSP library',
    author='muccc',
    author_email='martin@pc-coholic.de',
    url='https://github.com/pc-coholic/eSSP',
    packages=['eSSP'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    license='?',
    install_requires=['pyserial'],
)
