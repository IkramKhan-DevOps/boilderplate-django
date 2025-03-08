
## TEST CREDENTIALS
### EMAIL SMTP
**EMAIL_HOST_USER**=donald.duck0762@gmail.com                           <br>
**EMAIL_HOST_PASSWORD**=cikghsgphicaptqj
### STRIPE
**STRIPE_PUBLIC_KEY**=pk_test_51KNUx8GWh1G1v77h4cAKDbEvH3wEbK4yVZfSGKT5f5wgShK8cipV0ctpNrZ2tqt63fsVmJp4s>  <br>
**STRIPE_SECRET_KEY**=sk_test_51KNUx8GWh1G1v77hDR40VBVDDZTK2pgUZMk0yxDyN4evl4lBg2LyxFyOQCDoLQWhgy1t9bAzc>  <br>
**STRIPE_WEBHOOK_SECRET**=whsec_1d8d3fe0a2aa5e4636cd1343c86fdc72d962593725e8d3a4ab8ad122b8522893

## COMMANDS
### PYTHON
````shell
virtualenv env
env/Scripts/activate
source env/bin/activate
pip install -r requirements.txt
pip install package
pip uninstall package
pip freeze
````
### DJANGO
````shell
django-admin startproject projectname
django-admin startapp appname
python manage.py makemigrtions
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py runserver
````
### STRIPE
````shell
stripe login
stripe listen --forward-to 127.0.0.1:8000/url/webhook/
````
### GIT
````shell
git init
git remote add origin github_repository
git config --global user.name github_username
git config --global user.email github_email
git clone github_repository
git status
git log
git branch
git checkout -b branch_name
git add .
git commit -m "commit_message"
git push
````

### ENDPOINTS
[https://127.0.0.1:8000/admin/](https://127.0.0.1:8000/admin/)                <br>
[https://127.0.0.1:8000/api/](https://127.0.0.1:8000/api/)                    <br>
[https://127.0.0.1:8000/accounts/login/](https://127.0.0.1:8000/accounts/login)

## MIGRATIONS
make sure to follow this migrations order.
1. core
2. accounts
3. ...

## MISSING
accounts templates are missing
