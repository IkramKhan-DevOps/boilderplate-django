<p align="center">
  <a href="https://exarth.com/">
    <img alt="screen" src="https://github.com/IkramKhan-DevOps/boilderplate-django/blob/main/docs/images/screen.png" height="auto" width="100%">
  </a>
</p>
<hr>

# Django Boilerplate

Welcome to my Django Boilerplate – a comprehensive, reusable starting point for building professional-grade Django applications. This boilerplate is designed to save developers time by providing pre-built functionalities, essential features, reusable components, and configurations commonly required in modern web applications. Whether you're building a small prototype or a large-scale production app, this boilerplate has you covered.

## Table of Contents
1. Applications
2. Tools and Technologies
3. Development Phases
4. Modules
5. Features
6. How to Run
7. Contributing
8. License

## Applications
The boilerplate includes a variety of pre-designed applications to jumpstart your development:

1. Website
2. Administration
3. Staff Management
4. Root Administration

## Tools and Technologies

| Category  | Tools and technologies                        |
| --------- | --------------------------------------------- |
| Frontend  | Html, Css, Javascript, JQuery, Ajax, Jinja    |
| Backend   | Django, Django-Rest-Framework                 |
| Databases | SQLite, PostGre                               |
| Server    | Linux based ubuntu server (aws/digital ocean) |

## Features
The boilerplate comes with a range of features to help you build a robust Django app:

### Authentication and Authorization
- Includes AllAuth and RestAuth for robust authentication.
- Multi-factor authentication (MFA) support.
- Social logins (Google, Apple).

### Notifications
- Firebase push notifications.
- Email notifications.
- In-app notifications.

### Forms and Filters
- Crispy forms for enhanced form styling.
- Advanced filtering capabilities.

### Localization
- Support for multiple languages and localization.

### Documentation
- Integrated Swagger for API documentation.

### Admin and Models
- Pre-built Django required models.
- Updated Django admin interface.
- New admin portal for enhanced management.

### APIs
- Comprehensive API setup with Django Rest Framework.

### Database
- Configured to use PostgreSQL as the database.

## How to Run

### Install

```bash
git clone git@github.com:IkramKhan-DevOps/boilderplate-django.git
cd boilderplate-django
```

### Initialize and Run

```bash
pip install -r requirements.txt
python manage.py makemigrations core accounts whisper
python manage.py migrate
python manage.py runserver
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request with improvements or bug fixes.

1.  Fork the repository.
2.  Create a new branch (git checkout -b feature/your-feature).
3.  Commit your changes (git commit -m "Add your feature").
4.  Push to the branch (git push origin feature/your-feature).
5.  Open a pull request.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

<h4>ALERT !</h4>
<p>Application is developed by <a href="https://github.com/IkramKhan-DevOps/">MARK I</a> at <b><a href="https://exarth.com">Exarth</a></b>.
<small style="color: indianred">( NDA protected )</small>
</p>