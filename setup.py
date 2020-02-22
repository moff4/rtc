#!/usr/bin/env python3
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='rtc',
    version='1.0.0',
    author='Komissarov Andrey',
    author_email='Komissar.off.andrey@mail.ru',
    description='Runtime Type Checker',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/moff4/rtc',
    install_requires=[],
    packages=setuptools.find_packages(),
    classifiers=[
        'Typing :: Typed',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
