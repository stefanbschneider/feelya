**Status:** Prototype finished. Bug fixes or minor new features may still be added.

**Live demo:** [Heroku](https://feelya-app.herokuapp.com/)

# FeelYa

✔️😊 FeelYa: The app that gets you! Keep track of what you eat and do and improve how you feel. 

FeelYa is a simple progressive web app (PWA) that helps you keep track of what you do and understand what makes you feel good.

* Simply keep track of whatever is relevant to you: Food, sport, work, other activities - and how you feel.
* Add the same entry multiple times to indicate a larger quantity, e.g., more food/sport/stress/...
* Visualize your most common entries within a custom time frame
* Analyze your entires over time to identify what has a positive impact and what has a negative impact
* Use anywhere: Responsive design and secured via password

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
