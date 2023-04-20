# Listen to Arxiv papers as a podcast hosted on GitHub Pages

This example shows how to use Papercast to listen to papers from [arxiv.org](https://arxiv.org) as a podcast. The podcast is hosted on [GitHub Pages](https://pages.github.com/).

The tutorial will go through the following steps:
    
1. Create a GitHub repository and clone it locally
2. Create a GitHub Pages site
3. Install Papercast and its dependencies
3. Write the Papercast script
4. Process some papers
5. Subscribe to the podcast

##  1. Create a GitHub repository

Create a new GitHub repository. The repository name will be used as the podcast name. For example, if you create a repository named `arxiv-podcast`, the podcast will be available at `https://<your-username>.github.io/arxiv-podcast/`.

Clone the repository locally and create a new file named `server.py`:

    $ git clone https://github.com/<your-username>/<your-repository>.git
    $ cd <your-repository>
    $ touch server.py

Make folders to hold the podcast data:

    $ mkdir data
    $ mkdir data/pdfs
    $ mkdir data/json
    $ mkdir data/mp3s
    $ mkdir data/txts

##  2. Create a GitHub Pages site

Go to the repository settings and enable GitHub Pages. Select the `main` branch as the source. The branch will be used to host the podcast.

##  3. Install Papercast and its dependencies

Save the following contents to a file named `requirements.txt`:

    git+https://github.com/papercast-dev/papercast@v0.1.0
    git+https://github.com/papercast-dev/papercast-arxiv@v0.1.0
    git+https://github.com/papercast-dev/papercast-semanticscholar@v0.1.0
    git+https://github.com/papercast-dev/papercast-grobid@v0.1.0
    git+https://github.com/papercast-dev/papercast-say@v0.1.0
    git+https://github.com/papercast-dev/papercast-pdf@v0.1.0
    git+https://github.com/papercast-dev/papercast-github-pages-podcast@v0.1.0
    python-dotenv

Install the dependencies:

    $ pip install -r requirements.txt

##  4. Write the Papercast script

Open the `server.py` file and write the following script:

```python
from papercast.pipelines import Pipeline
from papercast.collectors import ArxivCollector
from papercast.processors import SayProcessor
from papercast.processors import GROBIDProcessor
from papercast.publishers import GithubPagesPodcastPublisher
from papercast.server import Server
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("PAPERCAST_ZOTERO_API_KEY", None)
user_id = os.getenv("PAPERCAST_ZOTERO_USER_ID", None)

if api_key is None or user_id is None:
    raise ValueError("Zotero API key or user ID not found")

pipeline = Pipeline(name="default")

pipeline.add_processor(
    "arxiv", ArxivCollector(pdf_dir="data/pdfs", json_dir="data/json")
)

pipeline.add_processor(
    "grobid",
    GROBIDProcessor(
        remove_non_printable_chars=True, grobid_url="http://localhost:8070/"
    ),
)

pipeline.add_processor("say", SayProcessor(mp3_dir="data/mp3s", txt_dir="data/txts"))

pipeline.add_processor(
    "github_pages",
    GithubPagesPodcastPublisher(
        title="example-papercast",
        base_url="https://example.github.io/papercast/",
        language="en-us",
        subtitle="Drinking the firehose one paper at a time",
        copyright="Rights to paper content are reserved by the authors for each paper. I make no claim to ownership or copyright of the content of this podcast.",
        author="Anonymous Author",
        email="email@example.com",
        description="A podcast of research articles, created with papercast (github.com/papercast-dev/papercast)",
        cover_path="https://example.github.io/papercast/cover.jpg",
        categories=["Mathematics", "Tech News", "Courses"],
        keywords=[
            "Machine Learning",
            "Natural Language Processing",
            "Artificial Intelligence",
        ],
        xml_path="/path/to/your/papercast/feed.xml",
    ),
)

pipeline.connect("arxiv", "pdf", "grobid", "pdf")
pipeline.connect("grobid", "text", "say", "text")
pipeline.connect("say", "mp3_path", "github_pages", "mp3_path")
pipeline.connect("grobid", "abstract", "github_pages", "description")
pipeline.connect("grobid", "title", "github_pages", "title")

server = Server(pipelines={"default": pipeline})

if __name__ == "__main__":
    server.run()
```


## 4. Run the Papercast Server and process some papers

Run the server:

    $ python ./server.py

The server will start and listen for requests. You can now process some papers. 

In a new terminal, run the following command to process the paper with the ID `1706.03762`:

    $ papercast add --pipeline default --arxiv-id 1706.03762

Since we are using github pages for hosting, we'll have to commit the changes and push them to GitHub:

    $ git add feed.xml
    $ git add data/mp3s/*.mp3
    $ git commit -m "Add Attention is All You Need"
    $ git push origin main

## 5. Subscribe to the podcast

Give GitHub pages a few minutes to update. After update, the podcast will be available at `https://<your-username>.github.io/<your-repository>/feed.xml`. You can subscribe to the podcast using your favorite podcast app.