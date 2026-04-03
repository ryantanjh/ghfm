# CLAUDE.md
# Project description
This project is to create a simple prototype of an order management system for a hedge fund

# General Project Architecture
/client
    /src
        /pages
        /components
    app.ts
/api
    requirements.txt
    start.sh
    /app
        main.py # all routes go here, injects services layer as dependency
        /models # pydantic dtos
        /repo # repo layer classes
            database.py # SQLAlchemy engine + Sqlite setup
        /services # business logic, injects repo layer as dependency
    /tests # unit testing for functions in services layer

# Tech Stack
- Front end: A simple ReactJs project using javascript, Highcharts, and Ant Design
- Backend: FastAPI
- Database: SQLlite with SQLAlchemy ORM
- Deployment: start.sh script used to run app locally. Assume that the user does not have any dependencies
installed

# General Coding Best Practices
- Follow DRY principles
- Each function should have single responsibility, and clear documentation, as well as specify output type
- If function params and return types are objects, create pydantic dtos for them
- Keep code as simple as possible
- Do not add code comments or print statements
- Implement the bare minimum test cases that are required for a particular feature

# Worflow
- Refer to PLAN.md and MEMORY.md on what has been done, and what needs to be done for the next feature
- You will work on it feature by feature, and I will clear context after each feature is done
- Generate the test cases for the feature that you are working on
- Once code is done and test cases pass, commit the changes, and update MEMORY.md