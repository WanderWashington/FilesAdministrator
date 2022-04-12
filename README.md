# FilesAdministrator
Project using Django Rest Framework

Developed in Django and Django Rest Framework, this project contains a API.

## Setup 
Import the requirements file:
    ```pip install -r requirements.txt```
    
Set the database on settings file, settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database_name',
        'USER': 'teste',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Run the migrations to apply the database changes:
```python manage.py migrate```

After apply the migrations, we have to create a super user.
```python manage.py createsuperuser```

With a super user created, now is just run the application, running the following command:
```python manage.py runserver```

### Endpoints:

      /admin/
      /api/
      /api/users/
      /api/address/
      /api/fileUpload/
      /api/fileUploadHistory/
      /api/guestUser/ 

### Search parameter:

To search by name of user:

      /api/users/?nome=test
      
To search by users non administrator/guest:

      /users/?guestUsers
      
Just the guestUser endpoint is public. The others are private
