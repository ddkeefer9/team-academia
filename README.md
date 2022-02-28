Academic Assessment Assistant Enhancements Project

To run locally enter "python manage.py runserver" within this folder

"models.py" file in main folder displays current tables within database.
Change Database settings to match your postgres database name go to
"settings.py" within the AcademicAssessmentAssistant folder 

# Release Notes

## 02-28-2022 (Milestone 1)

- SQL dump loaded into PostgreSQL database hosted on Amazon EC2 instance, information to connect is in the settings.py file.
- Models generated from the database in the models.py file.
- Home page displays the first 10 entries in table format of MakereportsSloinreport utilizing the model created in models.py, data is passed through the index function in views.py
- A few test cases have been written to test the URL routing of our existing project. These tests may be ran by typing in the project root directory:
```
pytest
```
