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

 pip install -e .

Run it::

 python niall2.py


Data store setup
----------------

1. Go to https://cloud.dgraph.io/
2. Create an account if necessary
3. Click "Launch new backend"
4. Select the "Free" option
5. From the sidebar, select "Schema"
6. Enter this in the "GraphQL schema" tab:
::

  type Word  {
    text: String! @id
  }
  type Transition {
    from: Word
    to: Word
    count: Int!
  }

7. Click "Deploy"
8. Copy your "GraphQL endpoint" URL from the XXX screen, and save it
   in a file called ``.datastore`` in the same directory as ``datastore.py``:
::

  echo "https://hot-shoes-186283.us-east-1.aws.cloud.dgraph.io/graphql" > .datastore

9. Run it:
::

  python datastore.py
