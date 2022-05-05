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

## 03-21-2022 (Milestone 2)
- Updated Home Page HTML with buttons for views and dropdown department/degree program selection
- Added PDF Generation to Historical Data View with basic plots
- Added Navbar and HTML template
- Added Selenium Testing Framework and ChromeDriver
- Added Tests for Historical and Feedback Buttons on Home Page
- Added a test database with updated test command
```
pytest --reuse-db
```
## 04-06-2022 (Milestone 3)
- Updated Home Page HTML with buttons for views and dropdown department/degree program selection
- Edited PDF Generation of Historical Data View to be dynamic with selected degree
- Enhanced Navbar and HTML template
- Added Historical Data page
- Added Degree Comparison page
- Added Degree Comparison PDF generation
- Added Selenium Tests for new pages
- Added new database credentials
- Adjusted how pytest works with database
- Added initial Smart Assistant HTML 
```
pytest
```
## 04-20-2022 (Milestone 4)
- Updated degree comparison page to filter by college
- Added heatmap to display blooms taxonomies used by each program
- Added assessment statistic plots to Historical pdf generattion
- Added more Selenium Tests
- Expanded on Smart Assistant and added Natural Language Processing for each SLO
```
pytest
```
## 05-07-2022 (Milestone 5)
- Added cosine similarity heatmap for programs SLOs
- Added coloring to smart assistant based on if they met or exceeded requirements
- Added more Selenium Tests
- Added more unit tests
- Cleaned up both pdf generations
```
pytest
```