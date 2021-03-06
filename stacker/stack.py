import json5
import docker
from glob import glob
import os
from .map import Map
from .progress import progress_wrapped

apiClient = docker.APIClient()
client = docker.from_env()

management = Map({})

root_stack = None


def get_container_name(c):
    global root_stack
    name = f"{root_stack.name}_"
    for s in get_stacks(root_stack):
        name += f"{s.name}_"
    return f"{name}{c.name}"


def get_volumes(c):
    volumes = c.volumes
    keys = list(volumes.keys())
    for i in range(len(volumes)):
        v = keys[i]
        if v.startswith("./"):
            newKey = os.path.abspath(c.stack.folder + v.replace(".", ""))
            volumes[newKey] = volumes[v]
            del volumes[v]
        if v.startswith("../"):
            newKey = os.path.abspath(c.stack.folder + v)
            volumes[newKey] = volumes[v]
            del volumes[v]
    return volumes


@progress_wrapped(estimated_time=100)
def start_stack(stack):
    try:
        apiClient.remove_network("stacker")
    except:
        # Network does not exist, create it
        pass
    try:
        apiClient.create_network("stacker")
    except Exception as e:
        print("Unable to create container network 'stacker': ")
        print(e)
        pass
    for c in get_containers(stack):
        c_name = get_container_name(c)
        print(f"Starting {c_name}")
        try:
            existing = client.containers.get(c_name)
            existing.stop()
            existing.remove()
        except Exception as e:
            pass
        try:
            client.images.get(c.image)
        except:
            # Image does not exist yet
            print(f"Pulling image {c.image}...")
            client.images.pull(c.image)
        environment = {}
        try:
            if c.environment:
                if isinstance(c.environment, str):
                    with open(c.stack.folder + c.environment) as f:
                        environment = json5.load(f)
                else:
                    environment = c.environment
        except Exception as e:
            print(f"Failed to parse json5 env file for {c_name}:")
            print(e)
        try:
            host_config = apiClient.create_host_config(
                binds=get_volumes(c),
                port_bindings=c.ports or {},
                networking_config=apiClient.create_networking_config({
                    "stacker": apiClient.create_endpoint_config(
                        links=[tuple(c.links or {})]
                    )
                })
            )
            apiClient.create_container(
                image=c.image, name=c_name, volumes=list(c.volumes.keys()), host_config=host_config, ports=list(c.ports.keys() or []), detach=True, environment=environment or {})
        except Exception as e:
            apiClient.create_container(
                image=c.image, name=c_name, detach=True, environment=environment or {})
        client.containers.get(c_name).start()


def get_logs(stack):
    logs = ""
    for c in get_containers(stack):
        c_name = get_container_name(c)
        try:
            existing = client.containers.get(c_name)
            logs += existing.logs().decode("utf-8")
        except docker.errors.NotFound as e:
            print(f"Couldnt get logs for {c_name}")
            continue
    return logs


def get_container_logs(c_name):
    logs = ""

    try:
        existing = client.containers.get(c_name)
        logs += existing.logs().decode("utf-8")
    except docker.errors.NotFound as e:
        print(f"Couldnt get logs for {c_name}")
        pass
    return logs


def list_containers(stack):
    containers = []
    for c in get_containers(stack):
        c_name = get_container_name(c)
        containers.append(c_name)
    return containers


def stop_container(name):
    try:
        management[name].stop()
    except:
        print(f"No such container {name}")


def start_container(name):
    try:
        management[name].start()
    except:
        print(f"No such container {name}")


def restart_container(name):
    stop_container(name)
    start_container(name)


def stop_stack(stack):
    for c in get_containers(stack):
        c_name = get_container_name(c)
        print(f"Stopping {c_name}")
        try:
            existing = client.containers.get(c_name)
            existing.stop()
        except:
            continue


def restart_stack(stack):
    for c in get_containers(stack):
        c_name = get_container_name(c)
        print(f"Restarting {c_name}")
        try:
            existing = client.containers.get(c_name)
            existing.stop()
            existing.start()
        except:
            continue


def get_stacks(stack):
    stacks = []
    stacks.extend(stack.children)
    for s in stack.children:
        stacks.extend(get_stacks(s))
    return stacks


def get_containers(stack):
    containers = []
    containers.extend(stack.containers)
    for c in stack.children:
        containers.extend(get_containers(c))
    return containers


def create_container(stack, name=None, obj={}):
    c = Map(
        {"stack": stack, "name": name or "default", **obj})
    return c


def create_stack(parent=None, folder=None, name=None, containers=None):
    global root_stack
    s = Map({"children": [], "containers": containers or [],
             "parent": parent, "folder": folder or "./", "name": name or "default"})
    if s.parent == None:
        root_stack = s
    return s


def get_file_name(f):
    return os.path.splitext(os.path.basename(f))[0].replace(".stack", "").replace(".json5", "")


def create_stack_from_file(file_path, parent):
    try:
        stack = create_stack(folder=(file_path.replace(
            os.path.basename(file_path), "")), parent=parent, name=get_file_name(file_path))
        with open(file_path) as f:
            data = json5.load(f)
            include = data.get("include", None)
            containers = data.get("containers", None)
            if include:
                for i in include:
                    for f in sorted(glob(stack.folder + i, recursive=True), reverse=True):
                        stack.children.append(
                            create_stack_from_file(f, stack))
            if containers:
                for c in containers:
                    stack.containers.append(
                        create_container(stack, c["name"], c))
    except FileNotFoundError:
        print(f"Stack file at {file_path} does not exist.")
    return stack


def remove_parents(stack):
    del stack.parent
    for con in stack.containers:
        con.stack = con.stack.name
    for c in stack.children:
        try:
            for con in c.containers:
                con.stack = con.stack.name
            del c.parent
            remove_parents(c)
        except KeyError:
            continue


def print_stack(s, indent=4):
    stack = s
    remove_parents(stack)

    return json5.dumps(stack, indent=indent)
