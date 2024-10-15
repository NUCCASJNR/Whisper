from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="WhisperCLI",
    version="1.0.0",
    author="Al-Areef",
    author_email="alareefadegbite@gmail.com",
    description=(
        "WhisperCLI is a secure, anonymous chat application for the command line, enabling private "
        "communication, user profile management, and more—all from your terminal."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NUCCASJNR/WhisperCLI",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.1",
        "argparse",
        "logging",
    ],
    entry_points={
        'console_scripts': [
            'whisper=whisper_cli.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="anonymous-chat cli secure-communication",
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://github.com/NUCCASJNR/WhisperCLI/docs',
        'Source': 'https://github.com/NUCCASJNR/WhisperCLI',
        'Tracker': 'https://github.com/NUCCASJNR/WhisperCLI/issues',
    },
)
