# Event Manager Assignment - User Management API

## Assignment Submission

This repository contains a FastAPI-based user management system with JWT token-based OAuth2 authentication. The implementation focuses on secure user authentication, profile management, and role-based access control.

## Issues Fixed

I have identified and fixed the following issues in the codebase:

1. [Nickname Validation](https://github.com/Hameed1117/event_manager_assignment/tree/fix-nickname-validation) - Implemented improved nickname validation with comprehensive tests to ensure nicknames follow the required format and constraints.

2. [Password Validation](https://github.com/Hameed1117/event_manager_assignment/tree/fix-password-validation) - Added comprehensive password validation tests to ensure passwords meet security requirements including length, complexity, and special characters.

3. [Profile Fields Validation](https://github.com/Hameed1117/event_manager_assignment/tree/fix-profile-fields) - Improved profile field validation and updates for bio and profile URLs to handle edge cases and ensure data integrity.

4. [OAuth Token Generation](https://github.com/Hameed1117/event_manager_assignment/tree/fix-oauth-token) - Implemented proper JWT token generation and validation for OAuth to ensure secure authentication.

5. [User Registration Edge Cases](https://github.com/Hameed1117/event_manager_assignment/tree/fix-user-registration-edge-cases) - Added tests and fixes for user registration edge cases to handle various scenarios and improve robustness.

6. [Swagger Bearer Auth](https://github.com/Hameed1117/event_manager_assignment/tree/fix-swagger-bearer-auth) - Fixed authorization in Swagger UI to improve API documentation and testing experience.

All these fixes have been merged into the main branch after thorough testing and code review.

## Docker Image

The Docker image for this project is available on Dockerhub at: [khadhar17/event-manager-api](https://hub.docker.com/repository/docker/khadhar17/event-manager-api/general)

## Reflection

Working on this assignment has been an invaluable learning experience that has significantly enhanced both my technical skills and understanding of collaborative development practices. The process of identifying and fixing issues related to user validation, authentication, and profile management has deepened my understanding of security best practices in web applications. I particularly found the implementation of JWT token-based authentication challenging yet rewarding, as it required a thorough understanding of OAuth2 flows and secure token handling.

The collaborative aspects of this assignment, including working with Git branches, creating pull requests, and conducting code reviews, have given me practical experience with industry-standard development workflows. I've learned the importance of clear documentation and comprehensive testing, especially when dealing with security-critical features like user authentication. Increasing the test coverage to 90% was initially daunting, but it forced me to consider various edge cases and potential vulnerabilities, ultimately resulting in more robust code. This assignment has reinforced my belief in the value of test-driven development and the role of quality assurance in building reliable software systems.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/Hameed1117/event_manager_assignment.git
   cd event_manager_assignment
   ```

2. Using Docker (recommended):
   ```
   docker-compose up -d
   ```

3. Access the API documentation at `http://localhost/docs`

4. Access PGAdmin at `http://localhost:5050` for database management

## Testing

Run the tests to verify the fixes and ensure high test coverage:

```
pytest
```

## License
This project is licensed under the MIT License - see the `license.txt` file for details.
