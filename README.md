# Ce zicea legea - API

[![GitHub contributors](https://img.shields.io/github/contributors/code4romania/czl-api.svg?style=for-the-badge)](https://github.com/code4romania/czl-api/graphs/contributors) [![GitHub last commit](https://img.shields.io/github/last-commit/code4romania/czl-api.svg?style=for-the-badge)](https://github.com/code4romania/czl-api/commits/master) [![License: MPL 2.0](https://img.shields.io/badge/license-MPL%202.0-brightgreen.svg?style=for-the-badge)](https://opensource.org/licenses/MPL-2.0)

* LAWMAKING TRACKED  EVERY STEP OF THE WAY
* centralized information helps people stay informed
* automatization can help citizens track and monitor legal initiatives
* making a closed and complex environment accessible to all
* increasing accountability among legislators

[See the project live](https://czl-web.surge.sh/)

With dozens of institutions involved in the process and incomplete information fragmented across a myriad of websites, it is almost impossible
for a regular citizen to follow the long process by which a proposal becomes law.

In these circumstances it is almost impossible to speak of active engagement in the legislative drafting process on the part of the citizens.

Right now people and entities interested in tracking legislation initiatives have to visit over 29 websites daily for updates. This places a large burden on legal
professionals, civil society actors and private corporations which are investing time and resources daily to stay up to date with legislation
initiatives. Once CeZiceLegea will be launched these costs will be reduced substantially.

CeZiceLegea aims to keep citizens informed at any time about changes in legislation and make them active participants in the legislative drafting process. Users will be able to track and
monitor proposed legislation through all the approval stages and be notified of the changes made.

As an extra feature, to give a sense of the wider context, CeZiceLegea will also allow access to current consolidated legislation.

[Built with](#built-with) | [Repos and projects](#repos-and-projects) | [Deployment](#deployment) | [Contributing](#contributing) | [Feedback](#feedback) | [License](#license) | [About Code4Ro](#about-code4ro)

## Built With

- Python 3
- Django 1.10.6

## Deployment

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
```

### To run the project as a WSGI app:

- make sure PYTHONPATH includes `<deploydir>/repo` (or chdir to it),
- use the virtualenv,
- and use `[<deploydir>/repo/]czl/base/wsgi.py` as the WSGI application file.

### Web server configuration:

In production you should set `STATIC_ROOT` appropriately in settings,
and serve the static files via the web server.

```shell
./manage.py collectstatic
```

### To run the development server:

```shell
cd <deploydir>
. venv/bin/activate
cd repo
./manage.py runserver
```

### Token generation:

You can generate tokens using the admin interface. To do so, create a superuser:

```shell
./manage.py createsuperuser
```

then, using your browser visit the admin interface and (optionally) create
a regular user under `/admin/auth/user/add/` and a token under
`/admin/authtoken/token/add/`.

## Repos and projects

Related projects:
- https://github.com/code4romania/czl-scrape - scrapers
- https://github.com/code4romania/czl-web - web UI

## Contributing

If you would like to contribute to one of our repositories, first identify the scale of what you would like to contribute. If it is small (grammar/spelling or a bug fix) feel free to start working on a fix. If you are submitting a feature or substantial code contribution, please discuss it with the team and ensure it follows the product roadmap.

* Fork it (https://github.com/code4romania/czl-api/fork)
* Create your feature branch (git checkout -b feature/fooBar)
* Commit your changes (git commit -am 'Add some fooBar')
* Push to the branch (git push origin feature/fooBar)
* Create a new Pull Request

[Pending issues](https://github.com/code4romania/czl-api/issues)

## Feedback

* Request a new feature on GitHub.
* Vote for popular feature requests.
* File a bug in GitHub Issues.
* Email us with other feedback contact@code4.ro

## License

This project is licensed under the MPL 2.0 License - see the [LICENSE](LICENSE) file for details

## About Code4Ro

Started in 2016, Code for Romania is a civic tech NGO, official member of the Code for All network. We have a community of over 500 volunteers (developers, ux/ui, communications, data scientists, graphic designers, devops, it security and more) who work pro-bono for developing digital solutions to solve social problems. #techforsocialgood. If you want to learn more details about our projects [visit our site](https://www.code4.ro/en/) or if you want to talk to one of our staff members, please e-mail us at contact@code4.ro.

Last, but not least, we rely on donations to ensure the infrastructure, logistics and management of our community that is widely spread accross 11 timezones, coding for social change to make Romania and the world a better place. If you want to support us, [you can do it here](https://code4.ro/en/donate/).
