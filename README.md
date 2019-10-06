<center>
    <img src="logo/bookworm.png" width="100%" />
</center>

[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/OmkarPathak/Django-Bookworm/blob/master/LICENSE) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg) [![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-:D-1EAEDB.svg)](https://saythanks.io/to/OmkarPathak)

# Django-Bookworm
 Love reading books, Have problem remembers main points from book like me? this is a fun project to store learning from each book.

# Features
- Easy to use GUI
- Chapter-wise bifurcation
- Generate summary from whatever your learning from each chapter are
- Get basic statistics about the books you read
- Get inspirational quotes on your homepage

# Installation

- Download or clone this repository
- Change directory to the recently cloned repository folder or unziped folder
- Run the following command to install dependencies:
    ```bash
    $pip install -r requirements.txt
    ```
- For summarization Python `nltk` is used. To download required files, execute:
    ```bash
    python prerequisites.py
    ```
- Then create a file named `.env` inside `django_bookworm/` and add following details with your details
    ```
    SECRET_KEY=<your_secret_key>
    ```
- Now, you can start the django server by executing following commands:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

# Working

![Working](result.gif)

# Special Mentions

- Special thanks to [@reallinfo](https://github.com/reallinfo) for the beautiful and thoughtful logo :smile:
