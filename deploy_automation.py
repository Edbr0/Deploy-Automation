import pyautogui as pa
import time
import json
import platform
from projects import projects

os = platform.system()


# Verifica se o arquivo de persistencia de dados ja existe
def fileExist(file_name):
    try:
        file = open(file_name)
        file.close()
        return True
    except:
        return False

# Cria o arquivo para persistencia de dados


def createFileData(file_name, data):
    try:
        file = open(file_name, 'w')
        file.write(data)
        file.close()
        return True
    except:
        return False


# digita e aperta enter
def writeAndPressEnter(value):
    pa.write(str(value))
    pa.press('enter')


# buscar dados no json
def getData(file_data):
    with open(file_data) as json_file:
        data = json.load(json_file)
    return data


# ------------------------------------------Funções que levam a pasta do projeto -----------------------------------------------------
def goToProject(project):
    writeAndPressEnter('cd /var/www/containers/')
    writeAndPressEnter(f'cd {project["path"]}')

# --------------------------------------------------------------------------------------------------------------------------------------------

# faz deploy de backend


def deployBackend(credentials):
    writeAndPressEnter('sudo git pull')
    time.sleep(0.5)
    writeAndPressEnter(credentials["password_server"])
    time.sleep(12)
    writeAndPressEnter(credentials["git_login"])
    time.sleep(0.5)
    writeAndPressEnter(credentials["git_pssw"])
    time.sleep(4)
    writeAndPressEnter('sudo docker-compose restart')


# faz deploy do frontend

def deployFrontend(credentials):
    writeAndPressEnter('sudo git pull')
    time.sleep(0.5)
    writeAndPressEnter(credentials["password_server"])
    time.sleep(12)
    writeAndPressEnter(credentials["git_login"])
    time.sleep(0.5)
    writeAndPressEnter(credentials["git_pssw"])
    time.sleep(4)
    writeAndPressEnter('yarnbuild')
    time.sleep(60)
    writeAndPressEnter('sudo docker-compose restart')


# Executa os passos da automaçãosudo docker-compose restart

def initAutomation(credentials, os, project):
    pa.PAUSE = 0.5
    if os == 'Windows':
        pa.hotkey('win', 'r')
        writeAndPressEnter('cmd')
    else:
        pa.hotkey('win', 't')
    time.sleep(1)
    writeAndPressEnter(
        f'ssh {credentials["user_server"]}@{credentials["server"]}')
    time.sleep(2)
    writeAndPressEnter(credentials["password_server"])
    time.sleep(0.5)
    goToProject(project)
    if project["mode"] == 'front':
        deployFrontend(credentials)
    else:
        deployBackend(credentials)

    time.sleep(3)
    pa.alert('Deploy realizado com sucesso!')


# Valida se todos os campos fora preenchidos
def fildsValidate(credentials):
    if not credentials["server"]:
        print('Ops... Você não informou o Servidor')
        return False
    if not credentials["user_server"]:
        print('Ops... Você não informou o usuario do Servidor')
        return False
    if not credentials["password_server"]:
        print('Ops... Você não informou sua senha do Servidor')
        return False
    if not credentials["git_login"]:
        print('Ops... Você não informou o seu usuario do Git')
        return False
    if not credentials["git_pssw"]:
        print('Ops... Você não informou sua senha do Git')
        return False

    return True

# Inputs dos dados de acesso ao servidor e git


def captureCredentials():
    server = input(str('Servidor(Com pontos): '))
    user = input(str('Usuário Servidor: '))
    password_server = input(str('Senha Servidor: '))
    git_login = input(str('Usuário Git: '))
    git_pssw = input(str('Senha Git: '))
    id_server = 1
    if fileExist('data.json') is True:
        servers = getData('data.json')
        id_server = servers[-1]["id"] + 1
    data = {'id': id_server, 'server': server, 'user_server': user, 'password_server': password_server,
            'git_login': git_login, 'git_pssw': git_pssw}

    return data


def __init__():
    if fileExist('data.json') is False:
        print('#############    Deploy Automation #################')
        print('-------------Preencha os dados abaixo.---------------')
        data = captureCredentials()
        validate = fildsValidate(data)
        if validate is False:
            return

        created = createFileData('data.json', json.dumps([data], indent=2))

        if created is False:
            print('Houve um erro ao gerar arquivo')
        else:
            print('############## Selecione o projeto #################')
            for project in projects:
                print(f'{project["id"]} - {project["name"]}')
            project_selected = int(input('Digite a opção: '))
            project_selected = projects[project_selected - 1]
            initAutomation(data, os, project_selected)
    else:
        servers = getData('data.json')
        print('############## Selecione o servidor #################')
        for server in servers:
            print(f'{server["id"]} - {server["server"]}')
        print('0 - Adicionar novo server')
        server_selected = int(input('Digite uma opção: '))
        if server_selected == 0:
            credential = captureCredentials()
            servers.append(credential)
            createFileData('data.json', json.dumps(servers, indent=2))
            return print('Server adicionado com sucesso!')

        server_selected = servers[server_selected - 1]
        print('############## Selecione o projeto #################')
        for project in projects:
            print(f'{project["id"]} - {project["name"]}')
        project_selected = int(input('Digite uma opção: '))
        project_selected = projects[project_selected - 1]

        initAutomation(server_selected, os, project_selected)


__init__()
