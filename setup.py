import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="algorand-state-sdk",
    description="Algorand State Tool SDK",
    author="palace22",
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    project_urls={
        "Source": "https://github.com/palace22/algorand-state-sdk",
    },
    install_requires=["py-algorand-sdk >= 2.0.0", "dacite >= 1.7.0"],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
)
