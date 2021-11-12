from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.20'
DESCRIPTION = 'Ngoto module'
LONG_DESCRIPTION = 'A python module containing variety red team tools'

# Setting up
setup(
    name="Ngoto",
    version=VERSION,
    author="Harry Ludemann",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['googlesearch-python'],
    keywords=['python', 'harryludemann', 'osint', 'hazzah', 'ngoto'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)