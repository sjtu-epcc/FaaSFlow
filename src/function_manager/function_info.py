import yaml
import os

# data structure for function info
class FunctionInfo:
    def __init__(self, function_name, img_name, max_containers, qos_time, qos_requirement):
        self.function_name = function_name
        self.img_name = img_name
        self.max_containers = max_containers
        self.qos_time = qos_time
        self.qos_requirement = qos_requirement

def generate_image(config_path, function_name, packages):
    function_path = os.path.join(config_path, function_name)
    dockerfile_path = os.path.join(function_path, "Dockerfile")
    requirements = ""
    for package in packages:
        requirements += " " + package
    with open(dockerfile_path, "w") as f:
        f.write("FROM workflow_base\n")
        f.write('COPY main.py /proxy/main.py\n')
        if requirements != "":
            f.write("RUN pip3 --no-cache-dir install{}".format(requirements))
    os.system("cd {} && docker build --no-cache -t {}_image .".format(function_path, function_name))

def parse(config_path):
    function_info = []
    config_file = os.path.join(config_path, "function_info.yaml")
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
        for c in config['functions']:
            function_name = c['name']
            packages = c['packages'] if 'packages' in c else [] 
            # generate_image(config_path, function_name, packages)
            
            # clear previous containers.
            os.system('docker stop $(docker ps -a | grep \"' + function_name + '_image' + '\" | awk \'{print $1}\')')
            os.system('docker rm $(docker ps -a | grep \"' + function_name + '_image' + '\" | awk \'{print $1}\')')

            info = FunctionInfo(function_name,
                              function_name + "_image",
                              c['max_containers'],
                              float(c['qos_time']),
                              float(c['qos_requirement']))
            function_info.append(info)
    return function_info