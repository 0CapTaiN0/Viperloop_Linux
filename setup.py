import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="Viperloop",
    version="1.0.0",
    author="0CapTaiN0",
    author_email="0mahdibalaei0@gmail.com",
    description="A tool to easily set and reset DNS on Linux systems. DNS Changer For Iranian people(Linux).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0CapTaiN0/Viperloop_Linux",
    packages=setuptools.find_packages(where=".", include=["Linux", "Linux.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "viperdns=Linux.main:main_cli",
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/0CapTaiN0/Viperloop_Linux/issues',
        'Source': 'https://github.com/0CapTaiN0/Viperloop_Linux/',
    },
) 