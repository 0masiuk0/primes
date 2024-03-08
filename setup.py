from setuptools import setup, find_packages

setup(
    name='primes',
    version='0.2',
    packages=find_packages(),
    url='https://github.com/0masiuk0/primes',
    license='',
    author='masiuk',
    author_email='',
    description='Primes and factorization related functions with memorization',
    long_description=open('README.md').read(),
    install_requires=['bitarray'])
