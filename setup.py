#To create a distribution package:
#$ python3 setup.py sdist bdist_wheel
#
#To upload for pip:
#$ python3 -m twine upload dist/*

import setuptools

SETUP_VERSION="0.1.9"

SHOE_VERSION_FILE="shoelib/shoeVer.py"
SHOE_VERSION_VAR="SHOE_VERSION"

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(SHOE_VERSION_FILE, "r") as fh:
    lines=fh.readlines()

with open(SHOE_VERSION_FILE, "w") as fh:
    for line in lines:
        if line[:len(SHOE_VERSION_VAR)] == SHOE_VERSION_VAR:
            line="%s=\"%s\"" % (SHOE_VERSION_VAR, SETUP_VERSION)
        fh.write(line)

setuptools.setup(
    name="shoe", # Replace with your own username
    version=SETUP_VERSION,
    author="Michael Karasoff",
    author_email="mike@karatronics.com",
    description="Configuration and control for HEOS speakers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkarasoff/shoe",
    packages=setuptools.find_packages(),
    scripts=['shoe'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
