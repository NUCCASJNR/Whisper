from setuptools import setup, find_packages

setup(
    name='whisper-cli',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests', 'argparse'],
    entry_points={
        'console_scripts': [
            'whisper=whisper_cli.cli:main',
        ],
    },
)
