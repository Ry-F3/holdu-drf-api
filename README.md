# Holdu
## Django REST API for Health and Social Sector Job Application Platform

This project is a Django REST API designed for a social media job application platform tailored specifically for the health and social sector. Similar to LinkedIn, it facilitates interactions between employers and employees, with a focus on seamless job posting, application management, and offer processing.

## Key Features:

* **Profile Types and Authentication:** Users are authenticated based on their profile type (employee or employer), ensuring secure access to relevant features and data.

* **Job Posting:** Employers can post job listings, detailing available positions within the health and social sector.

* **Application Management:** Employees can apply for jobs posted by employers, initiating a streamlined application process.

* **Applicant Tracking:** Employers can manage applicants by marking them as Shortlisted, Accepted, or Binned, streamlining the hiring process.

* **Offer Processing:** Once an applicant is accepted, the API facilitates the posting of offers, allowing applicants to respond accordingly.

* **Notification System:** Users receive notifications to stay updated on application status changes, messages, and other relevant activities within the platform.

* **Chat and Connections System:** A built-in chat system enables users to communicate with other users, potential employers, or employment partners, fostering connections and collaborations.

* **Rating System:** Users can rate and provide feedback on their experiences, enhancing transparency and trust within the community.

* **Showcasing Experience:** Users can showcase their professional experience and qualifications, providing comprehensive profiles for potential employers to review.

* **Interacting with Job Listings:** Users can engage with job listings by liking, commenting, and sharing, facilitating community interaction and engagement.

## Developer User Stories 

| Section 1 |
| --- |
| **#1** As a backend developer, I want to implement CRUD functionality for user profiles, allowing users to create, read, update, and delete their profile information, including details about skills and experience, through API endpoints. |
| **#2** As a backend developer, I want to implement endpoints for rating and reviewing other users, including logic to calculate average ratings and display them on user profiles. |
| **#3** As a user, I want to be able to create three types of profiles on the platform: employee, employer, and admin, each with distinct permissions and features, to cater to different user roles and functionalities. |
| **#4** As a backend developer, I want to implement search and filtering functionality for user profiles based on skills, ratings, and other relevant criteria, optimising queries for performance and scalability. |
| **#5** As a backend developer, I want to define database models for job listings, including fields for job title, description, required skills, compensation, and other relevant details, implementing CRUD functionality for managing job listings. |

| Section 2 |
| --- |
| **#6** As a backend developer, I want to implement database models and relationships for user connections, allowing users to send and accept connection requests and maintain a network of professional relationships. |
| **#7** As a backend developer, I want to create API endpoints for managing user connections, including functionalities for sending connection requests, accepting or rejecting requests, and fetching connections' profiles. |
| **#8** As a backend developer, I want to implement database models and relationships for direct messages, enabling users to send messages to specific connections. |
| **#9** As a backend developer, I want to create API endpoints for managing direct messages, including functionalities for sending, receiving, and deleting messages. |
| **#10** As a backend developer, I want to implement notification mechanisms for profile activities, including logic to trigger notifications when users receive connection requests, profile views, or messages. |

| Section 3 |
| --- |
| **#11** As a developer working on the Jobs app, I want to implement likes and comments functionalities to work seamlessly with the existing features. This will enhance user engagement and provide a platform for users to interact with each other regarding job listings. |
| **#12** As a developer, I want to integrate JWT tokens into my project to enhance security and provide authentication and authorization mechanisms for users. This involves generating tokens upon user authentication, validating tokens for each request, and managing token expiration and refreshment. |
| **#13** As a developer, I want to deploy my project to Heroku with appropriate settings to make it accessible to users on the web. This involves configuring environment variables, setting up the necessary buildpacks, and ensuring compatibility with Heroku's platform. |
| **#14** As a developer, I want to clean up and refactor my codebase to improve readability, maintainability, and performance. This involves identifying and removing redundant code, restructuring code for better organization, and optimising performance bottlenecks. |
| **#15** As a developer, I want to connect my project to an external database (ElephantSQL) to store and manage persistent data. This involves configuring database connection settings, creating necessary database tables or collections, and implementing data access logic within the project. |
| **#16** As a developer, I want to write tests for my code to ensure its correctness, reliability, and maintainability. This involves writing unit tests to cover individual functions or components, integration tests to test interactions between different parts of the system, and end-to-end tests. |

## Agile Methodology

GitHub Issues were utilised extensively throughout the development process of the project. These issues were tracked using the following link: [GitHub Issues](https://github.com/Ry-F3/holdu-drf-api/issues?q=is%3Aissue+is%3Aclosed).

Each user story, representing a feature or task, was captured as a GitHub issue and categorised accordingly. To ensure clarity and organisation, labels were employed. These labels can be viewed at: [Labels](https://github.com/Ry-F3/holdu-drf-api/labels). Labels were used to categorise issues based on workflow, enhancements, or new features.

To provide a higher-level overview and categorisation, issues were grouped into six epics. These epics served to distinguish between different aspects or modules of the project, making it easier to manage and prioritise work. Priority labels were applied to issues to indicate their importance and urgency, aiding in the allocation of resources and prioritisation of tasks.

Throughout the development process, the project progressed through three sprints. To document the conclusion of each sprint and mark significant [milestones](https://github.com/Ry-F3/holdu-drf-api/milestones?state=closed).
, milestones were used. These milestones helped in tracking the project's progress over time and provided a clear indication of the completion of specific phases or iterations.

For visual representation and enhanced project management, three Kanban boards were utilised as sprints. The Kanban boards provided a visual overview of the project's progress, this allowed the tracking of tasks as they moved through various stages of completion. The Kanban boards for the project can be accessed via the following link: [Kanban Board](https://github.com/Ry-F3/holdu-drf-api/projects?query=is%3Aopen).
