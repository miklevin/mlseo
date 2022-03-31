# mlseo
> Pythonic SEO in JupyterLab


This package contains a variety of building-blocks for constructing "deliverables" for the field of Search Engine Optimization (SEO). The goal is to make expressing such deliverables "light and breezy". For example, to crawl 1-page of a site into a local database:

    from sqlitedict import SqliteDict as sqldict
    import requests
    
    key = 'https://mikelev.in/'
    with sqldict('crawl.db') as db:
        db[key] = requests.get(key)
        db.commit()

## Install

`pip install -U mlseo`

## How to use

Start a new Notebook, preferably in standalone JupyterLab. Then type:

    from mlseo import *
    
Then follow the instructions.

## Standalone JupyterLab

I also recommend installing nbdev and nb_black if you're doing any development work inside Jupyter:

    pip install nb_black
    pip install nbdev
    
Standalone Jupyter changes a lot wiping out settings. Shortcuts are the hardest ones to get back, so here's mine. It's always a good time to restart kernel and clear all outputs.

    {
        "shortcuts": [
            {
                "command": "kernelmenu:restart-and-clear",
                "keys": [
                    "Ctrl Shift R"
                ],
                "selector": "body"
            }
        ]
    }

