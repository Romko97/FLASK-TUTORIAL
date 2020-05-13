from setuptools import find_packages, setup

setup(
    name='flaskr-pkg-Roman97',
    version='1.0.0',
    author="Roman Halychanivskyi",
    author_email="elgoog6651@gmail.com",
    description="A small example flask priject",
    packages=find_packages(),
    url="https://github.com/Romko97/FLASK-TUTORIAL/tree/master/flaskr",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)