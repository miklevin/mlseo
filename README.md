# mlseo
> Pythonic SEO in JupyterLab


## Install

`pip install mlseo --upgrade`

## How to use

Start a new Notebook, preferably in standalone JupyterLab. Then type:

```python
from mlseo import *
```


     Welcome to _                  (\         To chase the rabbit,
      _ __ ___ | |___  ___  ___     \\_ _/(\      run: look()
     | '_ ` _ \| / __|/ _ \/ _ \      0 0 _\)___
     | | | | | | \__ \  __/ (_) |   =(_T_)=     )*
     |_| |_| |_|_|___/\___|\___/      /"/   (  /
               The adventure begins! <_<_/-<__|

# The Most Important Things

## Storing API Responses into Database

This package contains a variety of building-blocks for constructing "deliverables" for the field of Search Engine Optimization (SEO). The goal is to make expressing such deliverables "light and breezy" by establishing certain conventions. For example, to crawl 1-page of a site into a local database:

```python
import httpx
from sqlitedict import SqliteDict as sqldict

url = 'https://mikelev.in/'
with sqldict('crawl.db') as db:
    db[url] = httpx.get(url)
    db.commit()
```

## Using Tuples As Composite-Keys

We are using SQlite as a key-value database in a way that requires the keys to be strings. Keys must be unique so if we use the URL as the key we can store each page we crawl only once. Instead of just a URL, the key to your database can contain a URL and Date so that we can crawl sites on subsequent days and store it into the same key-value database. Such a tuple key looks like this:

```python
from datetime import date

url = 'https://mikelev.in/'
atuple = (date.today(), url)
```

## Pickling and Unpickling

Tuples must become strings to be a key in the key-value database we're using. This is accomplished through ***pickling***. We "pickle" the tuple to make it a string, then can use that string as a key in the dictionary database.

```python
import pickle
from datetime import date

pkl = lambda x: pickle.dumps(x)
unpkl = lambda x: pickle.loads(x)

url = 'https://mikelev.in/'
today = date.today()
atuple = (today, url)

now_a_string = pkl(atuple)
print(now_a_string)
```

### Pickling Keys For Database

This example uses a pickled tuple containing the Date and the URL as the database key. It shows data both going in and coming out of the database. Notice the pickled key is restored to its original form. This approach prevents duplicate records in your database. Because dictionary keys must be unique, attempts to insert a new record with the same URL+Date key will fail, meaning this crawler can only record each page on the site once per day.

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
    tupkey = (date.today(), url)
    db[pkl(tupkey)] = httpx.get(url)
    db.commit()

# Data comes out
with sqldict('crawl.db') as db:
    for tupkey in db:
        adate, url = unpkl(tupkey)
        print(adate, url)
```

# mlseo Tutorials

[**HOUSEKEEPING:**](./housekeeping.ipynb) Once you have the basic trick of using a persistent dictionary and using tuples as your primary key, you'll need a place to ***put*** the database and all your other INPUT/OUTPUT files besides lumping it all into the top-level of your folder.

## A Word About JupyterLab

### Recovering pip installs

For now standalone Jupyter has to be reinstalled a lot and its easy to lose your pip-installed packages. For mlseo you can get all the necessary packages back by just typing this into a Code cell:

    pip install mlseo --upgrade

### Useful Dev Tools

I also recommend installing nbdev and nb_black if you're doing any development work inside Jupyter:

    pip install nb_black
    pip install nbdev

### Restart Kernel & Clear All Outputs A LOT

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
