from setuptools import setup, Extension

setup(ext_modules=[Extension("linux", sources=["linux.c"])])
