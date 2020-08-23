import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name='stacker',

    version='0.1',

    scripts=['src/cli'],

    author="Theo Paris",

    author_email="theo@throw-out-error.dev",

    description="A Docker compose alternative that uses",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/creepinson/stacker",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

    ],

)
