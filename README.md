# Simple Issue Tracker

#### Dependency Installation :
```
pip install -r requirement.txt
```
#### Project Structure :
```
issue-tracker/
    models/
      __init__.py
      issue.py
      user.py
    new_celery/
      __init__.py
      celery.py
      email.py
      tasks.py
    resources/
      __init__.py
      issue.py
      user.py
    api.py
    db.py
    security.py
    logger.py
    error.log
```


## Getting Started

#### Install depencencies :
```
pip install -r requirement.txt

Also add the Email address & pass word for mail Server at
/new_celery/email.py
```
#### Start Redis Server :
```
sudo service redis-server start
```
#### Start Celery
```
cd issue-tracker/
celery -A new_celery worker --loglevel=debug
```
#### Start Flask App
```
cd issue-tracker/
python api.py
```

## API

* ##### POST localhost:8080/register
    - Registers users with the given data format on the System
    ```
    {
      "email" : "user@email.com",
      "username" : "someUsername",
      "password" : "userpassword",
      "first_name" : "John",
      "last_name" : "Doe"
    }
    ```

* #### POST localhost:8000/authenticate
  - authenticate user with the following data format to issue the access_token
  ```
  {"username":"someUsername", "password":"userpassword"}
  ```
* #### GET localhost:8000/issue/<issue_id>
  - Returns the details of the <issue_id>
  - This request requires JWT access_token acquired via /authenticate
  ```
  Headers Needed :
  Authorization : JWT <access_token>
  ```
* #### POST localhost:8000/issue/
  - Request to create the issue with the following body
   ```
   {
    "title" : "New Issue Title",
    "description" : "Some Description",
    "author" : "creator@email.com",
    "assigned_to" : "assignee@email.com"
  }
   ```
  - The access_token must belong to the creator

* #### DELETE localhost:8000/issue/<issue_id>
  - The creator of an issue can delete the issue via the issue id

* #### PUT localhost:8000/issue/<issue_id>
  - The creator of an issue can alter the issue contents with the following body data
  ```
  { "title" : "New Title",
  "description" : "Some Description",
  "assigned_to" : "new_assignee@email.com",
  "status" : "CLOSE"
  }
  ```

On creation of an issue the assigned user will get an email after 12 mins with the details of the Issue assigned.
Also on updation of a Issue the assigned user will get an email with the details.

**The 24 hrs Scheduled email has not been Implemeted !**
**Along with the cancellation of task from Broker if a user is relieved of the issue while updation of Issue **

Updated with a Logger. Log statements will be saved at error.log

## Built With

* **Python 2.7**
* **Flask 1.0.2**
* **celery 3.1.25**

## Author

* [Sameer Barha](maitto:sameer.barha12@gmail.com)
