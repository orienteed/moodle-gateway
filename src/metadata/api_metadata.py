from ensurepip import version


title = "Moodle Gateway"
description = """
## What is Moodle Gateway?
Moodle Gateway is an excellent tool for those who want to integrate Moodle with external systems but don't have the knowledge or time to develop a custom integration.

It is an intermediate API that encapsulates/handles the authentication and requests to the Moodle API (like a wrapper) and exposes some endpoints to interact with them. The Gateway is a straightforward and effective way to integrate Moodle with third-party systems.

This software can be installed on a server and configured to listen for incoming requests from external systems. It then forwards those requests to Moodle using the Moodle API.

## How does it work?
You should use the header 'api-authorization' with the Magento Customer token value to authenticate the requests.
"""

version = "1.0.0"
contact = {"name": "Orienteed", "url": "https://www.orienteed.com"}
license_info = {
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
}
