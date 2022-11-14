# Prerequisites
- [Python version 3.6+](https://www.python.org/downloads/release/python-3100/)
- [Postgresql](https://www.postgresql.org/download/)
- [Sendgrid account](https://sendgrid.com/)
  

# Clone the project
```bash
git clone https://github.com/kgex/bigbbe
```
# Install [Postgresql](https://www.postgresql.org/download/)
## Initializing postgresql
### For Linux users
#### Step 1: Log into the psql shell
```bash 
sudo -u postgres psql
```
#### Step 2: Change your password
```bash
\password
```
#### Step 3: Create a database
```SQL
CREATE DATABASE bigbbe;
```
#### Step 4: exit using 
```bash
exit
```
### For Windows users
#### Step 1: Press the Windows key and search for "psql"
#### Step 2: Open the shell and hit enter for every prompt you are given
#### Step 3: Change your password using 
```bash
\password
```
#### Step 4: Create your database
```SQL
CREATE DATABASE bigbbe;
```
#### Step 5: Exit using
```bash
exit
```

# Installing the libraries
### Open a terminal inside the bigbbe directory and enter the following command
#### For Ubuntu/linux users
```bash
sudo apt install virtualenv
```
#### Create a virtual environment using the command
```bash
virtualenv env
```
#### Install the libraries
```bash
source env/bin/activate
pip install -r requirements.txt
```
#### For Windows users
```bash
pip install -m virtualenv
```
#### Create a virtual environment and install the requirements
```bash
python -m venv env
./env/Scripts/activate
```
If you get an UnauthorizedAccess error, then open PowerShell in admin mode and type the following command
```Powershell
set Restriction-Policy Unrestricted
```
and rerun the above commands and finally
```bash 
pip install -r requirements.txt
```



# Setting environment variables
## For Debian/Ubuntu users
### Open your bashrc file in your terminal using
```bash
nano ~/.bashrc
```
and add the following lines at the end
```bash
export SQLALCHEMY_DATABASE_URL="postgresql://postgres:password@localhost/bigbbe"
export SENDGRID_API_KEY="<your api key goes here>"
export SENDER_EMAIL="<your authorized sender email address goes here>"
```
and in your terminal
```bash
source ~/.bashrc
```

## For Windows users
### Step 1:Open your search bar using the `Windows` key and search for "Edit environment and system variables" and click on the first option

### Step 2: Click on the Environment Variables button

### Step 3: In the System variables tab, click on new and you will see two input boxes called `Variable name` and `Variable value`

The words on the left hand side of the `=` go in the `Variable name` box and the ones on the right hand side go in the `Variable value` box
```
SQLALCHEMY_DATABASE_URL = postgresql://postgres:password@localhost/bigbbe
SENDGRID_API_KEY = <your api key goes here>
SENDER_EMAIL = <your authorized sender email address goes here>
```


# Database Initial Migrations
## If you have successfully completed the database setup as mentioned above, then we can migrate our models into our database using alembic
#### Step 1: Initialize alembic
```bash
alembic init migrations
```
You should now see a folder called `migrations` and a file called `alembic.ini`
#### Step 2: Edit `sqlalchemy.url` the alembic.ini file and add the following string 
```
postgresql://postgres:password@localhost/bigbbe
```
You need to replace `password` with the password you entered changed to using `\password`.
#### Keep this string stored somewhere accessible outside the project as this string will be used to connect bigbbe to your local database 

#### Step 3: Inside your `migrations` folder, open the `env.py` and replace the line `target.metadata=None` To
```Python
import app.models as models
target.metadata = models.Base.metadata
``` 
#### Step 4: Migrate your models by opening your terminal inside the root directory of bigbbe and enter the commands
```bash
alembic revision --autogenerate -m "msg"
alembic upgrade head
```
Now the database has been setup completely.


# Running the app
To run the app, first the virtual env must be activated

## For windows
```Powershell
./env/Scripts/activate
```
## For Linux
```bash
source env/bin/activate
```

and when your env has been activated, you can run the app using the following command
```bash
uvicorn app.main:app --reload
```

# Migrations
When you make any changes to the models and want to see them reflected on your database, you can use the following commands
```bash
alembic revision --autogenerate -m "msg"
alembic upgrade head
```