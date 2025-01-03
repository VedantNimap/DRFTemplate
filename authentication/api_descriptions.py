CUSTOM_JWT_LOGIN_DESCRIPTION = """
This endpoint authenticates a user and issues JSON Web Tokens (JWT) for access and refresh.

**Required Fields:**
- `email` (string): The email address of the user.
- `password` (string): The password of the user.

**Optional Fields:**
- `browserInfo` (string): Information about the user's browser.
- `ipAddress` (string): The IP address of the user.
- `osInfo` (string): Information about the user's operating system.
- `timezone` (string): The user's timezone.
- `location` (string): The user's location.
- `deviceId` (string): The user's device's unique ID.


**Response:**
On successful authentication, the API returns an access token and a refresh token. The access token is used to authenticate subsequent requests, and the refresh token is used to obtain a new access token when the current one expires.
The duration of the access token and refresh token will changed during the development process.
"""

CUSTOM_LOGOUT_DESCRIPTION = """
**Description:**
This endpoint logs out the authenticated user by ending their session. The session end time is recorded on the server side. The frontend is responsible for deleting the access and refresh tokens.

**Response:**
On successful logout, the API confirms the session has been ended.

**Note:**
- The user must be authenticated to access this endpoint.
"""

TOKEN_VERIFY_DESCRIPTION = """
**Description:**
This endpoint verifies the validity of an access token.

**Request Body Parameters:**
- `token` (string): The access token to be verified.

**Response:**
- If the token is valid, the API returns a success status 200.
- If the token is invalid or expired, appropriate error messages are returned.

**Note:**
- This endpoint is used to verify the validity of access tokens before making authenticated requests.
"""

TOKEN_REFRESH_DESCRIPTION = """
**Description:**
This endpoint refreshes an expired access token using a valid refresh token.

**Request Body Parameters:**
- `refresh` (string): The refresh token obtained during login.

**Response:**
On successful token refresh, the API returns a new access token.

**Note:**
- This endpoint requires a valid refresh token to be provided.
"""

PROFILE_LIST_DESCRIPTION = """
**Description:**
This endpoint retrieves the profile details of the authenticated user. It returns the user's information.

**Response:**
The API returns the profile information of the authenticated user. 

**Note:**
- The user must be authenticated to access this endpoint.
"""

PROFILE_PICTURE_UPDATE_DESCRIPTION = """
**Description:**
This endpoint updates the profile picture of the authenticated user.

**Required Fields:**
- `profile_picture` (binary): The new profile picture of the user.

**Response:**
The API returns the link of the profile picture. 

**Note:**
- The user must be authenticated to access this endpoint.
"""

RECENT_ACTIVITY_LIST_DESCRIPTION = """
**Description:**
This endpoint retrieves the recent session data of the authenticated user, ordered by the session start time in descending order.

**Response:**
The API returns a list of session details, including information about each session's start time, end time, and the user associated with the session.

**Note:**
- The user must be authenticated to access this endpoint.
"""

