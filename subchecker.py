#!/usr/bin/env python
import sys
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor as executor

# Define color variables
yellow = "\033[93m"
green = "\033[92m"
blue = "\033[94m"
red = "\033[91m"
bold = "\033[1m"
end = "\033[0m"

# Print ASCII art with correct formatting
print(blue + bold + """
 ____        _      ____ _               _             
/ ___| _   _| |__  / ___| |__   ___  ___| | _____ _ __ 
\___ \| | | | '_ \| |   | '_ \ / _ \/ __| |/ / _ \ '__|
 ___) | |_| | |_) | |___| | | |  __/ (__|   <  __/ |   
|____/ \__,_|_.__/ \____|_| |_|\___|\___|_|\_\___|_|   
                                                       
                   Coded by: Abu Ruwais/Абу Руавайс                                   
                   ---------------
""" + end)

def printer(url):
    sys.stdout.write(url.ljust(100) + "\r")
    sys.stdout.flush()
    return True

def check(out, url):
    printer("Testing: " + url)
    url = 'http://' + url
    try:
        req = requests.head(url, timeout=10)
        scode = str(req.status_code)
        if scode.startswith("2"):
            print(green + "[+] " + scode + " | Found: " + end + "[ " + url + " ]")
        elif scode.startswith("3"):
            link = req.headers['Location']
            print(yellow + "[*] " + scode + " | Redirection: " + end + "[ " + url + " ]" + yellow + " -> " + end + "[ " + link + " ]")
        elif scode.startswith("4"):
            print(blue + "[!] " + scode + " | Check: " + end + "[ " + url + " ]")

        if out:
            with open(out, 'a') as f:
                f.write(url + "\n")

        return True

    except Exception as e:
        print(red + "[!] Error: " + end + str(e))
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wordlist", help="Domains List File", type=str, required=True)
    parser.add_argument("-t", "--threads", help="Threads Number - (Default: 10)", type=int)
    parser.add_argument("-o", "--output", help="Save Results In a File", type=str)

    args = parser.parse_args()

    wordlist_file = args.wordlist
    threads = args.threads or 10
    output_file = args.output

    lines = sum(1 for _ in open(wordlist_file))
    print(blue + "[+] File: " + end + wordlist_file)
    print(blue + "[+] Length: " + end + str(lines))
    print(blue + "[+] Threads: " + end + str(threads))
    print(blue + "[+] Output: " + end + str(output_file))
    print(red + bold + "\n[+] Results:\n" + end)

    with open(wordlist_file, 'r') as urls:
        with executor(max_workers=threads) as exe:
            exe.map(lambda url: check(output_file, url.strip()), urls)

if __name__ == '__main__':
    main()