# praytracing

Python source code for [Peter Shirley's _Ray Tracing in One Weekend_](https://github.com/petershirley/raytracinginoneweekend).
Heavily documented for better understanding (at least for me).

Part of this documentation is having type anotations, in the spirit of the
original C++ code, because I find that it helps bridge the understanding between
a programming and mathematical perspective. To this end, this needs **Python
3.6+** with [mypy](http://mypy-lang.org/) installed (see `requirements.txt`).

To check type consistency (assuming you have mypy in your path---use a
virtualenv!):

    mypy --ignore-missing-imports src/*.py

## PyPy

Given the nature of this repo, this is _notoriously slow_ when ran under 
CPython. I've tried using [PyPy](https://pypy.org/) with this and it works
surprisingly well. The performance gains using PyPy cannot be understated: the
least gain I've seen is being at least twice as fast and on some scripts a gain
of 7x-10x has been observed. Comparing CPython to PyPy is not the main objective
of this repo though, so my benchmarks are quite scant at the moment, and may be
dirty.

Use the PyPy3.6 v7.0.0-alpha release, which should be CPython 3.6-compatible. I
have not yet succeded in installing mypy with PyPy but it parses, and works.
