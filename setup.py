from setuptools import setup

setup(
    name="papercast",
    version="0.1",
    py_modules=["papercast"],
    install_requires=[
    ],
    packages=["papercast"],
    entry_points="""
        [console_scripts]
        papercast=papercast.scripts.papercast:main
    """,
)
