from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xnewsbot",
    version="0.2.0",
    description="AI-powered news bot for X.com (Twitter) automation with research and writing capabilities.",
    author="Huzaifa Azhar",
    author_email="huzaifablogger.contact@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={
        'xnewsbot': ['prompts/*.txt', 'images/*'],
    },
    install_requires=[
        "smolagents",
        "selenium",
        "undetected-chromedriver",
        "pywin32",  # for win32clipboard
        "requests",
        "beautifulsoup4",
        "Pillow",  # PIL
        "duckduckgo_search",
        "openai",
    ],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Communications :: Chat",
    ],
    keywords="twitter x automation bot selenium ai news research",
)
