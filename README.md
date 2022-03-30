# mlseo
> Pythonic SEO in JupyterLab


<a href="https://github.com/jupyterlab/jupyterlab-desktop">JupyterLab</a> standalone version is your "platform". Python is your framework. Pandas and Sqlite are your database. This package just adds some SEO functions and inspiration. Feel free to pip install it, but clone it from Github if you want the example Notebooks.

## Install

`pip install mlseo`

## How to use

Start a new Notebook, preferably in standalone JupyterLab. Then type:

    from mlseo import *
    
Then follow the instructions.

# Bonus Feature

mlseo is designed to be used in stand-alone JupyterLab. As such, you have to reconfigure it every time you reinstall/update. That's a pain. The biggest pain is putting your keyboard shortcuts back in. Here's mine:

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
