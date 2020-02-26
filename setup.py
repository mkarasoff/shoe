import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shoe", # Replace with your own username
    version="0.1.0",
    author="Michael Karasoff",
    author_email="mike@karatronics.com",
    description="Configuration and control for HEOS speakers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkarasoff/shoe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
