from setuptools import setup, find_packages

setup(
    name="fileorganizer",
    version="0.1",
    author="edelove",
    description="A simple file organizer script by extensions",
    packages=find_packages(),
    py_modules=["file_organiser"],
    install_requires = [],
    entry_points ={
        "console_scripts":[
            'organizer=file_organiser:main',
         ],
    },
)