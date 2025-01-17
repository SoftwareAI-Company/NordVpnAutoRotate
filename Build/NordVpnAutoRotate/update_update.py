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
from CoreSecurity.keys.keys import *



diretorio_script = os.path.dirname(os.path.abspath(__file__))



def fazendo_o_download_da_nova_versao(bucket):

    try:

        nome_da_versao_dentro_do_buckt = f'atualizando_nordvpnautorotate_att.zip'
        diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
        extract_dir = os.path.join(diretorio_script)
        
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


fazendo_o_download_da_nova_versao(bucket)
