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
4. In order for things to function correctly, set the environment variable **DJANGO_SETTINGS_MODULE** to `SPPM.settings.local`
5. Run `pip install -r pip-requirements/local.txt` to install all the Python/Django requirements.
   1. Be mindful in the future that when you `git pull`, you will want to update the requirements by running the above command again.
6. Run the [makemigrations](https://docs.djangoproject.com/en/dev/ref/django-admin/#makemigrations) management command in case any of the newly installed requirements has any to create.
   1. Any time the requirements are updated, you should attempt to run this command again, and `migrate` if there were any new migrations found.
7. Run the [migrate](https://docs.djangoproject.com/en/dev/ref/django-admin/#migrate) management command to create the tables/columns in your database.
8. Run the `create_game_instances` management command to create the Game objects.
9. Run the `create_test_user` management command to a few base Users.
    1. Arguments for the command are:
       1. **username** - The username of the Super User.
       2. **password** - The password to use for the User.
       3. **forum_id** - The user id from the Source.Python forums.
    2. You will want to create at least 1 superuser
       1. For this you will want to use the `--is_superuser` and `--is_staff` flags.
       2. `create_test_user <username> <password> <forum_id> --is_superuser --is_staff`
    3. You will want to create a couple non-superusers, as well, that are not randomly named.
10. If you want additional users to test with, run the `create_random_users` management command.
    1. Arguments for the command are:
       1. **count** - The number of random Users to create.
11. Run the server using the [runserver](https://docs.djangoproject.com/en/dev/ref/django-admin/#runserver) management command.
    1. Some IDEs, like Pycharm, have tools to run the server instead of manually running the command in a console window.

## Authentication (logging in)
You can log in one of two ways.

1. The Django Admin can be used to log in your Super User you created above.
2. A simple login page is available (local only) via the `/accounts/login` page.

Either way will allow you to login and view/utilize all the APIs except for the Django Admin. Certain APIs require you to be logged in, whether as a regular user or a Super User.

## APIs
### Walkable REST APIs
The REST APIs that the frontend will eventually be built off of can be found at `/api`. They are walkable, meaning the APIs are laid out before you on each page, so just click a link to navigate to another API. Some will require you to add a Project name to the URL path.

Each REST API should also show a list of filters and ordering fields, along with examples.

GET calls do not require the user to be logged in.
POST calls require the user to be logged in.
PATCH and DELETE calls require the user to be logged in, as well as be either the owner or a contributor for the Project (ie package/plugin/sub-plugin contributor).
DELETE cannot be called on Projects themselves, just on the associated models.

#### Games
`/api/games`
* displays the existing games along with their slug and icon
* allows for GET

#### Packages
`/api/packages/projects`
* displays all Packages
* allows for GET, POST, and PATCH
* POST not only requires base information for the &lt;package&gt;, but also information for the first release (ie notes, version, and zip file).
* PATCH requires the package to be added to the URL path (ie `/api/packages/packages/<package>`)

`/api/packages/contributors/<package>`
* displays the contributors for the given &lt;package&gt;.
* allows for GET, POST, and DELETE
* POST and DELETE can only be executed by the owner of the Project
* DELETE requires the id to be added to the URL path (ie `/api/packages/contributors/<package>/<package contributor id>`)

`/api/packages/games/<package>`
* displays all associated games for the given &lt;package&gt;.
* allows for GET, POST, and DELETE
* DELETE requires the id to be added to the URL path (ie `/api/packages/games/<package>/<package game id>`)

`/api/packages/images/<package>`
* displays all images for the given &lt;package&gt;.
* allows for GET, POST, and DELETE
* DELETE requires the id to be added to the URL path (ie `/api/packages/images/<package>/<package image id>`)

`/api/packages/releases/<package>`
* displays all releases for the given &lt;package&gt;.
* allows for GET and POST
* you cannot currently PATCH or DELETE a release, though the Django Admin does allow for it if a User happens to make a mistake.

`/api/packages/tags/<package>`
* displays all images for the given &lt;package&gt;.
* allows for GET, POST, and DELETE
* DELETE requires the id to be added to the URL path (ie `/api/packages/tags/<package>/<package tag id>`)

#### Plugins
* All the same APIs for [Packages](#packages) exist for Plugins (using `plugins` and `<plugin>` in place of `packages` and `<package>`) with the following addition.

`/api/plugins/paths/<plugin>`
* displays the Sub-Plugin paths allowed for the given &lt;plugin&gt;. For instance, [GunGame](https://github.com/GunGame-Dev-Team/GunGame-SP) allows for custom Sub-Plugins but requires them to be located in the `../plugins/custom` directory and include a file as `<sub-plugin>/<sub-plugin>.py`.
* For example: `../plugins/custom/gg_assists/gg_assists.py`
* allows for GET, POST, PATCH, and DELETE

#### Sub-Plugins
* All the same APIs for [Packages](#packages) exist for Sub-Plugins, though they require the `<plugin>` which they are associated as well as the `<sub-plugin>`.
* For example: `/api/sub-plugins/contributors/<plugin>/<sub-plugin>`

#### Tags
`/api/tags`
* displays all created tags
* tags are created via the `Project Tag` APIs listed above for `Packages`, `Plugins`, and `Sub-Plugins`.
* allows for GET
* tags can be black-listed by an Admin/Super User in the Django Admin. due to the black-listing, tags should not be deleted.

#### Users
  `/api/users`
* displays all created users
* allows for GET

### Admin
Since you have created a Super User, you should be able to log into `/admin` using your username/password. This will allow you to test the Django Admin functionality if you are working on it.

### Statistics
There is also a `/statistics` page to display certain statistics for your local environment from a project, user, and download perspective.

### User Frontend
Eventually we will be adding `/plugins` and `/packages`, as well as `/plugins/<plugin>/sub-plugins` for a frontend User experience. These all still need built, so if you have Javascript experience and are willing to help out, it would be much appreciated. The first obstacle will be to determine which Javascript framework to use. This really depends on what people know, but Vue or React would be preferred.

## Testing

### Unit Testing
To run the Django test suite, run `pytest`. The output will show you any tests that are failing. It will also show you a list of warnings, which will help with deprecated functionalities that may need updated in the future.

`pytest` also creates a coverage report that can be found at `htmlcov/index.html`. This report shows where there are gaps in the coverage.

### Linting
To run the linters, run `prospector`. The output will tell you where there are coding standards violations that need fixed.
