
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QLabel, QCheckBox, QSpinBox, QLineEdit, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from os import path
from subprocess import check_output,DEVNULL
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from firebase_admin import credentials, initialize_app, storage, db, delete_app

from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import psutil
import re
import time
import urllib
import requests
import json
import ctypes
import firebase_admin
import hashlib
import uuid
import json
from firebase_admin import credentials, db, initialize_app
import hashlib
import os
import random
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
from datetime import datetime, timedelta
import firebase_admin
import ssl
import time
from fake_useragent import UserAgent

import requests
import json
from bs4 import BeautifulSoup
from config.keys import *

class Security:
    def __init__(self, app1):
        self.app1 = app1
        self.serial_ref = db.reference('seriais', app=app1)
        self.session_ref = db.reference('sessions', app=app1)


    def get_machine_info(self):
        system_info = platform.uname()
        machine = system_info.node
        return machine
    
    def get_disk_serial_number(self):
        kernel32 = ctypes.windll.kernel32
        volume_serial_number = ctypes.c_ulonglong(0)
        filesystem_flags = ctypes.c_ulong(0)
        max_component_length = ctypes.c_ulong(0)
        file_system_name_buffer = ctypes.create_unicode_buffer(256)

        drive = 'C:\\'

        result = kernel32.GetVolumeInformationW(
            ctypes.create_unicode_buffer(drive),
            None,
            0,
            ctypes.pointer(volume_serial_number),
            ctypes.pointer(max_component_length),
            ctypes.pointer(filesystem_flags),
            file_system_name_buffer,
            ctypes.sizeof(file_system_name_buffer)
        )

        if result:
            serial = volume_serial_number.value
            return serial
        return None

    def get_cpu_info(self):
        system_info = platform.uname()
        cpu_info = {
            "system": system_info.system,
            "node": system_info.node,
            "release": system_info.release,
            "version": system_info.version,
            "machine": system_info.machine,
            "processor": system_info.processor
        }
        return str(cpu_info)

    def generate_serial(self, order_id, cpu_info):
        """
        Gera um serial único baseado no order_id e nas informações da CPU.
        """
        session_token = hashlib.sha256(f"{order_id}{cpu_info}".encode()).hexdigest()
        return session_token

    def register_computer(self, serial, computer_id, start_date, order_id):
        """
        Registra um computador para um serial.
        """
        serial_data = self.serial_ref.child(serial).get()

        if serial_data:
            registered_computers = serial_data.get('computers', [])
            if len(registered_computers) >= 2:
                raise Exception("Serial já foi usado em dois computadores diferentes.")
            if computer_id not in registered_computers:
                registered_computers.append(computer_id)
                self.serial_ref.child(serial).update({'computers': registered_computers})
        else:
            expiration_date = (datetime.fromisoformat(start_date) + timedelta(days=30)).isoformat()
            self.serial_ref.child(serial).set({
                'computers': [computer_id],
                'order_id_hash': serial,
                'order_id': order_id,
                'start_date': start_date,
                'expiration_date': expiration_date
            })

    def check_serial(self, serial, computer_id, start_date, order_id):
        """
        Verifica se o serial é válido para o computador.
        """
        serial_data = self.serial_ref.child(serial).get()

        if not serial_data:
            self.register_computer(serial, computer_id, start_date, order_id)
            serial_data = self.serial_ref.child(serial).get()

        start_date = serial_data.get('start_date')
        expiration_date = serial_data.get('expiration_date')
        if start_date and expiration_date:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
            expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M:%S')
            if expiration_date_obj <= start_date_obj:
                if expiration_date_obj <= datetime.now():
                    return False

        registered_computers = serial_data.get('computers', [])
        return computer_id in registered_computers or len(registered_computers) < 2

    def get_computer_id(self):
        """
        Gera um ID único para o computador atual baseado nas informações da CPU e do disco.
        """
        cpu_info = self.get_cpu_info()
        disk_serial = self.get_disk_serial_number()
        if cpu_info and disk_serial:
            computer_id = hashlib.sha256(f"{cpu_info}{disk_serial}".encode()).hexdigest()
            return computer_id
        return None

    def get_existing_session_token(self, order_id):
        session_data = self.session_ref.child(order_id).get()
        if session_data:
            return session_data.get('session_token')
        return None

    def create_session(self, order_id, key):
        """
        Cria uma nova sessão com as informações fornecidas.
        """
        session_data = f"{order_id}"
        session_token = hashlib.sha256(session_data.encode()).hexdigest()
        self.session_ref.child(order_id).set({
            'session_token': session_token,
            'order_id': order_id,
            'key': key
        })
        return session_token

    def get_or_create_session(self, order_id, key):
        """
        Obtém uma sessão existente ou cria uma nova.
        """
        session_token = self.get_existing_session_token(order_id)
        if session_token:
            return session_token
        session_token = self.create_session(order_id, key)
        return session_token

    def set_hardware_id(self, license_key, hardware_id):
        url = "https://dev.sellix.io/v1/products/licensing/hardware_id"

        payload = {
            "product_id": "666e049aa6efd",
            "key": license_key,
            "hardware_id": hardware_id
        }
        headers = {
            "Authorization": f"{SELLIX_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        return response
    
    def check_license(self, license_key, hardware_id):
        url = "https://dev.sellix.io/v1/products/licensing/check"

        payload = {
            "product_id": "666e049aa6efd",
            "key": license_key,
            "hardware_id": hardware_id
        }
        headers = {
            "Authorization": f"{SELLIX_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        return response

    def check_license_time(self, license_key, hardware_id):
        url = "https://dev.sellix.io/v1/products/licensing/check"

        payload = {
            "product_id": "666e049aa6efd",
            "key": license_key,
            "hardware_id": hardware_id
        }
        headers = {
            "Authorization": f"{SELLIX_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        json_data= response.json()
        created_at = json_data['data']['license']['created_at']
        created_at_dt = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        created_at_iso = created_at_dt.isoformat()
        return created_at_iso

    def get_order_id_by_serial(self, serial, hardware_id):
        headers = {
            'Authorization': f'Bearer {SELLIX_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "product_id": '666e049aa6efd',
            "key": serial,
            "hardware_id": hardware_id
        }
        
        response = requests.post('https://dev.sellix.io/v1/products/licensing/check', json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data and 'data' in data and 'license' in data['data']:
                return data['data']['license']['invoice_id']
            else:
                return "Invalid response structure or no data found."
        else:
            return f"Error: {response.status_code}, {response.text}"

    def set_hardware_id(self, license_key, hardware_id):
        url = "https://dev.sellix.io/v1/products/licensing/hardware_id"

        payload = {
            "product_id": "666e049aa6efd",
            "key": license_key,
            "hardware_id": hardware_id
        }
        headers = {
            "Authorization": f"{SELLIX_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        return response
