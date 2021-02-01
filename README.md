## Task Description
Write a Todo app. Each task has a name, description, and expiration date. You need to send a reminder email to the user 10 minutes before the expiration date. It is recommended that you use the celery task to send emails asynchronously. You are free to use rabbitmq or redis as a celery broker.

By default, tasks are only visible to the user who created them, not to other users. However, the user can share the task with another user by typing his username or email address. In this case, sharing in 2 formats is possible not only to see the draft, or the ability to see and write comments. On the details page of the task, comments are written in real time with a socket, ie written comments should appear instantly on the opposite side (django channels recommended).

Select postgresql as the database. Serve the application with a docker (docker-compose).

- If possible, try to store comments in a separate DB, not in the main DB. (django multi-database feature)
- If possible, the author of the task should be able to delete the comments written to the file.
- If possible, the author of the comment should be able to both delete and edit his comment.

## Installation
- Open a command line window and go to the project's directory.

- `pip install -r requirements.txt`

Build and run the Docker images.
```sh
$ docker-compose up --build -d
$ docker-cleanup
```