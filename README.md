Academic Assessment Assistant Enhancements Project
# Project Information
The UNO Academic Assessment Committee coordinates degree program assessment activities aimed at improving the student learning experience in all academic programs across the university. This initiative collects data from academic departments regarding student learning outcomes and the programs' progress towards achieving those outcomes. Each department reports their own set of metrics. A mechanism is needed to further process this data to produce actionable analytics. The ability to produce useful analytics can enhance faculty buy-in to the assessment process.

A previous capstone team has implemented a Django application, which is being deployed this spring. We are implementing a stand-alone complementary application which enhances the original with new functionality such as smart-assistant feedback and historical report generating.


To run locally enter "python manage.py runserver" within this folder

"models.py" file in main folder displays current tables within database.
Change Database settings to match your postgres database name go to
"settings.py" within the AcademicAssessmentAssistant folder 

# Release Notes

## 02-28-2022 (Milestone 1)

- SQL dump loaded into PostgreSQL database hosted on Amazon EC2 instance, information to connect is in the settings.py file.
- Models generated from the database in the models.py file.
- Home page displays the first 10 entries in table format of MakereportsSloinreport utilizing the model created in models.py, data is passed through the index function in views.py
- A few test cases have been written to test the URL routing of our existing project. These tests may be ran by typing in the project root directory the following:
```
pytest
```

## 02-28-2022 (Milestone 1)
- Updated Home Page HTML with buttons for views and dropdown department/degree program selection
- Added PDF Generation to Historical Data View with basic plots
- Added Navbar and HTML template
- Added Selenium Testing Framework and ChromeDriver
- Added Tests for Historical and Feedback Buttons on Home Page
- Added a test database with updated test command
```
pytest --reuse-db
```

