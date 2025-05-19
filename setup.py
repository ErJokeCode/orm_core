from setuptools import setup, find_packages

setup(
    name="orm_core",
    version="0.0.1",
    author="Erik Soloviev",
    author_email="eriksoloviev@gmail.com",
    description="ORM Core",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=[
        'pydantic>=2.11.4',
        'fastapi>=0.115.12',
        'SQLAlchemy>=2.0.41'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.13',
)
