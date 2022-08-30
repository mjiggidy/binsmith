# binsmith

`binsmith` is a command-line python script for creating new Avid bins (`.avb` files).

It can create regular ol' Avid bins with the default settings:
```bash
python3 binsmith.py path/to/new/avid_bin.avb [and/another/bin.avb ...]

```

You can add a `--template path/to/existing/bin.avb` option to use the view settings from an existing bin with your new bins:
```bash
python3 binsmith.py path/to/new/avid_bin.avb and/another/newbin.avb --template path/to/coolbin.avb
```

## Why?

This could be useful for all sorts of weird little post production needs.  For example, batch-creating new bins for a "new project" setup script.

## How does it work?

Well, the most important part of this is the amazing [`pyavb`](https://github.com/markreidvfx/pyavb) library written by Mark Reid.  So this is basically a wrapper for that.

## How to install

* Ensure a reasonably up-to-date python3 environment
* Clone this repo
* Install the dependencies (currently only [`pyavb`](https://github.com/markreidvfx/pyavb)) using the included Requirements file: `pip3 install -r requirements.txt`
* Enjoy
