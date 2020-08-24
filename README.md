# Stacker

A docker compose alternative that uses json5 and supports including other stack files.

## Dependencies

This requires docker to be installed, you can get it with this command:

```bash
curl -L https://get.docker.com | sh
```

## Usage

Simply install this package and then run `stacker -h` in a terminal for help.

### Configuring a stack

A stack file uses the json5 format. An example of a nginx stack looks like this:

```json
{
    "containers": [
        {
            "name": "nginx",
            "image": "nginx:alpine",
            "volumes": {
                "./html": {
                    "bind": "/usr/share/nginx/html"
                }
            },
            "ports": {
                "80": 8080
            }
        }
    ]
}
```

You can also include other stack files like so:

```json
{
    "include": ["services/*.stack.json5"]
}
```

You can include env files (must be in json5 format as of now) or a map of environment variables with the `environment` key.

Example:

```json
{
    "name": "nginx",
    "image": "nginx:alpine",
    "environment": "../.env.json5"
}
```

### Running a stack

To run a stack from a stack.json5 file, simply run the following command:

`stacker -f stack.json5 up`


### Installation
As of now it is not on pip so if you want to use it you have to clone and build it yourself (although its not that hard). To do this, first clone the repository and cd into it. Then run the following command to build and install it.

```
python3 setup.py sdist && python3 -m pip install dist/docker-stacker-1.0.0.tar.gz
```

It may not always be 1.0.0 so you can check the version in the setup.py file.