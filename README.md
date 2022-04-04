# mlseo
> Pythonic SEO in JupyterLab


## Install

`pip install mlseo --upgrade`

## How to use

Start a new Notebook, preferably in standalone JupyterLab. Then type:

```python
from mlseo import *
```
    
Chase the rabbit.

# The Gist of mlseo

This is NOT an SEO Software Suite of the sort that automatically sets up webserver user interfaces for you. This is completely the opposite. This package contains a grab-bag of building-blocks useful for constructing "deliverables" for the field of Search Engine Optimization (SEO), and tries to entice you into coding some Python in JupyterLab Desktop.

## Light & Breezy Python

The goal is to make expressing such deliverables "light and breezy" by establishing certain good Python (Pythonic) conventions that you can use throrought your data-jockying career. The approach I'm about to show you is ***perfect*** for raw-data capture from API-calls, using the arguments of the API-call itself as the database-key to recover the locally stored response. If this sounds like gobbledygook to you right now, just bear with me. You'll get it.

## Best Technique You've Never Heard Of

Use the exact values you fed to the API to fetch the data in the first place as the keys to your database to retreive the data again locally. I just boosted your earning-capacity x2 at least. SQLite3 (part of standard Python) is a gift. The dict API connected to it is a gift. The context-manager ("with *something* as *something*") is a gift. Use them.

For example, to crawl 1-page of a site into a local database:

```python
import httpx
from sqlitedict import SqliteDict as sqldict

url = 'https://mikelev.in/'
with sqldict('crawl.db') as db:
    db[url] = httpx.get(url)
    db.commit()
```

## Tuples As Composite-Keys (Unique Constraints)
If the database key should also contain the **date** of the crawl and a full/partial boolean (True/False), we can use a 3-position tuple. This is better practice than appending strings together, because you can keep dates as real datetime objects and perform date operations on them easily when stepping through records.

```python
from datetime import date

url = 'https://mikelev.in/'
atuple = (date.today(), url, True)
```

### Pickling and Unpickling

The way tuples become string keys (necessary for sqlitedict) is by a common Python serialization function called ***pickling***. We "pickle" the tuple to make it a string-based dictionary key. We can then iterate through all keys, unpickling the primary key and have it back in its orginal tuple-state as we go.

```python
import pickle
from datetime import date


pkl = lambda x: pickle.dumps(x)
unpkl = lambda x: pickle.loads(x)

url = 'https://mikelev.in/'
today = date.today()

atuple = (today, url, True)
now_a_string = pkl(atuple)


print(now_a_string)
> >>b'\x80\x04\x959\x00\x00\x00\x00\x00\x00\x00\x8c\x08datetime\x94\x8c\x04date\x94\x93\x94C\x04\x07\xe6\x04\x04\x94\x85\x94R\x94\x8c\x13https://mikelev.in/\x94\x88\x87\x94.'
print(unpkl(now_a_string))
> >>(datetime.date(2022, 4, 4), 'https://mikelev.in/', True)```

### Pickling Keys For Database

The example below puts the 2 above examples together to save the page-crawl to the database using a pickled tuple as the dictionary key. This is worth contemplating. Composite primary keys are unique constraints, thus naturally preventing duplicate redords from being recorded for the same URL for the same day. This sets the stage for efficient subsequent crawls.

```python
import httpx
import pickle
from datetime import date
from sqlitedict import SqliteDict as sqldict


pkl = lambda x: pickle.dumps(x)
unpkl = lambda x: pickle.loads(x)

url = 'https://mikelev.in/'

# Data goes in
with sqldict('crawl.db') as db:
    tupkey = (date.today(), url, True)
    db[pkl(tupkey)] = httpx.get(url)
    db.commit()

# Data comes out
with sqldict('crawl.db') as db:
    for tupkey in db:
        adate, url, full = unpkl(tupkey)
        print(adate, url, full)
```

# From Here

By following the install and how-to-use instructions above, you will be invited to run_me(), thereby initiating the example given here. Do the trick to get the trick. This is top-down education. \*POOF\* here's a gift. Now look at how that works.    

# A Word About JupyterLab

## Recovering pip installs

For now standalone Jupyter has to be reinstalled a lot and its easy to lose your pip-installed packages. For mlseo you can get all the necessary packages back by just typing this into a Code cell:

    pip install mlseo --upgrade

## Useful Dev Tools

I also recommend installing nbdev and nb_black if you're doing any development work inside Jupyter:

    pip install nb_black
    pip install nbdev

## Restart Kernel & Clear All Outputs A LOT

And lastly, shortcuts always get deleted between Jupyter reinstalls so here's my most important shortcut. It's always a good time to Restart kernel and clear all outputs.
```javascript
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
```
