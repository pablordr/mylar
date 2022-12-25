a sample web app to test things on

Checkpoint 4: Decoupling of front & back

- Back as separate server, works only as API. 
- Front as separate server only makes API requests.
    - Front includes teh `API_ENDPOINT` variable that points to the API.
- Each front instance shows its IP & hostname


Checkpoint 3: Docker

- Now it runs on docker
- Added BASE_URL variable for templates to use the correct endpoint.
- Should run with `docker run -d -p 8080:5000 --name mylar mylar:latest`

Checkpoint 2: Cookies

- Now it has a simple user_name cookie. Easy to manipulate. 
- Each view shows the value of the cookie.
- It will be used to assign edit ops to an user. 


Checkpoint 1: Minimum features

- Show all entries via `/entries`
- Add new entry via `/add`
- Show specific entry via `/entry?id=<ID>`
- Edit specific entry via `/edit?id=<ID>`
- Templates for each feature & an error page with a custom message.

TODO:

- Field type verification (id must be an INT, etc.)
- Repeated ID validation 