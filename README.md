# binsmith

`binsmith` is a command-line python script for creating new Avid bins (`.avb` files).

It can create regular ol' Avid bins with the default settings:
```bash
python3 binsmith.py my_new_bin.avb [another_new_bin.avb ...]

```

You can add a `--template path/to/existing/bin.avb` option to use the view settings from an existing bin with your new bins:
```bash
python3 binsmith.py my_new_bin.avb another_new_bin.avb --template path/to/coolbin.avb
```

Get *really* fancy with a bash for loop:
```bash
for x in {1..8}; do
  python3 binsmith.py "To Sound/Reel ${x} v12.avb" --template binviews/TurnoverView.avb;
done;
```

That'll get you 8 bins with whatever display settings are set in your `TurnoverView.avb` bin.

## Why?

This could be useful for all sorts of weird little post production needs.  For example, batch-creating new bins for a "new project" setup script, or as part of a dailies ingest workflow.  Or just for one-off bins because... I don't know about you, but *my* Avid takes *forever* to make a new bin the normal way.

## How does it work?

Well, the most important part of this is the amazing [`pyavb`](https://github.com/markreidvfx/pyavb) library written by Mark Reid.  So this is basically a wrapper for that.

## How to install

* Ensure a reasonably up-to-date python3 environment
* Clone this repo
* Install the dependencies using the included Requirements file: `pip3 install -r requirements.txt`
* Enjoy

## You may also like

* [`binlock`](https://github.com/mjiggidy/binlock) - Create lock files for Avid bins, with custom messages and an air of mystique
