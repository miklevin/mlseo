# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['display', 'Markdown', 'Audio', 'first_run', 'async_get_responses', 'beep', 'fig', 'h1', 'h2', 'h3', 'h4',
           'h5', 'h6', 'from_file', 'good_url', 'user_agent', 'extract_apex', 'extract_meta_link', 'extract_links',
           'extract_title', 'extract_meta', 'extract_meta_link', 'extract_hx', 'extract_body', 'extract_stemmed',
           'extract_url_keywords', 'extract_keywords', 'gsc_guess_site', 'gsc_url2keyword_query', 'gsc_url_query',
           'gsc2df', 'df_allout', 'ga_accounts', 'ga_properties', 'ga_properties_g4', 'ga_profiles', 'ga_everything',
           'inspect_url', 'drop_table', 'pk_compositor', 'pk_inserter', 'config2dict', 'build_google_search_query',
           'extract_serps', 'chrome', 'run_me', 'look', 'show_globals', 'enlighten_me', 'save_me', 'please_explain',
           'bs', 'lr', 'SPACES', 'LINES', 'pstem', 'stop_words', 'pkl', 'unpkl', 'svc_ga', 'svc_ga4', 'svc_gsc',
           'svc_mail', 'svc_oauth', 'svc_sheet', 'svc_photo', 'svc_youtube', 'url', 'response']

# Cell

import re
import nltk
import httpx
import ohawf
import pickle
import sqlite3
import asyncio
import configparser
from os import name
import pandas as pd
from sys import path
from os import environ
from art import text2art
from pathlib import Path
from random import shuffle
from asyncio import gather
from subprocess import call
from itertools import cycle
from pyppeteer import launch
from rich.table import Table
from rich.theme import Theme
from time import time, sleep
from contextlib import closing
from tldextract import extract
from collections import Counter
from rich.console import Console
from nltk.corpus import stopwords
from yake import KeywordExtractor
from collections import namedtuple
from nltk.stem import PorterStemmer
from datetime import date, timedelta
from inspect import signature, getdoc
from apiclient.discovery import build
from bs4 import BeautifulSoup as bsoup
from urllib.parse import urlparse, urljoin
from sqlitedict import SqliteDict as sqldict
from dateutil.relativedelta import relativedelta
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import ListPropertiesRequest


# Create do-nothing functions for running from Terminal
# These will all be overwritten by IPython import below
display = lambda x: x
Markdown = lambda x: x
Audio = lambda x: x
first_run = True


nltk.download("stopwords", quiet=True)
try:
    from IPython.display import display, Markdown, Audio, HTML

    is_jupyter = True
except:
    is_jupyter = False

if is_jupyter:
    from IPython.display import display, Markdown, Audio, HTML

if is_jupyter and __name__ == "__main__":
    display(HTML("<h3>Continue running the cells.</h3>"))

# Cell

bs = "\\"
lr = "\n"  # Because f-strings don't support \n.
SPACES = re.compile(r"(?a:\s+)")  # RegEx pattern used to format messages
LINES = re.compile(r"(?a: +)")  # RegEx pattern used to format messages

# Keyword parsing stuff
pstem = PorterStemmer()
stop_words = stopwords.words("english")

# For using tuples as single-column SQLite database keys
pkl = lambda x: pickle.dumps(x)
unpkl = lambda x: pickle.loads(x)

# Connections to mlseo's enabled-by-default Google Services
svc_ga = lambda: build("analytics", "v3", credentials=creds)
svc_ga4 = lambda: build("analyticsreporting", "v4", credentials=creds)
svc_gsc = lambda: build("searchconsole", "v1", credentials=creds)
svc_mail = lambda: build("gmail", "v1", credentials=creds)
svc_oauth = lambda: build("oauth2", "v2", credentials=creds)
svc_sheet = lambda: build("sheets", "v4", credentials=creds)
svc_photo = lambda: build("photoslibrary", "v1", credentials=creds)
svc_youtube = lambda: build("youtube", "v3", credentials=creds)


async def async_get_responses(reqs, func=None):
    """Return a list of tuples of asyncronously fetched URLs responses or function output.
    Tuples always contain the key (URL or tuple) in first postion and response in second.
    Sets up responses for rapid commit to key/value databases like SqliteDict."""

    rv = False

    if not func and not callable(func):
        if type(reqs) == str:
            reqs = [reqs]  # Must be in list.
        if not all([good_url(x) for x in reqs]):
            return "All URLs must be good"

    limits = httpx.Limits(max_keepalive_connections=5, max_connections=100)
    async with httpx.AsyncClient(timeout=10.0, limits=limits) as client:
        if func and callable(func):
            use_func = func
        else:
            use_func = client.get
        resps = await gather(*[use_func(req) for req in reqs])
        rv = list(zip(reqs, resps))

    return rv


def beep():
    """Causes a beep when run from Jupyter. Useful when running long-running scripts
    and you want to walk away and be alerted with a beep when the job is done."""
    if is_jupyter:
        display(Audio("beep.wav", autoplay=True))
    else:
        print("BEEP!")


def fig(text):
    """Returns Figlet-style ASCII-art of input text for when h1's aren't big enough."""
    if is_jupyter:
        display(
            HTML(
                f'<pre style="white-space: pre;">{text2art(text).replace(lr, "<br/>")}</pre>'
            )
        )
    else:
        print(text2art(text))
    global first_run
    if first_run and text != "This?":
        first_run = False
        h1("Well done!")
        h2("You'll be an SEO in no time.")
        msg = f"""From this point on you will have to enter multiple lines of text for
        each example so that it can prompt you to the next step. When you copy/paste text
        be careful to maintain indents consistent with the example. You can select all
        text in a Code block and Tab or Shift+Tab to shift text left or right. Also you
        can learn about the <a href="https://pypi.org/project/art/">art</a> package
        that makes the cool text (and much more)."""
        display(Markdown(SPACES.sub(" ", msg)))
        print()
        display(
            Markdown(
                """
```python
import httpx

url = "https://mikelev.in/"
response = httpx.get(url)

enlighten_me()
```"""
            )
        )
        print()


def h1(text):
    """Return text as an HTML-style h1 headline when run from Jupyter."""
    if is_jupyter:
        display(Markdown(f"# {text}"))
    else:
        print(f"# {text}")


def h2(text):
    """Return text as an HTML-style h2 headline when run from Jupyter."""
    if is_jupyter:
        display(Markdown(f"## {text}"))
    else:
        print(f"## {text}")


def h3(text):
    """Return text as an HTML-style h3 headline when run from Jupyter."""
    if is_jupyter:
        display(Markdown(f"### {text}"))
    else:
        print(f"### {text}")


def h4(text):
    """Return text as an HTML-style h4 headline when run from Jupyter."""
    if is_jupyter:
        display(Markdown(f"#### {text}"))
    else:
        print(f"#### {text}")


def h5(text):
    """Return text as an HTML-style h5 headline when run from Jupyter."""
    if is_jupyter:
        display(Markdown(f"##### {text}"))
    else:
        print(f"##### {text}")


def h6(text):
    """Return text as an HTML-style h6 headline when run from Jupyter."""
    if is_jupyter:
        display(Markdown(f"####### {text}"))
    else:
        print(f"###### {text}")


def from_file(file_name):
    """Return Python list loaded from lines in file (load keywords, sites, etc).
    Makes loading lists of keywords and URLs from file very easy."""

    rv = False
    with open(file_name) as fh:
        spotty = fh.read().split("\n")
    spotless = [x for x in spotty if x]
    if all(spotless):
        rv = spotless
    return rv


def good_url(url):
    """Return input URL if well-formed per urlparse which evals True, Else False.
    Makes checking whether you have a good URL very easy. Often used in all() func."""

    rv = False  # Default is to return false.
    pieces = urlparse(url)
    if (
        pieces.scheme  # Notice use of short-circuit evaluation.
        and pieces.scheme in ["http", "https"]
        and pieces.netloc
        and "." in pieces.netloc
    ):
        rv = url
    return rv


def user_agent():
    """Return a user-agent at random from external file of user-agents.
    Useful for lightweight disguising of http-fetching mechanism."""

    rv = False
    try:
        user_agents = from_file("./user_agents.txt")
        shuffle(user_agents)
        iteragent = cycle(user_agents)
        rv = {"User-agent": next(iteragent)}
    except:
        pass
    return rv


def extract_apex(url):
    """Return the registered or apex domain of a given good URL. Else return False.
    Makes for a good pivot-table column (group by site) or folder save location."""

    rv = False  # Default is to return false.
    if not good_url(url):
        url = f"https://{url}"
    if good_url(url):
        parts = extract(url)
        apex = f"{parts.domain}.{parts.suffix}"
        rv = apex
    return rv


def extract_meta_link(html, link_name="canonical"):
    """Return href attribute of link element where rel attribute has provided value.
    Mainly useful for extracting canonical."""

    if good_url(html):
        html = get(html, headers=user_agent())
    rv = False
    soup = bsoup(html, "lxml")
    links = soup.find_all("link")
    for link in links:
        attrs = link.attrs
        if "rel" in attrs and attrs["rel"][0] == link_name:
            if "href" in attrs:
                rv = attrs["href"]
    return rv


def extract_links(page, allow_offsite=False):
    """Return a list of on-site links from provided URL or text.
    Useful for site-crawling. Defaults to on-site links for crawling purposes."""

    def homepage(url):
        """Return guessed homepage given URL.
        Useful for building absolute links during crawl."""

        rv = False
        parts = urlparse(url)
        scheme, netloc = parts.scheme, parts.netloc
        if all([scheme, netloc]):
            rv = f"{parts.scheme}://{parts.netloc}/"
        return rv

    def guess_page(text):
        """Return guessed url of page given only text.
        Useful for beginning crawl from HTML fetched from uknown URL."""

        rv = False
        canonical = extract_meta_link(text, "canonical")
        if good_url(canonical):
            rv = canonical
        return rv

    rv = False
    if good_url(page):
        parts = urlparse(page)
        hpage = f"{parts.scheme}://{parts.netloc}/"
        text = httpx.get(page, headers=user_agent()).text
    else:
        hpage = homepage(guess_page(page))
        text = page
    soup = bsoup(text, "html.parser")
    rv = True
    if rv:
        seen = set()
        table = []

        for i, link in enumerate(soup.find_all("a")):
            if "href" in link.attrs:
                href = link.attrs["href"]
                if ":" in href and "//" not in href:
                    continue
                if "://" not in href:
                    href = urljoin(hpage, href)
                if href == "/":
                    href = hpage
                if allow_offsite or (homepage(href)) == hpage:
                    if "#" in href:
                        href = href[: href.index("#")]
                    if href not in seen:
                        seen.add(href)
                        table.append(href)
        rv = table
    return rv


def extract_title(page):
    """Return title from provided URL or text. Useful for figuring out targeted keyword of page."""
    rv = False
    if good_url(page):
        page = get(page, headers=user_agent())
    soup = bsoup(page, "lxml")
    title = soup.title.string.strip()
    title = title.strip().replace("\n", "")
    rv = title
    return rv


def extract_meta(html, meta_name="description"):
    """Return content attribute from meta element whose name attribute has provided value.
    Useful for extracting descriptions and other meta values for analysis."""

    rv = None
    if good_url(html):
        html = httpx.get(html, headers=user_agent())
    soup = bsoup(html, "lxml")
    metas = soup.find_all("meta")
    for meta in metas:
        attrs = meta.attrs
        if "name" in attrs and attrs["name"] == meta_name:
            if "content" in attrs:
                rv = attrs["content"]
    return rv


def extract_meta_link(html, link_name="canonical"):
    """Return href attribute of link element where rel attribute has provided value.
    Mainly useful for extracting canonical."""

    if good_url(html):
        html = httpx.get(html, headers=user_agent())
    rv = None
    soup = bsoup(html, "lxml")
    links = soup.find_all("link")
    for link in links:
        attrs = link.attrs
        if "rel" in attrs and attrs["rel"][0] == link_name:
            if "href" in attrs:
                rv = attrs["href"]
    return rv


def extract_hx(page, hx="h1"):
    """Return headline element from provided URL or text. Defaults to H1."""
    rv = None
    if good_url(page):
        page = httpx.get(page, headers=user_agent())
    soup = bsoup(page, "lxml")
    soup_str = f"soup.{hx}"
    title = eval(soup_str)
    if title and title.string:
        title = title.string.strip().replace("\n", "")
        rv = title
    return rv


def extract_body(html, lower=True):
    """Return text extracted from body element of html.
    Useful for looking at page-content with HTML and scripts stripped out."""

    rv = False
    soup = bsoup(html, features="html.parser").get_text(separator=" ", strip=True)
    if lower:
        soup = soup.lower()
    rv = soup
    return rv


def extract_stemmed(html):
    """Return stemmed text extracted from body element of html.
    Useful as a preliminary step for keyword analysis."""

    rv = False
    soup = bsoup(html, features="html.parser").get_text(separator=" ", strip=True)
    stripped = re.sub(r"[^ -~]", " ", soup)
    if stripped:
        stemmed = pstem.stem(stripped)
        stemmed = " ".join([x for x in stemmed.split() if x not in stop_words])
        rv = stemmed
    return rv


def extract_url_keywords(url, stem=False):
    """Return keyword extracted from URL.
    Useful for figuring out what keywords a URL is targeting."""

    rv = False
    if good_url(url):
        parts = urlparse(url)
        keywords = re.split("\W+", parts.path)
        keywords = " ".join([x for x in keywords if x and not x.isnumeric()])
        if stem:
            keywords = extract_stemmed(keywords)
        rv = keywords
    return rv


def extract_keywords(response, stem=False, top=10, ke_args=("en", 3, 0.75, 100, None)):
    """Return list of target keywords descending by score given an httpx response object.
    Useful for figuring out what keywords page-content is targeting."""

    rv = False
    lan, n, dedupLim, top, features = ke_args

    url_keywords = ""
    if type(response) == httpx.Response:
        url = str(response.url)
        text = response.text
        url_keywords = extract_url_keywords(url)
    elif type(response) == str:
        text = response
    kw_extractor = KeywordExtractor(
        lan=lan, n=n, dedupLim=dedupLim, top=top, features=features
    )

    if stem:
        title = extract_stemmed(extract_title(text))
        description = extract_stemmed(extract_meta(text, "description"))
        body = extract_stemmed(text)
    else:
        title = extract_title(text).lower()
        description = extract_meta(text, "description")
        if description:
            description = description.lower()
        else:
            description = ""
        body = extract_body(text)

    meta_stuff = " ".join([url_keywords, title, description])
    examine_me = " ".join([meta_stuff, body])
    keywords = kw_extractor.extract_keywords(examine_me)
    keywords = [x for x in keywords if len(x[0].split()) > 1][:top]
    rv = keywords

    return rv


def gsc_guess_site(url):
    """Return best site-match in Google Search Console to provided URL."""
    gsc_sites = [x["siteUrl"] for x in svc_gsc().sites().list().execute()["siteEntry"]]
    site_dict = dict([(re.split("https://|http://|:", x)[1], x) for x in gsc_sites])
    rv = None
    try:
        rv = site_dict[extract_apex(url)]
    except:
        ...
    return rv


def gsc_url2keyword_query(pagestart_date=None, end_date=None, days=486, days_back=4):
    # https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics/query

    # Set default start and end dates
    today = date.today()
    if not start_date:
        start_date = f"{today - timedelta(days=days + days_back)}"
    if not end_date:
        end_date = f"{today - timedelta(days=days_back)}"

    # Build the request
    request = {
        "dimensions": ["QUERY"],
        "dimensionFilterGroups": [
            {
                "filters": [
                    {"dimension": "PAGE", "operator": "EQUALS", "expression": page}
                ]
            }
        ],
        "startDate": start_date,
        "endDate": end_date,
    }
    return request


def gsc_url_query(url=None, start_date=None, end_date=None, days=486, days_back=4):
    """Return Google Search Console query to get list of keywords for a URL.
    Return keywords for entire site if url left off."""

    # Set default start and end dates
    today = date.today()
    if not start_date:
        start_date = f"{today - timedelta(days=days + days_back)}"
    if not end_date:
        end_date = f"{today - timedelta(days=days_back)}"

    # Build the request
    rv = {
        "dimensions": ["QUERY"],
        "startDate": start_date,
        "endDate": end_date,
    }
    if url:
        rv["dimensionFilterGroups"] = [
            {
                "filters": [
                    {"dimension": "PAGE", "operator": "EQUALS", "expression": url}
                ]
            }
        ]
    return rv


def gsc2df(data, dimensions=None, extras=None):
    """Return Pandas DataFrame given standard GSC searchanalytics query.
    Dimension columns will be generically named if list not provided."""

    table = []
    if "rows" in data:
        for row in data["rows"]:
            keys, clicks, impressions, ctr, position = tuple(row.values())
            new_row = keys + [clicks, impressions, ctr, position]
            if extras and type(extras) == dict:
                more_cols = []
                for akey in extras:
                    more_cols.append(extras[akey])
                new_row = more_cols + new_row
            table.append(new_row)
    defaults = ["clicks", "impressions", "ctr", "position"]
    if not dimensions:
        dimensions = [f"dimension_{x + 1}" for x in range(len(keys))]
    columns = dimensions + defaults
    if extras and type(extras) == dict:
        more_cols = []
        for akey in extras:
            more_cols.append(akey)
        columns = more_cols + columns

    rv = pd.DataFrame(table, columns=columns)
    return rv


def df_allout(df, name, sql=False):
    """Create csv, Excel and SQL output of provided name from provided df."""
    df.fillna("", inplace=True)
    df.to_csv(f"{apex}/{name}.csv")
    df.to_excel(f"{apex}/{name}.xlsx")
    if sql:
        with closing(sqlite3.connect(dbfile)) as conn:
            df.to_sql(name, conn, if_exists="append", index=False)


def ga_accounts(service=None, everything=False):
    """Return a list of Google Analytics Accounts accessible to Google login."""
    if not service:
        service = svc_ga()
    accounts = service.management().accounts().list().execute()
    if everything:
        return accounts
    else:
        if accounts.get("items"):
            alist = []
            for item in accounts["items"]:
                alist.append((item["name"], item["id"]))
            return alist


def ga_properties(account, service=None, everything=False):
    """Return a list of Google Analytics Web Properties accessible to Google login
    given an Account ID."""
    if not service:
        service = svc_ga()
    properties = service.management().webproperties().list(accountId=account).execute()
    if everything:
        return properties
    else:
        if properties.get("items"):
            alist = []
            for item in properties["items"]:
                alist.append((item["name"], item["id"]))
            return alist


def ga_properties_g4(account_id):
    """Return a list of Google Analytics G4 Accounts accessible to Google login
    given an Account ID."""
    client = AnalyticsAdminServiceClient(credentials=creds)
    results = client.list_properties(
        ListPropertiesRequest(filter=f"parent:accounts/{account_id}", show_deleted=True)
    )
    table = []
    for item in results:
        pid = item.name.split("/")[1]
        name = item.display_name
        table.append((name, pid))
    rv = table
    return rv


def ga_profiles(account, property_id, service=None, everything=False):
    """Return a list of Google Analytics Profile IDs accessible to Google login
    given an Account and Web Property ID. (aka Views)"""
    if not service:
        service = svc_ga()
    profiles = (
        service.management()
        .profiles()
        .list(accountId=account, webPropertyId=property_id)
        .execute()
    )
    if everything:
        return profiles
    else:
        if profiles.get("items"):
            alist = []
            for item in profiles["items"]:
                alist.append((item["name"], item["id"]))
            return alist


def ga_everything(service=None, ga4=False):
    """Print and return an object containing all Accoount, Web Property and Profile
    IDs accessible to to Google Login."""
    if not service:
        service = svc_ga()
    acts = {}
    accounts = ga_accounts(service)
    for account in accounts:
        print()
        print("Account: %s %s" % account)
        key, val = account
        acts[account] = []
        plist = []
        if ga4:
            properties = ga_properties_g4(account[1])
            for prop in properties:
                print(f"{' ' * 4}Property: {prop}")
                plist.append(prop)
            acts[account].append({prop: plist})
        else:
            properties = ga_properties(account[1], service)
            if properties:
                for prop in properties:
                    print(f"{' ' * 4}Property: {prop}")
                    acts[account].append({prop: plist})
                    profiles = ga_profiles(account[1], prop[1])
                    if profiles:
                        plist = []
                        for profile in profiles:
                            print("%sProfile: %s" % (" " * 8, profile))
                            plist.append(profile)
                        acts[account].append({prop: plist})
    return acts


def inspect_url(url, site, service=None):
    """Return a Google Search Console URL Inspection API response for given URL."""
    if not service:
        service = svc_gsc()
    request = {"inspectionUrl": url, "siteUrl": site, "languageCode": "en-us"}

    response = service.urlInspection().index().inspect(body=request).execute()
    # r = response['inspectionResult']
    r = response
    return r


def drop_table(db, table):
    """Drop SQLite table."""
    stmt = f"DROP TABLE IF EXISTS {table};"
    with closing(sqlite3.connect(f"{db}")) as conn:
        conn.execute(stmt)
    return stmt


def pk_compositor(db, table, columns, composite_keys):
    """Create SQLite table with composite primary key, especially
    useful for transforming SqliteDict key/values to rows & columns.
    Easiest way to use is with DataFrame column slices like this:
    pk_compositor("file.db", "table", df.columns, df.columns[:2])"""

    def lc(maybe):
        rv = maybe
        if type(maybe) in [tuple, list, pd.core.indexes.base.Index]:
            rv = ", ".join(maybe)
        return rv

    line1 = f"CREATE TABLE IF NOT EXISTS {table} ("
    line2 = lc(columns)
    line3 = f"PRIMARY KEY ({lc(composite_keys)})) WITHOUT ROWID"
    stmt = f"{line1}{line2}, {line3};"
    with closing(sqlite3.connect(f"{db}")) as conn:
        conn.execute(stmt)
    return stmt


def pk_inserter(db, table, df_lot):
    """Insert DataFrame or list of tuples into SQLite table row-by-row.
    Useful when using composite primary key to prevent duplicates.
    Use after pk_compositor makes table and in place of df.to_sql().
    Skips duplicates on try/except rather than attempting Update."""

    rv = True
    if type(df_lot) == pd.core.frame.DataFrame:
        lot = df.to_records(index=False)
    elif type(df_lot) == list and type(df_lot[0]) in [tuple, list]:
        lot = df_lot
    else:
        rv = False
    if rv:
        inserted = 0
        with closing(sqlite3.connect(f"{db}")) as conn:
            for atup in lot:
                stmt = f"INSERT INTO {table} VALUES {atup};"
                try:
                    conn.execute(stmt)
                    conn.commit()
                    inserted += 1
                except:
                    ...
        rv = {"submitted": len(lot), "inserted": inserted}
    return rv


def config2dict(fname):
    """Return a Python dict of a 1-section .ini file."""
    rv = None
    fname = f"config/{fname}"
    if fname[-4:] != ".ini":
        fname = f"{fname}.ini"
    if not Path(fname).is_file():
        print(f"You must make a {fname} config file for this step.")
    else:
        config = configparser.ConfigParser()
        config.read(fname)
        section = config.sections()[0]
        cfg = dict([x for x in config.items(section)])
        rv = cfg
        # for item in cfg:
        #     print(f"{item}: {cfg[item]}")
    return rv


def build_google_search_query(keyword, site=None, num=10):
    """Return a URL that will perform a Google search for given keyword and optional site.
    Useful for scraping Google search results."""

    rv = False
    try:
        base = "https://www.google.com/search?q="
        if site:
            keyword = f"site:{site} {keyword}"
        url = f"{base}{quote_plus(keyword)}"
        if num != 10 and num % 10 == 0:
            url = f"{url}&start={num}"
        rv = url
    except:
        pass
    return url


def extract_serps(text):
    """Return list of Google search results from provided "raw" SERP scrape.
    Useful for checking whether SERPS actually collected or extracting results."""

    rv = False
    try:
        div_pat = re.compile('<div class="yuRUbf">(.*?)</div>')
        divs = re.findall(div_pat, text)
        lot = []
        for div in divs:
            pat_url = re.compile('<a href="(.*?)"')
            url_group = re.match(pat_url, div)
            pat_title = re.compile('<h3 class="LC20lb MBeuO DKV0Md">(.*?)</h3>')
            title_group = re.search(pat_title, div)
            try:
                url = url_group.groups(0)[0]
            except:
                url = ""
            try:
                title = title_group.groups(0)[0]
            except:
                title = ""
            lot.append((url, title))
        rv = lot
    except:
        pass
    return rv


async def chrome(url, headless=False):
    Resp = namedtuple("Resp", "url, text, status_code, headers")
    chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data = r"%userprofile%\AppData\Local\Google\Chrome\User Data"

    browser = await launch(
        autoClose=False,
        headless=headless,
        executablePath=chrome_exe,
        userDataDir=user_data,
        defaultViewport=None,
        slowMo=10,
    )
    # "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    page = await browser.newPage()
    await page.setViewport({"width": 1024, "height": 1024})
    response = await page.goto(url, timeout=500000)
    html = await page.evaluate("document.documentElement.outerHTML", force_expr=True)
    await browser.close()
    rv = False
    if html:
        # rv = Resp(url, html, response.headers["status"], response.headers)
        rv = Resp(url, html, None, None)
    #  if name == "nt" else ...
    return rv


def run_me():
    text = r""" Welcome to _                  (\             To chase the rabbit,
  _ __ ___ | |___  ___  ___     \\_ _/(\      run: look()
 | '_ ` _ \| / __|/ _ \/ _ \      0 0 _\)___
 | | | | | | \__ \  __/ (_) |   =(_T_)=     )*
 |_| |_| |_|_|___/\___|\___/      /"/   (  /
           The adventure begins! <_<_/-<__|"""
    print(text)


def look():
    h2("Psst!")
    h3("Want big ASCII-art like...")
    fig("This?")
    global first_run
    first_run = True
    msg = """Try running: fig("Hello World")"""
    print(SPACES.sub(" ", msg))


def show_globals(docs=False):
    """Print every publlic function and object in global namespace with their
    API signatures. Optionally display their docstrings."""
    label_width = 30
    desc_width = 95
    rtab = Table(title="functions and objects in global()", show_lines=True)
    ct = Theme(
        {
            "func": "bold dim cyan",
            "obj": "bold cyan",
            "doc": "bold dim red",
        }
    )
    rtab.add_column(
        "Object or Function name",
        justify="left",
        style="white",
        no_wrap=False,
        width=label_width,
    )
    if docs:
        rtab.add_column(
            "Docstring (brief description found in function itself)",
            justify="left",
            style="white",
            no_wrap=False,
            width=desc_width,
        )
    else:
        rtab.add_column(
            "Arguments (inputs)", justify="left", style="white", width=desc_width
        )

    fliter_globals = [
        "Table",
        "Console",
        "In",
        "Out",
        "get_ipython",
        "exit",
        "quit",
        "core",
        "is_jupyter",
    ]
    global_publics = [x for x in globals() if x[:1] != "_" and x not in fliter_globals]

    for aglobal in global_publics:
        sig = ""
        obj = eval(aglobal)
        is_obj = False
        try:
            sig = f"[func]FUNCTION ARGS:[/func] {signature(obj)}"
        except:
            sig = f"[obj]OBJECT TYPE:[/obj] {type(obj)}{lr}[obj]OBJECT REPR:[/obj] {repr(obj).replace(bs+bs, bs)}"
            is_obj = True
        if docs:
            doc = getdoc(obj)
            if doc:
                sig = f"{sig}{lr}{lr}[doc]DOCSTRING[/doc]{lr}{doc}"
            else:
                sig = f"{sig}"
        rtab.add_row(aglobal, f"{sig}")

    fig("Welcome to MLSEO")
    h1("Pythonic SEO in JupyterLab")
    msg = """\nThe following is a list of ***functions*** and pre-imported ***packages*** that are
    available to you. **FUNCTION ARGS** means what you put in function parenthesis when you call
    them(args). **OBJECT REPR** is the string representation of an object (you can't really show it).
    These reside in your ***globals()*** as a result of <b>from mlseo import *</b>. If you wish to
    learn more about using them, use: **run_me(docs=True)**\n"""
    if is_jupyter:
        display(Markdown(SPACES.sub(" ", msg)))
    else:
        print(SPACES.sub(" ", msg))
    print()

    table_width = label_width + desc_width
    console = Console(theme=ct, width=table_width)
    # console.print(rtab)


def enlighten_me():
    h1("Congratulations!")
    msg = """You just fetched a webpage from the Internet. It now resides in a variable
    called **response**. To prove to yourself that you have the webpage in computer memory,
    try each of the following commands, ***each on their own Code block***. Output of
    print(response.text) is the HTML of the page and will be very long. You can delete that
    block or hide the output after you've looked at it."""
    display(Markdown(SPACES.sub(" ", msg)))
    print()
    display(
        Markdown(
            """
```python
print(response)
type(response)
dir(response)
print(response.text)

save_me()
```"""
        )
    )
    print()


def save_me():
    h1("Wonderful!")
    msg = """Now let's store the **response** in a database on your drive. Copy this code exactly (watch indenting) into the Code block below."""
    display(Markdown(SPACES.sub(" ", msg)))
    print()
    display(
        Markdown(
            """
```python
from sqlitedict import SqliteDict as sqldict

with sqldict("crawl.db") as db:
    db[url] = response
    db.commit()

please_explain()
```"""
        )
    )
    print()


def please_explain():
    h1("Stay here awhile. Read. Contemplate.")
    msg = """Understanding what's going on above is one of the most important things you
    will do in your Python career. Take your time. Read each point below and really
    try to internalize it. The key things to understand are:"""
    display(Markdown(SPACES.sub(" ", msg)))
    msg2 = """
    1. A package called <a href="https://pypi.org/project/sqlitedict/">sqlitedict</a> has been pip installed on your computer as part of the mlseo dependencies.
    1. During the import, we are ***renaming*** sqlitedict.SqliteDict to just sqldict.
    1. The **db** object is actually the SQLite database ***pretending to be a standard dict***.
    1. The **"with"** keyword means Python **CLOSES** the database on the **out-dent** using the context manager which spares us from looking at some ugly try/finally code.
    1. This has the effect of making the dictionary **PERSISTENT** so we can get the value again without re-crawling the site.
    1. This is often done with Python pickles, but using SQLite is **MUCH** faster.
    1. The **string** contents of the url variable is being used as a dictionary key.
    1. The entire httpx.Response object is being used as a dictionary value.
    1. The changes made to the **db** object must be ***committed*** to the file with db.commit().
    1. Using SQLite for persistent dicts is beyond useful.
    """
    display(Markdown(LINES.sub(" ", msg2)))


if is_jupyter:
    h1("mlseo: Pythonic SEO in JupyterLab")
    h2("To begin: run_me()")