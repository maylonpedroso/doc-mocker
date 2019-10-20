import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doc-mocker",
    version="0.0.2",
    author="Maylon Pedroso",
    author_email="maylonpedroso@gmail.com",
    description="Mock Document Image Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maylonpedroso/doc-mocker",
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=["Pillow", "wikipedia"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["doc-mocker = main:run"]},
)
