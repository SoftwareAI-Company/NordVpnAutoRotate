from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QLabel, QCheckBox, QSpinBox, QLineEdit, QWidget
from PyQt5.uic import loadUi

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
from CoreSecurity.keys.keys import *
from CoreSecurity.Security import *

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

        self.user_agent_rotator = UserAgent()

    def set_headers(self):
        useragent_pick = self.user_agent_rotator.random
        headers = {
            'User-Agent': useragent_pick,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        return headers

    def disconect_nord(self):
        try:
            option_1_path = 'C:/Program Files/NordVPN'
            subprocess.Popen(["nordvpn", "-d"], shell=True, cwd=option_1_path, stdout=DEVNULL)
        except:
            pass 

    def get_nordvpn_servers_location_and_region(self, location, region=None):
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

    def get_nordvpn_servers(self):
        try:
            serverlist = BeautifulSoup(requests.get("https://api.nordvpn.com/v1/servers?limit=10000").content,"html.parser")
            site_json=json.loads(serverlist.text)
            filtered_servers = {'windows_names': [], 'linux_names': []}

            for specific_dict in site_json:
                try:
                    groups = specific_dict.get('groups', [])  # Verifica se 'groups' está presente
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

    def get_monitor(self):
        while True:
            ip_check_websites = [
                'https://ipinfo.io/json',
                'http://ipapi.co/json',
                'https://ipwhois.app/json',
                'https://get.geojs.io/v1/ip/geo.json', 
                'http://ip-api.com/json/',
            ]
            random.shuffle(ip_check_websites)  
            headers = self.set_headers()
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
                    organizacao = data.get('org')
                    fuso_horario = data.get('timezone')
                    return ip, cidade, regiao, pais, fuso_horario, organizacao
                except Exception as error:
                    print(f"Error retrieving {website_pick} monitor info: {error}")

    def load_benchmark_data(self):
        try:
            security = Security(app1=app1)
            respostaname_machine = security.get_machine_info()
            ref = db.reference(f'benchmark_data_users/{respostaname_machine}')
            data = ref.get()
            if data:
                data['total_rotations'] = int(data.get('total_rotations', 0))  # Garantir que é um inteiro
                data['time_spent'] = float(data.get('time_spent', 0))  # Garantir que é um float
                if isinstance(data['locations_used'], str):  # Verificar se locations_used é uma string JSON
                    try:
                        data['locations_used'] = json.loads(data['locations_used'])
                    except json.JSONDecodeError:
                        data['locations_used'] = {}
                return data
            else:
                return {
                    'total_rotations': 0,
                    'time_spent': 0,
                    'locations_used': {}
                }
        except Exception as e:
            print(f"Error loading data: {e}")
            return {
                'total_rotations': 0,
                'time_spent': 0,
                'locations_used': {}
            }

    def update_benchmark_data(self):
        security = Security(app1=app1)
        respostaname_machine = security.get_machine_info()

        # Carregar dados existentes
        ref1 = db.reference(f'benchmark_data_users/{respostaname_machine}')
        existing_data = ref1.get() or {
            'total_rotations': 0,
            'time_spent': 0,
            'locations_used': {}
        }

        # Atualizar dados existentes
        self.benchmark_data['total_rotations'] = int(existing_data.get('total_rotations', 0)) + 1
        self.benchmark_data['time_spent'] += float(existing_data.get('time_spent', 0))

        ip, cidade, regiao, pais, fuso_horario, organizacao = self.get_monitor()
        self.benchmark_data['locations_used'][regiao] = self.benchmark_data['locations_used'].get(regiao, 0) + 1

        # Salvar dados atualizados
        ref1.set(self.benchmark_data)

        # Atualizar global_benchmark
        global_ref = db.reference('global_benchmark')
        global_data = global_ref.child(respostaname_machine).get() or {
            'total_rotations': 0,
            'time_spent': 0,
            'locations_used': {}
        }

        global_data['total_rotations'] = int(global_data.get('total_rotations', 0)) + 1
        global_data['time_spent'] += float(global_data.get('time_spent', 0))

        for location, count in self.benchmark_data['locations_used'].items():
            global_data['locations_used'][location] = global_data['locations_used'].get(location, 0) + count

        global_ref.child(respostaname_machine).set(global_data)

    def saved_settings_check(self):
        print("\33[33mTrying to load saved settings...\33[0m")
        try:
            instructions = json.load(open("settings_nordvpn.txt"))
        except FileNotFoundError:
            raise Exception("\n\nSaved settings not found.\n"
                            "Run initialize_VPN() first and save the settings on your hard drive or store it into a Python variable.")
        else:
            print("\33[33mSaved settings loaded!\n\33[0m")
        return instructions

    def initialize_VPN(self, area_input):
        stored_settings = 0
        save = 0
        skip_settings = 0

        ###load stored settings if needed and set input_needed variables to zero if settings are provided###
        windows_pause = 3
        additional_settings_needed = 1
        additional_settings_list = list()

        input_needed = 2
        windows_pause = 8

        ###performing system check###
        opsys = platform.system()

        ##windows##
        if opsys == "Windows":
            option_1_path = 'C:/Program Files/NordVPN'
            option_2_path = 'C:/Program Files (x86)/NordVPN'
            custom_path = str()
            if path.exists(option_1_path) == True:
                cwd_path = option_1_path
            elif path.exists(option_2_path) == True:
                cwd_path = option_2_path
            else:
                custom_path = input("\x1b[93mIt looks like you've installed NordVPN in an uncommon folder. Would you mind telling me which folder? (e.g. D:/customfolder/nordvpn)\x1b[0m")
                while path.exists(custom_path) == False:
                    custom_path = input("\x1b[93mI'm sorry, but this folder doesn't exist. Please double-check your input.\x1b[0m")
                while os.path.isfile(custom_path+"/NordVPN.exe") == False:
                    custom_path = input("\x1b[93mI'm sorry, but the NordVPN application is not located in this folder. Please double-check your input.\x1b[0m")
                cwd_path = custom_path

            # checking nordvpn service is running
            check_service = "nordvpn-service.exe" in (p.name() for p in psutil.process_iter())
            if check_service is False:
                raise Exception("NordVPN service hasn't been initialized, please start this service in [task manager] --> [services] and restart your script")

            # start NordVPN app and disconnect from VPN service if necessary
            open_nord_win = subprocess.Popen(["nordvpn", "-d"], shell=True, cwd=cwd_path, stdout=DEVNULL)
            while ("NordVPN.exe" in (p.name() for p in psutil.process_iter())) == False:
                time.sleep(windows_pause)
            open_nord_win.kill()
            self.location.emit(f"NordVPN app launched.")

        else:
            raise Exception("I'm sorry, NordVPN switcher only works for Windows and Linux machines.")

        diretorio_script = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(diretorio_script,'config', 'countrylist.txt')

        with open(file_path, 'r') as file:
            areas_list = file.read().split('\n')
            country_dict = {'countries':areas_list[0:60],'europe': areas_list[0:36], 'americas': areas_list[36:44],
                            'africa east india': areas_list[49:60],'asia pacific': areas_list[49:60],
                            'regions australia': areas_list[60:65],'regions canada': areas_list[65:68],
                            'regions germany': areas_list[68:70], 'regions india': areas_list[70:72],
                            'regions united states': areas_list[72:87],'special groups':areas_list[87:len(areas_list)]}

        ##provide input if needed##
        flag = False
        while input_needed > 0:
            if input_needed == 2:
                self.location.emit(f"You've entered a list of connection options. Checking list...")

                try:
                    settings_servers = [area.lower() for area in area_input]
                    settings_servers = ",".join(settings_servers)
                except TypeError:
                    raise Exception("I expected a list here. Are you sure you've not entered a string or some other object?\n ")

            else:
                if area_input == 'complete rotation':
                    settings_servers = 'complete rotation'

            if opsys == "Windows":
                nordvpn_command = ["nordvpn", "-c"]
            if opsys == "Linux":
                nordvpn_command = ["nordvpn", "c"]
            #create sample of regions from input.#
            #1. if quick connect#
            if settings_servers == "quick":
                if input_needed == 1:
                    quickconnect_check = input("\nYou are choosing for the quick connect option. Are you sure? (y/n)\n")
                    if 'y' in quickconnect_check:
                        sample_countries = [""]
                        input_needed = 0
                        pass
                if input_needed == 2:
                    sample_countries = [""]
                    input_needed = 0
                else:
                    print("\nYou are choosing for the quick connect option.\n")
            #2. if completely random rotation
            elif settings_servers == 'complete rotation':
                print("\nFetching list of all current NordVPN servers...\n")
                for i in range(120):
                    try:
                        filtered_servers = self.get_nordvpn_servers()
                        if opsys == "Windows":
                            nordvpn_command.append("-n")
                            sample_countries = filtered_servers['windows_names']
                        else:
                            sample_countries = filtered_servers['linux_names']
                    except:
                        time.sleep(0.5)
                        continue
                    else:
                        input_needed = 0
                        break
                else:
                    raise Exception("\nI'm unable to fetch the current NordVPN serverlist. Check your internet connection.\n")

            #3. if provided specific servers. Notation differs for Windows and Linux machines, so two options are checked (first is Windows, second is Linux#
            elif "#" in settings_servers or re.compile(r'^[a-zA-Z]+[0-9]+').search(settings_servers.split(',')[0]) is not None:
                if opsys == "Windows":
                    nordvpn_command.append("-n")
                sample_countries = [area.strip() for area in settings_servers.split(',')]
                input_needed = 0
            else:
                #3. If connecting to some specific group of servers#
                if opsys == "Windows":
                    nordvpn_command.append("-g")
                #3.1 if asked for random sample, pull a sample.#
                if "random" in settings_servers:
                    #determine sample size#
                    samplesize = int(re.sub("[^0-9]", "", settings_servers).strip())
                    #3.1.1 if asked for random regions within country (e.g. random regions from United States,Australia,...)#
                    if "regions" in settings_servers:
                        try:
                            sample_countries = country_dict[re.sub("random", "", settings_servers).rstrip('0123456789.- ').lower().strip()]
                            input_needed = 0
                        except:
                            input("\n\nThere are no specific regions available in this country, please try again.\nPress enter to continue.\n")
                            if input_needed == 2:
                                input_needed = 1
                                continue
                        if re.compile(r'[^0-9]').search(settings_servers.strip()):
                            sample_countries = random.sample(sample_countries, samplesize)
                    #3.1.2 if asked for random countries within larger region#
                    elif any(re.findall(r'europe|americas|africa east india|asia pacific', settings_servers)):
                        larger_region = country_dict[re.sub("random|countries", "", settings_servers).rstrip('0123456789.- ').lower().strip()]
                        sample_countries = random.sample(larger_region,samplesize)
                        input_needed = 0
                    #3.1.3 if asked for random countries globally#
                    else:
                        if re.compile(r'[^0-9]').search(settings_servers.strip()):
                            sample_countries = random.sample(country_dict['countries'], samplesize)
                            input_needed = 0
                        else:
                            sample_countries = country_dict['countries']
                            input_needed = 0
                #4. If asked for specific region (e.g. europe)#
                elif settings_servers in country_dict.keys():
                    sample_countries = country_dict[settings_servers]
                    input_needed = 0
                #5. If asked for specific countries or regions (e.g.netherlands)#
                else:
                    #check for empty input first.#
                    if settings_servers == "":
                        input("\n\nYou must provide some kind of input.\nPress enter to continue and then type 'help' to view the available options.\n")
                        if input_needed == 2:
                            input_needed = 1
                            continue
                    else:
                        sample_countries = [area.strip() for area in settings_servers.split(',')] #take into account possible superfluous spaces#
                        approved_regions = 0
                        for region in sample_countries:
                            if region in [area.lower() for area in areas_list]:
                                approved_regions = approved_regions + 1
                                pass
                            else:
                                if input_needed == 2:
                                    input_needed = 1
                                    continue
                        if approved_regions == len(sample_countries):
                            input_needed = 0

        ##fetch current ip to prevent ip leakage when rotating VPN##
        for i in range(59):
            if flag == True:
                break
            try:
                og_ip, cidade, regiao, pais, fuso_horario, organizacao = self.get_monitor() 
            except ConnectionAbortedError:
                time.sleep(1)
                continue
            else:
                break
        else:
            raise Exception("Can't fetch current ip, even after retrying... Check your internet connection.")

        ##if user does not use preloaded settings##
        if "instructions" not in locals():
            #1.add underscore if spaces are present on Linux os#
            for number,element in enumerate(sample_countries):
                if element.count(" ") > 0 and opsys == "Linux":
                        sample_countries[number] = re.sub(" ","_",element)
            else:
                pass
            #2.create instructions dict object#
            instructions = {'opsys':opsys,'command':nordvpn_command,'settings':sample_countries,'original_ip':og_ip}
            if opsys == "Windows":
                instructions['cwd_path'] = cwd_path

            #3.save the settings if requested into .txt file in project folder#
            if save == 1:
                print("\nSaving settings in project folder...\n")
                try:
                    os.remove("settings_nordvpn.txt")
                except FileNotFoundError:
                    pass
                instructions_write = json.dumps(instructions)
                f = open("settings_nordvpn.txt", "w")
                f.write(instructions_write)
                f.close()

        self.location.emit(f"Done!")
        return instructions

    def run(self):
        self.progress.emit(1)
        security = Security(app1=app1)
        key = self.nvar_keyy
        hardware_id = security.get_computer_id()
        order_id = security.get_order_id_by_serial(key, hardware_id)
        security.set_hardware_id(order_id, hardware_id)
        session_token = security.get_or_create_session(order_id, key)
        cpu_info = security.get_cpu_info()
        serial = security.generate_serial(session_token, cpu_info)
        computer_id = security.get_computer_id()
        start_date = security.check_license_time(key, computer_id)
        is_valid = security.check_serial(serial, computer_id, start_date, order_id)

        self.location.emit(f"CHECK YOU KEY WAIT.")
        time.sleep(1)
        self.location.emit(f"CHECK YOU KEY WAIT..")
        time.sleep(1)
        self.location.emit(f"CHECK YOU KEY WAIT...")
        time.sleep(1)
        self.location.emit(f"CHECK YOU KEY WAIT....")
        if is_valid == True:
            self.location.emit(f"YOU KEY IS VALID.")
            time.sleep(2)

            start_time = time.time()

            vpn_options = {
                "America/New_York": ["New York,Manassas"],
                "America/Chicago": ["Chicago,Saint Louis"],
                "America/Denver": ["Denver,Chicago"],
                "America/Los_Angeles": ["Los Angeles,Phoenix"],
                "America/Seattle": ["Seattle,Chicago"],
                "America/Salt_Lake_City": ["Chicago,Denver"],
                "America/San_Francisco": ["San Francisco,Los Angeles"],
                "America/Dallas": ["Dallas,Chicago"],
                "America/Kansas_City": ["Chicago,Saint Louis"],
                "America/Saint_Louis": ["Saint Louis,Dallas"],
                "America/Atlanta": ["Atlanta,Charlotte"],
                "America/Charlotte": ["Charlotte,Manassas,New York"],
                "America/Miami": ["Miami,Atlanta,Charlotte"],
                "America/Manassas": ["Manassas,New York"],
                "America/Buffalo": ["Buffalo,New York"],
                "America/Phoenix": ["Phoenix,Los Angeles"],
                "America/Toronto": ["Toronto,Buffalo"],
                "America/Vancouver": ["Atlanta,Seattle"],
                "Europe/Paris": ["Miami,Buffalo"],
                "North_America/Ottawa": ["Salt Lake City,New York,Phoenix"],
                "North_America/Havana": ["Phoenix,Seattle"],
            }

            for i in range(self.rotation_count):
                if not self._is_running:
                    break

                self.progress.emit(int(100 * i / self.rotation_count))
                
                if self.rotate_in_usa:
                    timezone = random.choice(list(vpn_options.keys()))
                    vpn_options_for_timezone = vpn_options.get(timezone, [])
                    vpn_option = random.choice(vpn_options_for_timezone)
                    print(vpn_options_for_timezone)
                    print(vpn_option)
                    self.location.emit(f'{[vpn_option]}')
                    vpn_instruction = self.initialize_VPN(area_input=[vpn_option])
                if self.rotate_complete:    
                    self.location.emit('Rotate complete')
                    vpn_instruction = self.initialize_VPN(area_input='complete rotation')

                if self.rotate_in_canada:    
                    self.location.emit('Rotate in CANADA')
                    vpn_instruction = self.initialize_VPN(area_input=["Vancouver,Montreal,Toronto"])

                self.benchmark_data['total_rotations'] += 1

                instructions = vpn_instruction
                google_check = 0
                if instructions is None:
                    instructions = self.saved_settings_check()

                opsys = instructions['opsys']
                command = instructions['command']
                settings = instructions['settings']
                og_ip = instructions['original_ip']

                if opsys == "Windows":
                    cwd_path = instructions['cwd_path']

                for i in range(2):
                    try:
                        current_ip, cidade, regiao, pais, fuso_horario, organizacao = self.get_monitor() 
                    except urllib.error.URLError:
                        self.location.emit(f"Can't fetch current ip. Retrying...")
                    
                        time.sleep(10)
                        continue
                    else:
                        self.location.emit(f"Your current ip-address is: {current_ip}")

                        time.sleep(2)
                        break
                else:
                    self.location.emit(f"Can't fetch current ip, even after retrying... Check your internet connection.")
                    
                if not self._is_running:
                    break
                for i in range(5):
                    if len(settings) > 1:
                        settings_pick = list([random.choice(settings)])
                    else:
                        settings_pick = settings

                    input = command + settings_pick

                    if settings[0] == "":
                        print("\nConnecting you to the best possible server (quick connect option)...")
                    else:
                        self.location.emit(f"Connecting: {settings_pick[0]}")
                            
                    if not self._is_running:
                        break
        
                    try:
                        if opsys == "Windows":
                            new_connection = subprocess.Popen(input, shell=True, cwd=cwd_path)
                            new_connection.wait(220)
                        else:
                            new_connection = check_output(input)
                            print("Found a server! You're now on "+re.search('(?<=You are connected to )(.*)(?=\()', str(new_connection))[0].strip())
                    except:
                        self.location.emit(f"An unknown error occurred")

                    if not self._is_running:
                        break
                    for i in range(12):
                        try:
                            new_ip, cidade, regiao, pais, fuso_horario, organizacao = self.get_monitor() 
                        except:
                            time.sleep(5)
                            continue
                        else:
                            if new_ip in [current_ip,og_ip]:
                                time.sleep(5)
                                continue
                            else:
                                break
                    else:
                        pass

                    if new_ip in [current_ip,og_ip]:
                        print("ip-address hasn't changed. Retrying...\n")
                        time.sleep(10)
                        continue
                    else:
                        self.location.emit(f"Conected! Enjoy your new server.")
                        time.sleep(3)

                    if not self._is_running:
                        break

                    if google_check == 1:
                        print("\n\33[33mPerforming captcha-check on Google search and Youtube...\n"
                            "---------------------------\33[0m")
                        try:
                            google_search_check = BeautifulSoup(
                                requests.get("https://www.google.be/search?q=why+is+python+so+hard").content,"html.parser")
                            youtube_video_check = BeautifulSoup(
                                requests.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ").content,"html.parser")

                            google_captcha = google_search_check.find('div',id="recaptcha")
                            youtube_captcha = youtube_video_check.find('div', id = "recaptcha")

                            if None not in (google_captcha,youtube_captcha):
                                print("Google throws a captcha. I'll pick a different server...")
                                time.sleep(5)
                                continue
                        except:
                            print("Can't load Google page. I'll pick a different server...")
                            time.sleep(5)
                            continue
                        else:
                            print("Google and YouTube don't throw any Captcha's: \33[92m\N{check mark}\33[0m")
                            break
                    else:
                        break
                self.benchmark_data['time_spent'] += time.time() - start_time
                self.update_benchmark_data()

                for _ in range(self.interval):
                    if not self._is_running:
                        self.disconect_nord()
                        self.location.emit(f"N-V-A-R Stop")
                        break
                    time.sleep(1)
            self.location.emit(f"N-V-A-R Stop")    
            self.progress.emit(100)
            self.finished.emit()

        elif is_valid == False:
            self.location.emit(f"YOU KEY IS Expired.")
            time.sleep(2)
        else:
            # Registra o computador para o serial
            try:
                security.register_computer(serial, computer_id, start_date)
                self.location.emit(f"YOU KEY IS Registred. Please try new")
                time.sleep(2)
            except Exception as e:
                print(f"Erro: {e}")

    def stop(self):
        self._is_running = False

