### GFModules Pseudonym Service

The Pseudonym Service is responsible for the pseudonymisation of the BSN. Preferably the
BSNk service would be used instead of this service. But because the BSNk is still under
development, the Pseudonym Service is used.


## Usage

The application is a FastAPI application, so you can use the FastAPI documentation to see how to use the application.

## Development

You can either run the application natively or in a docker container. If you want to run the application natively you
can take a look at the initialisation steps in `docker/init.sh`. 

The preferred way to run the application is through docker.

If you run Linux, make sure you export your user ID and group ID to synchronize permissions with the Docker user.

```
export NEW_UID=$(id -u)
export NEW_GID=$(id -g)
```

After this you can simply run `docker compose up`. 

The application will be available at https://localhost:8504 when the startup is completed.


# Docker container builds

There are two ways to build a docker container from this application. The first is the default mode created with:

```bash
docker build \
  --build-arg="NEW_UID=1000" \
  --build-arg="NEW_GID=1000" \
  -f docker/Dockerfile \
  -t gfmodules-pseudonym-stub \
  .
```

This will build a docker container that will run its migrations to the database specified in app.conf.

The second mode is a "standalone" mode, where it will not run migrations, and where you must explicitly specify
an app.conf mount.

```bash
docker build \
  --build-arg="standalone=true" \
  -f docker/Dockerfile \
  -t gfmodules-pseudonym-stub \
  .
```

Both containers only differ in their init script and the default version usually will mount its own local src directory
into the container's /src dir.

```bash
docker run -ti --rm -p 8504:8504 \
  --mount type=bind,source=./app.conf.example,target=/src/app.conf \
  gfmodules-pseudonym-stub
```
