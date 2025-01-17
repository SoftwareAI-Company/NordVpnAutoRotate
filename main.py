from ui.main_window_ui import Ui_MainWindow
from ui.benchmark_window_ui import Ui_BenchmarkWindow
from ui.global_benchmark_window_ui import Ui_GlobalBenchmarkWindow

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QLabel, QCheckBox, QSpinBox, QLineEdit, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from os import path
from subprocess import check_output, DEVNULL
import subprocess
import psutil
import re
import time
import urllib
import requests
import json
import os
import random
import sys
import threading
import ssl
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from datetime import datetime, timedelta
from fake_useragent import UserAgent
from firebase_admin import credentials, initialize_app, storage, db

from config.keys import *
from config.Security import *

software_names = ["chrome"]
operating_systems = ["windows", "linux"]
user_agent_rotator = UserAgent()

class Balanceamento_de_vpn:
    def __init__(self, items):
        self.items = items
        self.counter = [0] * len(items)

    def selecionar(self):
        min_count = min(self.counter)
        candidatos = [i for i, count in enumerate(self.counter) if count == min_count]
        selecionado = random.choice(candidatos)
        self.counter[selecionado] += 1
        return self.items[selecionado]

def set_headers(user_agent_rotator):
    useragent_pick = user_agent_rotator.random
    headers = {
        'User-Agent': useragent_pick,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    return headers

def get_monitor():
    ip_check_websites = [
        'https://ipinfo.io/json',
        'http://ipapi.co/json',
        'https://ipwhois.app/json',
        'https://get.geojs.io/v1/ip/geo.json', 
        'http://ip-api.com/json/',
    ]
    random.shuffle(ip_check_websites)  
    headers = set_headers(user_agent_rotator)
    for website_pick in ip_check_websites:
        try:
            request_currentip = urllib.request.Request(url=website_pick, headers=headers)
            context = ssl._create_unverified_context()  # Bypass SSL verification temporarily
            response = urllib.request.urlopen(request_currentip, context=context)
            data = json.loads(response.read().decode('utf-8'))
            ip = data.get('ip')
            cidade = data.get('city')
            regiao = data.get('region')
            pais = data.get('country')
            fuso_horario = data.get('timezone')
            organizacao = data.get('org')
            return ip, cidade, regiao, pais, fuso_horario, organizacao
        except Exception as error:
            print(f"Error retrieving {website_pick} monitor info: {error}")

def saved_settings_check():
    print("\33[33mTrying to load saved settings...\33[0m")
    try:
        with open("settings_nordvpn.txt") as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception("\n\nSaved settings not found.\n"
                        "Run initialize_VPN() first and save the settings on your hard drive or store it into a Python variable.")
    
def get_nordvpn_servers_location_and_region(location, region=None):
    try:
        serverlist = requests.get("https://api.nordvpn.com/v1/servers?limit=10000").content
        site_json = json.loads(serverlist)
        filtered_servers = {'windows_names': [], 'linux_names': []}

        for specific_dict in site_json:
            try:
                locations = specific_dict.get('locations', [])
                for loc in locations:
                    country_info = loc.get('country', {})
                    country = country_info.get('name', '')
                    city_info = country_info.get('city', {})
                    city = city_info.get('name', '')

                    if isinstance(country, str) and location.lower() in country.lower():
                        if region:
                            if isinstance(city, str) and region.lower() in city.lower():
                                print(f"Found match for location: {location} and region: {region} in city: {city}")  # Debug message
                                groups = specific_dict.get('groups', [])
                                for group in groups:
                                    if group['title'] == 'Standard VPN servers':
                                        filtered_servers['windows_names'].append(specific_dict['name'])
                                        filtered_servers['linux_names'].append(specific_dict['domain'].split('.')[0])
                                        print(f"Added server: {specific_dict['name']}")  # Debug message
                                        break  # Exit the group loop if you find the desired category
                        else:
                            print(f"Found match for location: {location}")  # Debug message
                            groups = specific_dict.get('groups', [])
                            for group in groups:
                                if group['title'] == 'Standard VPN servers':
                                    filtered_servers['windows_names'].append(specific_dict['name'])
                                    filtered_servers['linux_names'].append(specific_dict['domain'].split('.')[0])
                                    print(f"Added server: {specific_dict['name']}")  # Debug message
                                    break  # Exit the group loop if you find the desired category
            except KeyError as e:
                print(f"KeyError: {e}")  # Debug message

        return filtered_servers
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_nordvpn_servers():
    try:
        serverlist = BeautifulSoup(requests.get("https://api.nordvpn.com/v1/servers?limit=10000").content,"html.parser")
        site_json=json.loads(serverlist.text)
        filtered_servers = {'windows_names': [], 'linux_names': []}

        for specific_dict in site_json:
            try:
                groups = specific_dict.get('groups', [])  # Verifica se 'groups' est\u00e1 presente
                for group in groups:
                    if group['title'] == 'Standard VPN servers':
                        filtered_servers['windows_names'].append(specific_dict['name'])
                        filtered_servers['linux_names'].append(specific_dict['domain'].split('.')[0])
                        break  # Exit the group loop if you find the desired category
            except KeyError:
                pass  # Ignore dictionaries that do not have the 'groups' or 'title' key

        return filtered_servers
    except:
        pass


def disconnect_nord():
    try:
        option_1_path = 'C:/Program Files/NordVPN'
        subprocess.Popen(["nordvpn", "-d"], shell=True, cwd=option_1_path, stdout=DEVNULL)
    except:
        pass 

# Main Application Logic
class RotateVpnThread(QThread):
    progress = pyqtSignal(int)
    location = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, rotation_count, interval, rotate_in_usa, rotate_in_canada, rotate_in_complete, nvar_key):
        super().__init__()
        self.rotation_count = rotation_count
        self.interval = interval
        self.rotate_in_usa = rotate_in_usa
        self.rotate_in_canada = rotate_in_canada
        self.rotate_complete = rotate_in_complete
        self.nvar_keyy = nvar_key
        self.benchmark_data = self.load_benchmark_data()
        self._is_running = True

    def load_benchmark_data(self):
        return {
            'total_rotations': 0, 
            'time_spent': 0, 
            'locations_used': {}
        }

    def run(self):
        self.progress.emit(1)
        # Other operations...

    def stop(self):
        self._is_running = False

# Main Window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Nord Vpn Auto Rotate')
        # Setup and connections...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())