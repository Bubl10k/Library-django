
# Library Web Application

This is a Django-based web application that allows users to manage their personal book collections. Users can create collections, add and remove books, track reading progress, and search for books using an external API. The app also supports user authentication, allowing users to sign up, log in, and have personalized collections and statistics.


## Features

- **User Authentication**: Users can register, log in, and log out securely.
- **Book Collection Management**: Users can create collections, add books, and remove them.
- **Search for Books**: Integrated with Google Books API to search for books by title.
- **Reading Progress Tracking**: Track the number of pages read and status (read, unread) for each book.
- **Favorite Books**: Mark books as favorites to keep track of important reads.
- **CRUD Operations for Collections**: Add, update, and delete book collections.

## Installation

 1. Clone the repository: 

```bash
  git clone https://github.com/Bubl10k/Library-django.git
```

 2. Navigate into the project directory:

 ```bash
  cd ./library
```

 3. Set up a virtual environment and install the dependencies:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```

 4. Run migrations to set up the database:

```bash
  python3 manage.py makemigrations
  python3 manage.py migrate
```

 5. Run redis

 ```bash
 docker pull redis
 docker run -it --rm --name redis -p 6379:6379 redis
 ```

 6. Run the development server:
```bash
  python3 manage.py runserver
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`: Django's secret key for encryption.

`BOOK_API_URL`: The base URL for the external book API.

`BOOK_API_KEY`:  Your API key for the book search service.







