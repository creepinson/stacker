import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name='docker-stacker',

    version='1.0.0',

    entry_points={
        'console_scripts': [
            'stacker=stacker:main',
        ],
    },

    install_requires=[
        'json-five',
        'docker',
        'argparse',
        'attrdict',
        'tqdm',
    ],

    author="Theo Paris",

    author_email="theo@throw-out-error.dev",

    description="A Docker compose alternative that uses json5.",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/creepinson/stacker",

    packages=setuptools.find_packages(),

    classifiers=[
    ],

)
