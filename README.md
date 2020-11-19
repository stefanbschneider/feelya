# feelya

✔️😊 feelya: The app that gets you! Keep track of what you eat and do and improve how you feel. 

## Development

Favicon:

* Generate with [favicon generator](https://realfavicongenerator.net/)

## Deployment

### Local

```
# serve
python manage.py runserver

# test
python manage.py test app
```

### Production Deployment on Heroku

Deployment is automatically updated with new pushes to `master`.

Set the following config vars in Heroku (= env vars):

* `DJANGO_SETTINGS_MODULE`: `project.prod_settings`
* `DJANGO_SECRET_KEY`: `<randomly-generated-secret-key>`
* `DATABASE_URL`: URL to Heroku Postgres DB
* `SENDGRID_API_KEY`: `<sendgrid-api-key>`
* `CONTACT_MAIL`: `<email-address-for-receiving-contact-messages>`

For serving static files (e.g., favicon) in production, Ideally uses `whitenoise`.
For deployment, also `Procfile` and `runtime.txt` are relevant.
