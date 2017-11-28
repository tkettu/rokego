# Rokego

Web-app for tracking endurance sports (running, cycling, skiing...). Excel-stylish tables, visualisations based for time-distance and weekly,
monthly (yearly) stats for different sports.

## Setup
Clone and setup Rokego at local machine
```
~/path/to$ git clone https://github.com/tkettu/rokego
~/path/to$ cd rokego
~/path/to/rokego$ python3 -m venv ll_env 
~/path/to/rokego$ source ll_env/bin/activate
~/path/to/rokego$ pip install -r requirements.txt
```

### Local settings
Make file ```local_settings.py``` to same folder as settings.py

```python
from .settings import *

SECRET_KEY = 'SomeSecretKey'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Database
Initialize database
```
~/path/to/rokego$ python manage.py makemigrations
~/path/to/rokego$ python manage.py migrate
```
And run on localhost to verify that everything works.
```
~/path/to/rokego$ python manage.py runserver
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
