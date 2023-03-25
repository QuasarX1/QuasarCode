import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "QuasarCode",
    version = "0.6.0",
    author = "Christopher Rowe",
    author_email = "thequasarx1@gmail.com",
    description = "A general purpose library for Python applications.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/QuasarX1/QuasarCode",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    install_requires = [
        "numpy",
        "matplotlib",
        "scipy"
      ],
    python_requires = ">=3.7",
)