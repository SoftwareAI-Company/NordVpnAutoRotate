import threading
import time
import subprocess
import firebase_admin
import importlib.util
import os
import zipfile
import shutil
import pyautogui
import datetime
from firebase_admin import credentials, storage, db
import psutil
import firebase_admin
import time
import threading
import zipfile
import tempfile
import socket
from firebase_admin import credentials, initialize_app, storage, db, delete_app

from config.keys import *


diretorio_script = os.path.dirname(os.path.abspath(__file__))

def fazendo_o_download_da_nova_versao(bucket, nome_versao_atual, nova_versao):

    try:

        nome_da_versao_dentro_do_buckt = f'atualizando_nordvpnautorotate_{nova_versao}.zip'
        diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
        extract_dir = os.path.join(diretorio_script, 'Libs', 'vesion', f'Versao_{nova_versao}')
        
        #extract_dir = f'Arquivos/Versionamento_do_protocolo/Versao_{nova_versao}'
        os.makedirs(extract_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(delete=False) as temp_zip_file:
            temp_zip_filename = temp_zip_file.name
            blob = bucket.blob(nome_da_versao_dentro_do_buckt)
            blob.download_to_filename(temp_zip_filename)

        with zipfile.ZipFile(temp_zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        os.remove(temp_zip_filename)

    except Exception as eroo1:
        print(f"{eroo1}erro ao att ")



    try:

        nome_da_versao_dentro_do_buckt = f'atualizando_nordvpnautorotate_config_{nova_versao}.zip'
        diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
        extract_dir = os.path.join(diretorio_script, 'Libs', 'vesion', f'Versao_{nova_versao}', 'config')
        
        #extract_dir = f'Arquivos/Versionamento_do_protocolo/Versao_{nova_versao}'
        os.makedirs(extract_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(delete=False) as temp_zip_file:
            temp_zip_filename = temp_zip_file.name
            blob = bucket.blob(nome_da_versao_dentro_do_buckt)
            blob.download_to_filename(temp_zip_filename)

        with zipfile.ZipFile(temp_zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        os.remove(temp_zip_filename)

    except Exception as eroo1:
        print(f"{eroo1}erro ao att ")




    try:

        nome_da_versao_dentro_do_buckt = f'atualizando_nordvpnautorotate_ui_{nova_versao}.zip'
        diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
        extract_dir = os.path.join(diretorio_script, 'Libs', 'vesion', f'Versao_{nova_versao}', 'ui')
        
        #extract_dir = f'Arquivos/Versionamento_do_protocolo/Versao_{nova_versao}'
        os.makedirs(extract_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(delete=False) as temp_zip_file:
            temp_zip_filename = temp_zip_file.name
            blob = bucket.blob(nome_da_versao_dentro_do_buckt)
            blob.download_to_filename(temp_zip_filename)

        with zipfile.ZipFile(temp_zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        os.remove(temp_zip_filename)

    except Exception as eroo1:
        print(f"{eroo1}erro ao att ")
    return True
def fazendo_o_download_da_versao(bucket, nome_versao_atual, nova_versao):

    try:

        nome_da_versao_dentro_do_buckt = f'atualizando_nordvpnautorotate_{nova_versao}.zip'
        diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
        extract_dir = os.path.join(diretorio_script, 'Libs', 'vesion', f'Versao_{nova_versao}')
        
        #extract_dir = f'Arquivos/Versionamento_do_protocolo/Versao_{nova_versao}'
        os.makedirs(extract_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(delete=False) as temp_zip_file:
            temp_zip_filename = temp_zip_file.name
            blob = bucket.blob(nome_da_versao_dentro_do_buckt)
            blob.download_to_filename(temp_zip_filename)

        with zipfile.ZipFile(temp_zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        os.remove(temp_zip_filename)

    except Exception as eroo1:
        print(f"{eroo1}erro ao att ")



    try:

        nome_da_versao_dentro_do_buckt = f'atualizando_nordvpnautorotate_config_{nova_versao}.zip'
        diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
        extract_dir = os.path.join(diretorio_script, 'Libs', 'vesion', f'Versao_{nova_versao}', 'config')
        
        #extract_dir = f'Arquivos/Versionamento_do_protocolo/Versao_{nova_versao}'
        os.makedirs(extract_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(delete=False) as temp_zip_file:
            temp_zip_filename = temp_zip_file.name
            blob = bucket.blob(nome_da_versao_dentro_do_buckt)
            blob.download_to_filename(temp_zip_filename)

        with zipfile.ZipFile(temp_zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        os.remove(temp_zip_filename)

    except Exception as eroo1:
        print(f"{eroo1}erro ao att ")




    try:

        nome_da_versao_dentro_do_buckt = f'atualizando_nordvpnautorotate_ui_{nova_versao}.zip'
        diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
        extract_dir = os.path.join(diretorio_script, 'Libs', 'vesion', f'Versao_{nova_versao}', 'ui')
        
        #extract_dir = f'Arquivos/Versionamento_do_protocolo/Versao_{nova_versao}'
        os.makedirs(extract_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(delete=False) as temp_zip_file:
            temp_zip_filename = temp_zip_file.name
            blob = bucket.blob(nome_da_versao_dentro_do_buckt)
            blob.download_to_filename(temp_zip_filename)

        with zipfile.ZipFile(temp_zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        os.remove(temp_zip_filename)

    except Exception as eroo1:
        print(f"{eroo1}erro ao att ")




def nova_versao_disponivel(app1):
    buckett = storage.bucket(app=app1)
    ref1 = db.reference(f'Controle_de_versao/Controle_2', app=app1)
    data1 = ref1.get()
    x = data1["versao"]
    nome_versao_atual = f"{x}"
    numero_versao_atual = int(nome_versao_atual.split("_")[-1].split(".")[0])
    blobs = buckett.list_blobs()
    for blob in blobs:
        try:
            if blob.name != nome_versao_atual and blob.name.startswith("atualizando_nordvpnautorotate_"):
                numero_versao_nova = int(blob.name.split("_")[-1].split(".")[0])
                if numero_versao_nova > numero_versao_atual:
                    return True, numero_versao_nova, numero_versao_atual, blob.name
        except:
            pass
    
    return False, None, numero_versao_atual, x
        


Y, nova_versao, versao_atual, nome_versao_atual = nova_versao_disponivel(app1)
if Y:
    print("Recebemos uma nova versão. Vamos atualizar agora!")
    print(f"Nome da versao atual  {nome_versao_atual}")
    print(f"Número da nova versão: {nova_versao}")
    print(f"Número da versão atual: {versao_atual}")

    ver_true = fazendo_o_download_da_nova_versao(bucket, nome_versao_atual, nova_versao)
    if ver_true == True: 
        print("a nova versao foi baixada")    

        # nome_pasta_destinoteste = os.path.join(diretorio_script, 'vesion', f'Versao_{nova_versao}', )
        # os.makedirs(nome_pasta_destinoteste, exist_ok=True)
    

        comando_terminal = ['start', 'Dependenc/Python/pythonw', f'Dependenc/Libs/vesion/Versao_{nova_versao}/main.py']

        subprocess.Popen(comando_terminal, shell=True)
else:

    fazendo_o_download_da_versao(bucket, nome_versao_atual, versao_atual)


    comando_terminal = ['start', 'Dependenc/Python/pythonw', f'Dependenc/Libs/vesion/Versao_{versao_atual}/main.py']

    subprocess.Popen(comando_terminal, shell=True)