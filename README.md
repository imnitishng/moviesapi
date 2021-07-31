
# Movies API 

The project is meant to demonstrate standard CRUD operation for a movies API.
Project developed using TDD approach and follows standard rules for creating APIs with proper HTTP success and error codes and data handling, validation using serializers.


[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/imnitishng/moviesapi)

## Run Locally

Clone the project

```bash
  git clone https://github.com/imnitishng/moviesapi
```

Go to the project directory

```bash
  cd moviesapi
```

Make python virtual environment

```bash
  mkdir venv && python3 -m venv ./venv
```

Activate virtual environment and install dependencies

```bash
  pip install -r requirements.txt
```

Make migrations and run server

```bash
  python manage.py makemigrations && python manage.py migrate 
  python manage.py runserver
```

## Running Tests

To run tests, run the following command

```bash
  python manage.py test
```

  
## API Reference

#### Get all movies 

```http
  GET /api/movies
```

#### Get a movie of the specified ID

```http
  GET /api/movies/<movie_id>
```

#### Delete a movie of the specified ID

```http
  DELETE /api/movies/<movie_id>
```


#### Edit an already existing movie of the specified ID

```http
  PUT /api/movies/<movie_id>
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Required**. Name of the movie |
| `desc`      | `string` | **Required**. Description of the movie |
| `dor`      | `string` | **Required**. Date of release of the movie [YYYY-MM-DD] |


#### Create a new movie

```http
  POST /api/movies
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Required**. Name of the movie |
| `desc`      | `string` | **Required**. Description of the movie |
| `dor`      | `string` | **Required**. Date of release of the movie [YYYY-MM-DD] |


## Demo
(Open image in new tab for fullscreen)
![App Screenshot](https://user-images.githubusercontent.com/35267629/127738259-3dceecba-fb60-4abd-8269-6464a12346c4.gif)
