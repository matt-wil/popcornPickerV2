# popcornPickerV2

A web application for saving and displaying your favorite movies.

## Installation

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/matt-wil/popcornPickerV2.git
cd popcornPickerV2
```

## Usage

Before running the application, you need to set up the movie database.

### Setting up the Database

You have two options for creating the database:

**Option 1: Create an empty database**

1.  Create a directory named `instance` in the project's root folder.
2.  Inside the `instance` directory, create an empty file named `movies.db`.

**Option 2: Seed the database with sample movies**

1.  Open the `app.py` file.
2.  Locate the `if __name__ == '__main__':` block at the end of the file.
3.  Uncomment the lines that add movies to the database. You can customize the movie details as you see fit.
4.  Run the application once to populate the `movies.db` file.
5.  **Important:** After the database is created, comment out the lines you previously uncommented. This will prevent duplicate movies from being added every time you start the application.

### Running the Application

1.  Execute the `app.py` file:
    ```bash
    python app.py
    ```
2.  Open your web browser and go to the local server address displayed in your terminal (e.g., `http://127.0.0.1:5000`).