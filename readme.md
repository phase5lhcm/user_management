

# The User Management System Final Project: Your Epic Coding Adventure Awaits! 🎉✨🔥

## Introduction: Buckle Up for the Ride of a Lifetime 🚀🎬

Welcome to the User Management System project - an epic open-source adventure crafted by the legendary Professor Keith Williams for his rockstar students at NJIT! 🏫👨‍🏫⭐ This project is your gateway to coding glory, providing a bulletproof foundation for a user management system that will blow your mind! 🤯 You'll bridge the gap between the realms of seasoned software pros and aspiring student developers like yourselves. 

### [Instructor Video - Project Overview and Tips](https://youtu.be/gairLNAp6mA) 🎥

- [Introduction to the system features and overview of the project - please read](system_documentation.md) 📚
- [Project Setup Instructions](setup.md) ⚒️
- [Features to Select From](features.md) 🛠️
- [About the Project](about.md)🔥🌟

## Goals and Objectives: Unlock Your Coding Superpowers 🎯🏆🌟

Get ready to ascend to new heights with this legendary project:

1. **Practical Experience**: Dive headfirst into a real-world codebase, collaborate with your teammates, and contribute to an open-source project like a seasoned pro! 💻👩‍💻🔥
2. **Quality Assurance**: Develop ninja-level skills in identifying and resolving bugs, ensuring your code quality and reliability are out of this world. 🐞🔍⚡
3. **Test Coverage**: Write additional tests to cover edge cases, error scenarios, and important functionalities - leave no stone unturned and no bug left behind! ✅🧪🕵️‍♂️
4. **Feature Implementation**: Implement a brand new, mind-blowing feature and make your epic mark on the project, following best practices for coding, testing, and documentation like a true artisan. ✨🚀🎆
5. **Collaboration**: Foster teamwork and collaboration through code reviews, issue tracking, and adhering to contribution guidelines - teamwork makes the dream work, and together you'll conquer worlds! 🤝💪🌍
6. **Industry Readiness**: Prepare for the software industry by working on a project that simulates real-world development scenarios - level up your skills to super hero status  and become an unstoppable coding force! 🔝🚀🏆⚡

## Submission and Grading: Your Chance to Shine 📝✏️📈

1. **Reflection Document**: Submit a 1-2 page Word document reflecting on your learnings throughout the course and your experience working on this epic project. Include links to the closed issues for the **5 QA issues, 10 NEW tests, and 1 Feature** you'll be graded on. Make sure your project successfully deploys to DockerHub and include a link to your Docker repository in the document - let your work speak for itself! 📄🔗💥

2. **Commit History**: Show off your consistent hard work through your commit history like a true coding warrior. **Projects with less than 10 commits will get an automatic 0 - ouch!** 😬⚠️ A significant part of your project's evaluation will be based on your use of issues, commits, and following a professional development process like a boss - prove your coding prowess! 💻🔄🔥

3. **Deployability**: Broken projects that don't deploy to Dockerhub or pass all the automated tests on GitHub actions will face point deductions - nobody likes a buggy app! 🐞☠️ Show the world your flawless coding skills!

## Managing the Project Workload: Stay Focused, Stay Victorious ⏱️🧠⚡

This project requires effective time management and a well-planned strategy, but fear not - you've got this! Follow these steps to ensure a successful (and sane!) project outcome:

1. **Select a Feature**: [Choose a feature](features.md) from the provided list of additional improvements that sparks your interest and aligns with your goals like a laser beam. ✨⭐🎯 This is your chance to shine!

2. **Quality Assurance (QA)**: Thoroughly test the system's major functionalities related to your chosen feature and identify at least 5 issues or bugs like a true detective. Create GitHub issues for each identified problem, providing detailed descriptions and steps to reproduce - the more detail, the merrier! 🔍🐞🕵️‍♀️ Leave no stone unturned!

3. **Test Coverage Improvement**: Review the existing test suite and identify gaps in test coverage like a pro. Create 10 additional tests to cover edge cases, error scenarios, and important functionalities related to your chosen feature. Focus on areas such as user registration, login, authorization, and database interactions. Simulate the setup of the system as the admin user, then creating users, and updating user accounts - leave no stone unturned, no bug left behind! ✅🧪🔍🔬 Become the master of testing!

4. **New Feature Implementation**: Implement your chosen feature, following the project's coding practices and architecture like a coding ninja. Write appropriate tests to ensure your new feature is functional and reliable like a rock. Document the new feature, including its usage, configuration, and any necessary migrations - future you will thank you profusely! 🚀✨📝👩‍💻⚡ Make your mark on this project!

5. **Maintain a Working Main Branch**: Throughout the project, ensure you always have a working main branch deploying to Docker like a well-oiled machine. This will prevent any last-minute headaches and ensure a smooth submission process - no tears allowed, only triumphs! 😊🚢⚓ Stay focused, stay victorious!

Remember, it's more important to make something work reliably and be reasonably complete than to implement an overly complex feature. Focus on creating a feature that you can build upon or demonstrate in an interview setting - show off your skills like a rockstar! 💪🚀🎓

Don't forget to always have a working main branch deploying to Docker at all times. If you always have a working main branch, you will never be in jeopardy of receiving a very disappointing grade :-). Keep that main branch shining bright!

Let's embark on this epic coding adventure together and conquer the world of software engineering! You've got this, coding rockstars! 🚀🌟✨

## Enhancements to the Event Management System, by Christine Maynard 🌟

🔨 Features Implemented 
# Event Model
* Created an Event SQLAlchemt model with:
    - title, description, start and end date, create_id (this is a ForeignKey to User)
    -Established a bi-directional relationship between User and Event models

* Pydantic Schemas 
    - Defined EventCreate for incoming request validation
    - Defined EventOut for clean API responses
    - Defined EventUpdate for partial or full updates

* Authorization 
    - Created is_admin_or_manager(), a utility function that takes an instance of User data to determine access to event management routes
    - Role-based access is restricted to admins/managers for main CRUD operations


# BREAD/API endpoints implemented in routers/event.py

| Endpoint                  | Method | Description                      |
|---------------------------|--------|----------------------------------|
| `/events/`                | GET    | Browse all events                |
| `/events/{event_id}`      | GET    | Read details of a single event   |
| `/events/`                | POST   | Add a new event                  |
| `/events/{event_id}`      | PUT    | Edit/update an existing event    |
| `/events/{event_id}`      | DELETE | Delete an event   


# Quality Assurance
Several critical issues were addressed to enhance the stability and reliability of the application:

Primary Key Configuration: Resolved a TypeError by ensuring the creator_id field in the Event model is correctly defined with UUID(as_uuid=True) and a proper foreign key reference.

Validation Error Handling: Fixed improper assertions in test_event_create_missing_title by accurately checking for missing fields in validation errors.

Date Validation in Event Creation: Corrected the test_event_create_start_after_end to ensure that events cannot have a start date after the end date, aligning with business rules.

Schema Consistency: Updated EventOut schema to match the creator_id type with the database model, preventing serialization errors.

Authorization Checks: Enhanced the is_admin_or_manager utility to robustly handle user role verification, preventing unauthorized access and reducing 500 errors.

New Tests Added
To ensure comprehensive coverage and reliability, new tests were created:

-Event Creation: Validates successful event creation with correct data.
-Missing Title Validation: Ensures that creating an event without a title raises a validation error.
-Start Date After End Date: Checks that an event cannot be created if the start date is after the end date.
-Unauthorized Access: Verifies that users without proper roles cannot access event-related endpoints.
-Event Retrieval: Tests fetching a specific event by ID.
-Event Update: Ensures that events can be updated correctly.
-Event Deletion: Validates that events can be deleted and are no longer retrievable.
-List Events: Checks that the list of events is returned correctly.
-Event Schema Output: Verifies the output schema of events matches expectations.
-Authorization Enforcement: Ensures that only users with 'admin' or 'manager' roles can perform certain actions.

Tests can be found in the app/tests directory.

# New Features Implemented
-Event Management Endpoints: Implemented CRUD operations for events, including creation, retrieval, updating, and deletion.
-Role-Based Access Control: Introduced checks to ensure only users with 'admin' or 'manager' roles can perform certain actions.
-Asynchronous Database Operations: Utilized AsyncSession for non-blocking database interactions, improving performance.
-Comprehensive Test Suite: Expanded the test suite to cover new features and edge cases, ensuring robustness.

For more detailed information on each feature and fix, refer to the respective test files and implementation details in the app/tests directory.               |