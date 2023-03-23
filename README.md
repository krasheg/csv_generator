# CSV Generator

CSV Generator is a web application that allows users to create datasets with fake data by defining custom data schemas. The application supports 6 different types of data, such as Full name, Job, Email, Company name, Integer, and Address.

## Getting Started
To get started, you'll need to have the following installed:

Python 3
Django 3
Git
First, clone this repository using Git:


Copy code
`git clone https://github.com/krasheg/csv_generator.git`
Next, navigate into the project directory and install the Python dependencies:


Copy code
`cd csv_generator`
`pip install -r requirements.txt`
Finally, start the Django development server:

Copy code
`python manage.py runserver`
You should now be able to access the application by navigating to `http://localhost:8000/`in your web browser.

### Usage
Once logged in, any user can create any number of data schemas to create datasets with faked data. Each data schema has a name and a list of columns with names and specified data types. Users can build the data schema with any number of columns of any type described above. Some types support extra arguments, such as a range, while others do not. Each column also has its name (which will be a column header in the CSV file) and order (just a number to manage column order).

After creating the schema, users should be able to input the number of records they need to generate and press the "Generate" button. When the CSV file of the specified structure is ready, the file saved to the "media" directory.

The interface shows a colored label of generation status for each dataset (e.g., in progress, completed, or failed).
