# Linecount

Count nonblank lines in UTF-8 files without opening an editor. For developers checking generated text and small exports.

Requires Python 3.10 or later. No external dependencies, account or network access.

## Try it

Download `linecount.py` from this repository, then:

```sh
printf 'first\n\nsecond\n' > sample.txt
python3 linecount.py sample.txt
```

Expected output: `2`. Input files are not modified. Binary files are unsupported; files are read into memory, so use another tool for multi-gigabyte inputs.

MIT licence: [terms](LICENSE). Report reproducible problems through repository issues. This is a small volunteer-maintained utility with no response-time commitment.
