import subprocess
from time import sleep
import consolemenu
from consolemenu.items import *
import shutil 

API_CONTAINER_NAME = "marketweb-api"

def _apiContainerRunning():
    is_running = subprocess.run(f"docker ps", shell=True, capture_output=True, text=True).stdout.find('marketweb') > 0
    if not is_running: print("Make sure that the api container is running.")
    return is_running

def _apiContainerExecute(command: str):
    subprocess.run(f"docker exec {API_CONTAINER_NAME} {command}", shell=True)


def start():
    subprocess.run("docker compose up -d", shell=True)
    # TODO need to add checking if the database exists in docker, if not need to create it

def stop():
    subprocess.run("docker compose down", shell=True)

def restart():
    stop()
    start()

def clearCache():
    stop()
    cache_clear_cmds = ['docker container prune', 'docker image prune -a', 'docker builder prune']
    for command in cache_clear_cmds:
        try:
            subprocess.run(f"{command} -f", shell=True, capture_output=True, check=True, text=True)
        except subprocess.CalledProcessError as error:
            print(f"Error (code {error.returncode}): {error.stderr}")

    print("Cache Deleted!")

def newMigration():
    if not _apiContainerRunning(): return

    migration_name: str = input("Enter the name of the migration: ")
    CMD = f"npm run typeorm migration:create ./src/migrations/{migration_name}"
    _apiContainerExecute(CMD)
    return


def migrateUp():
    if not _apiContainerRunning(): return

    CMD = f"npm run migration:run"
    _apiContainerExecute(CMD)
    return

def migrateDown():
    if not _apiContainerRunning(): return

    CMD = f"npm run migration:revert"
    _apiContainerExecute(CMD)
    return

def newController():
    if not _apiContainerRunning():
        print("Make sure that the api container is running.")
        return

    controller_name: str = input("Enter the name of the controller: ")
    CMD = f"npx @nestjs/cli g controller ./resources/controllers/{controller_name}"
    _apiContainerExecute(CMD)

def newService():
    if not _apiContainerRunning():
        print("Make sure that the api container is running.")
        return

    service_name: str = input("Enter the name of the service: ")
    CMD = f"npx @nestjs/cli g service ./resources/services/{service_name}"
    _apiContainerExecute(CMD)

def newModule():
    if not _apiContainerRunning(): return

    module_name: str = input("Enter the name of the module: ")
    CMD = f"npx @nestjs/cli g module ./resources/modules/{module_name}"
    _apiContainerExecute(CMD)

def newResource():
    BASE_PATH = './marketweb-api/src'
    if not _apiContainerRunning(): return
    resource_name: str = input("Enter the name of the resource: ")
    CMD = f"npx @nestjs/cli g resource ./resources/{resource_name}"
    _apiContainerExecute(CMD)
    
def updateNpmPackages():
    if not _apiContainerRunning(): return
    CMD = 'npm ci'
    _apiContainerExecute(CMD)

if __name__ == '__main__':
    PROMPT = "Enter an action: "

    # using parallel lists bc selectio returns index not key
    labels = ['start', 'stop', 'restart', 'update npm packages', 'clear cache', 'new resource', 'new controller', 'new service', 'new module',  'new migration', 'migrate up', 'migrate down', 'exit']
    functions = [start, stop, restart, updateNpmPackages, clearCache, newResource, newController, newService, newModule, newMigration, migrateUp, migrateDown,  exit]

    menu = consolemenu.SelectionMenu(labels,"Select an option", clear_screen=False)

    while True:
        menu.show(show_exit_option=False)
        menu.join()

        selection = menu.selected_option
        functions[selection]()