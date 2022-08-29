`binsmith` is a command-line python script for creating new Avid bins (`.avb` files).

It can create regular ol' Avid bins with the default settings:
```bash
python3 binsmith.py path/to/new/avid_bin.avb [and/another/bin.avb ...]

```

*...or*, you can add a `--template path/to/existing/bin.avb` option to copy the view settings from an existing bin:
```bash
python3 binsmith.py path/to/new/avid_bin.avb and/another/newbin.avb --template path/to/coolbin.avb
```

## How does it work?

Well, the most important part of this is the amazing [`pyavb`](https://github.com/markreidvfx/pyavb) library written by Mark Reid.  So this is basically a wrapper for that.

## What's next?

I don't want to get too fancy, but I plan to add the ability to set a default bin view.
