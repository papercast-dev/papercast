from setuptools import setup, find_packages

setup(
    name="papercast",
    version="0.2.0",
    install_requires=["fastapi", "uvicorn", "loguru", "requests"],
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        papercast=papercast.scripts.papercast:main
    """,
    extras_require={
        "dev": [
            "pytest",
            "pytest-mock",
            "pytest-asyncio",
            "pytest-cov",
        ],
    },
)
