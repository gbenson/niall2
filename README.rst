Niall2
======

Niall2 is a simple chatbot that collects statistics on sentences you
type and tries to construct meaningful replies.  The original Niall
was an Amiga program I liked, and spent a lot of time tweaking and
reimplementing in the 1990s.  I initially wrote this version in
Python in under an hour, from memory, to explain how ChatGPT works
to my daughter.


Local setup
-----------

Clone the repo::

 git clone https://github.com/gbenson/niall2.git
 cd niall2

Create a virtual environment::

 python3 -m venv venv
 . venv/bin/activate

Upgrade pip and setuptools::

 pip install --upgrade pip setuptools

Install in editable mode::

 pip install -e .[dev]

Test it::

 pytest
