from setuptools import setup, Extension

module1 = Extension('linux', sources=['linux.c'])

setup(name='linux',
      version='1.0',
      description='',
      ext_modules=[module1])
