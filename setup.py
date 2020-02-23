import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shoe-mkaraosff", # Replace with your own username
    version="0.0.1",
    author="Michael Karasoff",
    author_email="mike@karatronics.com",
    description="Configuration and control for HEOS speakers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkarasoff/shoe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
