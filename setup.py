"""
WIP: Program's import needs to updated inorder to package the program.
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reforg-sourabhtk37",
    version="0.0.1",
    author="T K Sourab",
    author_email="sourabhtk37@gmail.com",
    description="Key value endpoints caller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sourabhtk37/reforg",
    project_urls={
        "Bug Tracker": "https://github.com/sourabhtk37/reforg/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_namespace_packages(),
    python_requires=">=3.6",
    install_requires=[
        "requests==2.25.1",
    ],
    entry_points={
        "console_scripts": [
            "reforg = reforg.cli:main",
        ]
    },
)