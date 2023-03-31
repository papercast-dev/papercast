Install papercast

```bash
git clone https://github.com/papercast-dev/papercast.git
cd papercast
pip install -e .
```

Install the plugins

```
cd examples/arxiv-grobid-say-github-pages
pip install -r requirements.txt
```

Run the server

```bash
python ./server.py
```

Add a paper

```bash
papercast add --pipeline default --arxiv-id 1706.03762
```
