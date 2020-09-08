# Research files

Some files used to research the spec.

I use this command on Linux to diff the two logbook files in this directory:

```
colordiff --width 200 -y <(xxd -g1 kh_logbook_1) <(xxd -g1 kh_logbook_2) | less -R
```

> Note that it requires `colordiff`, which can be installed with `apt-get install colordiff`

