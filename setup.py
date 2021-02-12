import re

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open("webframework/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(name="webframework", version=version, packages=find_packages())
