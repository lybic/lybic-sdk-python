from setuptools import setup, find_packages

setup(
    name='lybic',
    version='0.0.2',
    author='Lybic Development Team',
    author_email='team@lybic.ai',
    description='Lybic sdk for python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lybic/lybic-python-sdk',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.13',
    install_requires=[
        'requests',
        'pydantic',
        'mcp'
    ],
)
