from ensurepip import version


title = "Moodle Gateway"
description = """ Intermediate API endpoint that encapsulates/handles the authentication and request to the Moodle API (like a wrapper) and exposes a single, dedicated endpoint for POSTing the payloads.
## Authentication

Before all, you must **Authenticate it**.
## Autentication
* Login
* Logout

## Courses
* Get all courses
* Get course details
* Get course contents
* Get course progress
* Get courses by category

## Completion
* Mark as done

## Enrollment
* Enroll user
* Unenroll user

## Media
* Get media course
* Get media resource
"""

version = "1.0.0"
contact = {"name": "Orienteed", "url": "https://www.orienteed.com"}
license_info = {
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}
