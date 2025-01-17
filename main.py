from ui.main_window_ui import Ui_MainWindow
from ui.benchmark_window_ui import Ui_BenchmarkWindow
from ui.global_benchmark_window_ui import Ui_GlobalBenchmarkWindow

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QLabel, QCheckBox, QSpinBox, QLineEdit, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from os import path
from subprocess import check_output, DEVNULL
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from firebase_admin import credentials, initialize_app, storage, db, delete_app

import subprocess
import psutil
import re
import time
import urllib
import requests
import json
import ctypes
import hashlib
import uuid
import os
import random
import sys
import threading
from datetime import datetime, timedelta
import ssl
from fake_useragent import UserAgent

from config.keys import *
from config.Security import *

software_names = ["chrome"]
operating_systems = ["windows", "linux"]
user_agent_rotator = UserAgent()


class VPNBalancer:
    def __init__(self, items):
        self.items = items
        self.counter = [0] * len(items)

    def select(self):
        min_count = min(self.counter)
        candidates = [i for i, count in enumerate(self.counter) if count == min_count]
        selected = random.choice(candidates)
        self.counter[selected] += 1
        return self.items[selected]


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
    # Refatorado para tratamento de exceções
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
            city = data.get('city')
            region = data.get('region')
            country = data.get('country')
            organization = data.get('org')
            timezone = data.get('timezone')
            return ip, city, region, country, timezone, organization
        except Exception as error:
            print(f"Error retrieving {website_pick} monitor info: {error}")

# Continue com suas outras funções e classes aqui.