# SimpleZstd

This library provides simple Pythonic interface of [`zstd`](https://facebook.github.io/zstd/) algorithm like Python's builtin `gzip` library, by wrapping the [`zstandard`](https://github.com/indygreg/python-zstandard) library.

Further more, it provides builtin session support to take advantage of `zstd`'s powerful training mode without additional user effort, by auto collecting training samples (10 by default) during compression/decompression.

``` python
In [1]: c = open("poetry.lock").read().encode("utf-8")

In [2]: len(c)
Out[2]: 73946

In [3]: from simple_zstd import compress, decompress

In [4]: for i in range(10):
   ...:     x = compress(c)
   ...:     print(len(x), len(x) / len(c))
   ...:     assert decompress(x) == c
   ...:
22259 0.3010169583209369
22259 0.3010169583209369
22259 0.3010169583209369
22259 0.3010169583209369
22259 0.3010169583209369
7123 0.09632704946853109
7123 0.09632704946853109
7123 0.09632704946853109
7123 0.09632704946853109
7123 0.09632704946853109
```

Note that user can also choose to have dedicated session instead of default one.

``` python
In [1]: c = open("poetry.lock").read().encode("utf-8")

In [2]: from simple_zstd import Session

In [3]: session = Session()

In [4]: x = session.compress(c)

In [5]: assert session.decompress(x) == c
```

For simpler usage, you can also just import `zstd` instead of `simple_zstd`.
