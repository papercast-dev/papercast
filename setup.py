from setuptools import setup

setup(
    name="papercast",
    version="0.1",
    py_modules=["papercast"],
    install_requires=[
    ],
    entry_points="""
        [console_scripts]
        papercast-legacy=papercast.scripts.papercast_legacy:papercast_legacy
        papercast=papercast.scripts.papercast:main
        ss=papercast.scripts.ss:ss
    """,
)
