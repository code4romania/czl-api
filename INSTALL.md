```shell
createdb <dbname>
echo create extension hstore | psql <dbname>

mkdir <deploydir>
cd <deploydir>
git clone https://github.com/code4romania/czl-api repo

virtualenv --python=python3 venv
. venv/bin/activate
pip install -r repo/requirements.txt

cd repo
cp czl/base/localsettings.py.example czl/base/localsettings.py
# edit localsettings.py as required
./manage.py migrate
./manage.py collectstatic
```

To run the project as a WSGI app:

- make sure PYTHONPATH includes `<deploydir>/repo` (or chdir to it),
- use the virtualenv,
- and use `[<deploydir>/repo/]czl/base/wsgi.py` as the WSGI application file.

To run the development server:

```shell
cd <deploydir>
. venv/bin/activate
cd repo
./manage.py runserver
```
