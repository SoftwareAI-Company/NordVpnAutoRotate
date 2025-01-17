
from firebase_admin import credentials, initialize_app, storage, db, delete_app


import os
import time
import zipfile
import subprocess
import shutil
import random
import sys
import threading
import os
import platform
import subprocess
import psutil
import re
import time
import urllib
import requests
import json

import firebase_admin
from CoreSecurity.keys.keys import *

time.sleep(3)

start_time = time.time()




start_time = time.time()
lista = ['main.py']
for list in lista: #   "-e", "30",  
    subprocess.run(["pyarmor-8", "gen", "--assert-import", "--assert-call", "--enable-themida",  "--enable-jit",  "--mix-str",  "--obf-code", "2", f"{list}"])



time.sleep(3)

def buscar_arquivo(nome_arquivo):
    blob = bucket.blob(nome_arquivo)
    if blob.exists():
        return blob
    else:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado no bucket.")
        return None


diretorio_script = os.path.dirname(os.path.abspath(__file__))

ref1 = db.reference(f'Controle_de_versao/Controle_2')
data1 = ref1.get()
x = data1["versao"]

nome_arquivo = f"{x}"
blob_arquivo = buscar_arquivo(nome_arquivo)
if blob_arquivo:
    print(f"O arquivo '{nome_arquivo}' foi encontrado no bucket criando nova versao.")
    numero_versao_atual = int(nome_arquivo.split("_")[-1].split(".")[0])
    nova_versao = numero_versao_atual + 1
    folder_to_zip = "dist"
    zip_folder_name = "atualizando_nordvpnautorotate"    
    zip_file_name = zip_folder_name + f"_{nova_versao}" + ".zip"

    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(folder_to_zip):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, folder_to_zip)
                zipf.write(filepath, arcname)


    blob = bucket.blob(zip_file_name)
    blob.upload_from_filename(zip_file_name)
    print("ZIPADO E ENVIADO PARA FIREBASE COM sucesso !")

    time.sleep(3)
    os.remove(zip_file_name)
    

    time.sleep(3)
    try:
        shutil.rmtree(folder_to_zip)
        print(f"A pasta '{folder_to_zip}' foi excluída com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir a pasta '{folder_to_zip}': {str(e)}")

    ref1 = db.reference(f'Controle_de_versao')
    data1 = ref1.get()                         
    controle_das_funcao = "Controle_1"
    controle_das_funcao_info_ = {
    "versao": zip_file_name,
    }
    ref1.child(controle_das_funcao).set(controle_das_funcao_info_)
    
    ref1 = db.reference(f'Controle_de_versao')
    data1 = ref1.get()                         
    controle_das_funcao2 = "Controle_2"
    controle_das_funcao_info_2 = {
    "versao": nome_arquivo,
    }
    ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
    

else:
    print("Não foi possível encontrar o arquivo.")




def buscar_arquivo(nome_arquivo):
    blob = bucket.blob(nome_arquivo)
    if blob.exists():
        return blob
    else:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado no bucket.")
        return None


diretorio_script = os.path.dirname(os.path.abspath(__file__))

ref1 = db.reference(f'Controle_de_versao/Controle_config_2')
data1 = ref1.get()
x = data1["versao"]

nome_arquivo = f"{x}"
blob_arquivo = buscar_arquivo(nome_arquivo)
if blob_arquivo:
    print(f"O arquivo '{nome_arquivo}' foi encontrado no bucket criando nova versao.")
    numero_versao_atual = int(nome_arquivo.split("_")[-1].split(".")[0])
    nova_versao = numero_versao_atual + 1
    folder_to_zip = "config"
    zip_folder_name = f"atualizando_nordvpnautorotate_config"    
    zip_file_name = zip_folder_name + f"_{nova_versao}" + ".zip"

    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(folder_to_zip):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, folder_to_zip)
                zipf.write(filepath, arcname)


    blob = bucket.blob(zip_file_name)
    blob.upload_from_filename(zip_file_name)
    print("ZIPADO E ENVIADO PARA FIREBASE COM sucesso !")

    ref1 = db.reference(f'Controle_de_versao')
    data1 = ref1.get()                         
    controle_das_funcao = "Controle_config_1"
    controle_das_funcao_info_ = {
    "versao": zip_file_name,
    }
    ref1.child(controle_das_funcao).set(controle_das_funcao_info_)
    
    ref1 = db.reference(f'Controle_de_versao')
    data1 = ref1.get()                         
    controle_das_funcao2 = "Controle_config_2"
    controle_das_funcao_info_2 = {
    "versao": nome_arquivo,
    }
    ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
    
    os.remove(zip_file_name)


else:
    print("Não foi possível encontrar o arquivo.")







start_time = time.time()
lista = ['ui/benchmark_window_ui.py', 'ui/global_benchmark_window_ui.py', 'ui/main_window_ui.py']
for list in lista: #   "-e", "30", "--assert-import", "--assert-call", "--enable-themida",  "--enable-jit", 
    subprocess.run(["pyarmor-8", "gen", "--assert-import", "--assert-call", "--enable-themida",  "--enable-jit",  "--mix-str",  "--obf-code", "2", f"{list}"])

time.sleep(3)
shutil.copy('ui/logo.jpg', 'dist')
shutil.copy('ui/logo2.png', 'dist')
shutil.copy('ui/style.qss', 'dist')
shutil.copy('ui/icone_usa.png', 'dist')
shutil.copy('ui/icone_canada.png', 'dist')

def buscar_arquivo(nome_arquivo):
    blob = bucket.blob(nome_arquivo)
    if blob.exists():
        return blob
    else:
        print(f"O arquivo '{nome_arquivo}' não foi encontrado no bucket.")
        return None


diretorio_script = os.path.dirname(os.path.abspath(__file__))

ref1 = db.reference(f'Controle_de_versao/Controle_ui_2')
data1 = ref1.get()
x = data1["versao"]

nome_arquivo = f"{x}"
blob_arquivo = buscar_arquivo(nome_arquivo)
if blob_arquivo:
    print(f"O arquivo '{nome_arquivo}' foi encontrado no bucket criando nova versao.")
    numero_versao_atual = int(nome_arquivo.split("_")[-1].split(".")[0])
    nova_versao = numero_versao_atual + 1
    folder_to_zip = "dist"
    zip_folder_name = f"atualizando_nordvpnautorotate_ui"    
    zip_file_name = zip_folder_name + f"_{nova_versao}" + ".zip"

    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(folder_to_zip):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, folder_to_zip)
                zipf.write(filepath, arcname)


    blob = bucket.blob(zip_file_name)
    blob.upload_from_filename(zip_file_name)
    print("ZIPADO E ENVIADO PARA FIREBASE COM sucesso !")
    ref1 = db.reference(f'Controle_de_versao')
    data1 = ref1.get()                         
    controle_das_funcao = "Controle_ui_1"
    controle_das_funcao_info_ = {
    "versao": zip_file_name,
    }
    ref1.child(controle_das_funcao).set(controle_das_funcao_info_)
    
    ref1 = db.reference(f'Controle_de_versao')
    data1 = ref1.get()                         
    controle_das_funcao2 = "Controle_ui_2"
    controle_das_funcao_info_2 = {
    "versao": nome_arquivo,
    }
    ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

    time.sleep(3)
    os.remove(zip_file_name)
    
    try:
        shutil.rmtree(folder_to_zip)
        print(f"A pasta '{folder_to_zip}' foi excluída com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir a pasta '{folder_to_zip}': {str(e)}")


else:
    print("Não foi possível encontrar o arquivo.")


lista = ['att.py']
for list in lista: #   "-e", "30", "--assert-import", "--assert-call", "--enable-themida",  "--enable-jit", 
    subprocess.run(["pyarmor-8", "gen", "--assert-import", "--assert-call", "--enable-themida",  "--enable-jit",  "--mix-str",  "--obf-code", "2", f"{list}"])



time.sleep(3)

folder_to_zip = "dist"
zip_folder_name = f"atualizando_nordvpnautorotate_att"    
zip_file_name = zip_folder_name + ".zip"

with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(folder_to_zip):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, folder_to_zip)
            zipf.write(filepath, arcname)


blob = bucket.blob(zip_file_name)
blob.upload_from_filename(zip_file_name)
print("ZIPADO E ENVIADO PARA FIREBASE COM sucesso !")

time.sleep(3)
os.remove(zip_file_name)

try:
    shutil.rmtree(folder_to_zip)
    print(f"A pasta '{folder_to_zip}' foi excluída com sucesso.")
except Exception as e:
    print(f"Erro ao excluir a pasta '{folder_to_zip}': {str(e)}")



ende = time.time()
segundos = ende - start_time
minutos = segundos / 60

print(f"Segundos: {segundos}")
print(f"Minutos: {minutos}")
