from setuptools import setup, find_packages

setup(
    name='mws_extensions',
    version=__import__('mws_extensions').__version__,
    description=__import__('mws_extensions').__doc__,
    long_description=open('readme.md').read(),
    author='Thomas Berdy',
    author_email='thomas.berdy@seelk.co',
    url='https://gitlab.seelk.io/seelk/open-source/mws_extensions',
    packages=find_packages(),
    classifiers=[
        "Development Status :: Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'mws==0.8.6'
        'python-dateutil',
        'lxml',
    ],
    include_package_data=True,
    zip_safe=False,
)
