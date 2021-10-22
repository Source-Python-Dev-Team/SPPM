# Source.Python Project Manager

This Django app will be used to host Source.Python plugins, sub-plugins, and custom packages.

## Want to help develop this application?

If you wish to contribute to this application, follow the instructions below on how to set it up locally.

### Local setup
1. Clone the repository
2. Create a virtual environment
   1. Some IDEs, like Pycharm, come with tools to automatically create the virtual environment.
   2. If you have to set it up yourself, there are plenty of online guides to help you.
   3. We may Docker-ize the app in the future, which will make this a little simpler, but will require you to install/run Docker.
3. Log into your virtual environment to complete the rest of these steps.
4. Run `pip install -r pip-requirements/local.txt` to install all the Python/Django requirements.
5. Run the [migrate](https://docs.djangoproject.com/en/dev/ref/django-admin/#migrate) management command to create the tables/columns in your database.
6. Run the `create_game_instances` management command to create the Game objects.
7. Run the [createsuperuser](https://docs.djangoproject.com/en/dev/ref/django-admin/#createsuperuser) management command to create your main user.
8. Run the `associate_super_user` management command to associate the Super User you just created with a ForumUser object.
   1. Arguments for the command are:
      1. **username** - The username of the Super User
      2. **forum_id** - The user id from the Source.Python forums.
9. If you want additional users to test with, run the `create_random_users` management command.
   1. Arguments for the command are:
      1. **count** - The number of random Users to create.
10. Run the server using the [runserver](https://docs.djangoproject.com/en/dev/ref/django-admin/#runserver) management command.
    1. Some IDEs, like Pycharm, have tools to run the server instead of manually running the command in a console window.

## APIs
### Walkable REST APIs
The REST APIs that the frontend will eventually be built off of can be found at `/api`. They are walkable, meaning the APIs are laid out before you on each page, so just click a link to navigate to another API. Some will require you to add a project name to the URL path.

### Admin
Since you have created a Super User, you should be able to log into `/admin` using your username/password. This will allow you to test the Django Admin functionality if you are working on it.

### Statistics
There is also a `/statistics` page to display certain statistics for your local environment from a project, user, and download perspective.

### User Frontend
Eventually we will be adding `/plugins` and `/packages`, as well as `/plugins/<plugin>/sub-plugins` for a frontend User experience. These all still need built, so if you have Javascript experience and are willing to help out, it would be much appreciated. The first obstacle will be to determine which Javascript framework to use. This really depends on what people know, but Vue or React would be preferred.
