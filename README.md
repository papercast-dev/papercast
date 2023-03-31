# Papercast

![papercast logo](./papercast_logo.png)


<!-- 
[![Documentation Status](https://readthedocs.org/projects/papercast/badge/?version=latest)](https://papercast.readthedocs.io/en/latest/?badge=latest)
An extensible framework for audio narration of technical documents. Written in Python. -->

## Features
Add documents in multiple formats, from popular sources:
- PDF
- TeX/LaTeX
- ArXiv
- Semantic Scholar

Flexible text extraction
- GROBID
- Write your own!

Flexible text narration
- OSX `say` command
- Write your own!

Publish to multiple endpoints:
- Self-hosted RSS podcast using GitHub Pages
- Any other endpoint you can think of

Run anywhere:
- Local machine
- Cloud (AWS, GCP, Azure, etc.)

## How it works

### Modules
Papercast is designed around 3 types of modules:

- **Collectors** convert documents to a usable format (plaintext for now).
- **Processors** process the document 
- **Publishers** publish the audio to your desired endpoint (e.g. a podcast feed).

Customize the behavior at each of these steps by writing your own modules.

### Interfaces
A papercast instance is accessible via a **command-line interface (CLI)** and a web server via a **REST API**.

## Getting Started
### Install dependencies

Install papercast and its dependencies

```bash
pip install -e .
```
