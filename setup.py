import setuptools

setuptools.setup(
    name="qsub",
    version="1.0",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["qstat"]
)
