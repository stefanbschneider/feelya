from setuptools import setup, find_packages


requirements = [
    'django>=3.1.2',
    'django-registration>=3.1.1',
    'django-crispy-forms>=1.9.2',
    'gunicorn>=20.0.4',
    'dj-database-url>=0.5.0',
    'psycopg2-binary>=2.8.6',
    'django-pwa>=1.0.10',
    'whitenoise>=5.2.0',
]

setup(
    name='feelya',
    author='Stefan Schneider',
    version=1.0,
    description="FeelYa: The app that gets you! Keep track of what you eat and do and improve how you feel.",
    url='https://feelya-app.herokuapp.com/',
    find_packages=find_packages(),
    python_requires=">=3.8.*",
    install_requires=requirements,
    zip_safe=False
)
