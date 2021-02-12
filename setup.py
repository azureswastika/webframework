import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("webframework/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="webframework",
    version=version,
    packages=["webframework"],
    install_requires=['Jinja2>=2.11.3'],
    python_requires=">=3.6",)
