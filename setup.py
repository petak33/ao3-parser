import setuptools

with open(file="requirements.txt", mode="r") as read_req:
    requires = [line for line in read_req.read().splitlines() if line != ""]

setuptools.setup(
    name="ao3-parser",
    author="petak33",
    description="Parses raw data from a AO3 browsing page into works and provides tools to create urls for requests.",
    version="1.0.0",
    url="https://github.com/petak33/ao3-parser",

    readme = "README.md",
    python_requires='>=3.8',
    install_requires=requires,
    packages=setuptools.find_packages(include=["AO3Parser"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)