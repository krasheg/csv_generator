# csv_generator
The application allows any user to log in using a username `admin` and password `admin`. 

Once logged in, any user can create any number of data schemas to create datasets with faked data. Each data schema has a name and a list of columns with names and specified data types. The application supports 6 different types of data, such as Full name (a combination of first name and last name), Job, Email,  Company name, Integer (with specified range), Address.

Users can build the data schema with any number of columns of any type described above. Some types support extra arguments, such as a range, while others do not. Each column also has its name (which will be a column header in the CSV file) and order (just a number to manage column order).

After creating the schema, users should be able to input the number of records they need to generate and press the "Generate" button. When the CSV file of the specified structure is ready, the file saved to the "media" directory.

The interface shows a colored label of generation status for each dataset (e.g., in progress, completed, or failed).
