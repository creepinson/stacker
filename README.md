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

### Running a stack

To run a stack from a stack.json5 file, simply run the following command:

`stacker -f stack.json5 up`
