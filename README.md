# kmsi (Keyboard MSI)

This module, coming with a script, will illuminate your MSI keyboard, if supported.

## Dependancies

- [cython-hidapi][https://github.com/trezor/cython-hidapi] (compatible python3 except for the try.py script)
- python 3.3 or above

## Build it from source

1. Download it:
```
$ git clone https://github.com/ElricleNecro/kmsi.git
```

2. Build the module:
```
$ python3 setup.py build
```

3. Install it:
```
$ sudo python3 setup.py install
```

4. Execute the kmsi script:
```
$ sudo kmsi
```

Use `kmsi --help` to get more information about the options.

**Note**: You can add the `--user` option, but root right will still be needed to execute the script.
