from datetime import datetime
from tabulate import tabulate
from admin import AdminLogin, Constitution
import uuid
import os


class Voterlist:
    @classmethod
    def calculate_age(cls, dob, election_date):
        dob_date = datetime.strptime(dob, "%Y/%m/%d")
        election_year = int(election_date.split("/")[0])
        age = election_year - dob_date.year
        return age

    @classmethod
    def add_voter(cls):
        try:
            latest_election_date = Constitution.get_latest_election_date()
        except ValueError as e:
            print(e)
            return

        voter_name = input("Enter Voter's Name: ")
        dob = input("Enter Date of Birth (YYYY/MM/DD): ")
        address = input("Enter Address: ")

        age = cls.calculate_age(dob, latest_election_date)

        if age < 18:
            print("Not Eligible age.")
            return
        else:
            print("Voter is eligible to vote.")

        voter_sno = cls.generate_serial_number()
        password = cls.generate_password()

        if not os.path.exists("voterlist.txt"):
            with open("voterlist.txt", "w"):
                pass
            
        with open("voterlist.txt", "a") as file:
            file.write(f"{voter_sno}\t{voter_name}\t{dob}\t{address}\t{password}\n")

        print("Voter added successfully.")        
    @classmethod
    def delete_voter(cls, voter_sno):
        with open("voterlist.txt", "r") as file:
            lines = file.readlines()

        with open("voterlist.txt", "w") as file:
            for line in lines:
                if line.startswith(f"{voter_sno}\t"):
                    print(f"Deleted Voter: {line.strip()}")
                else:
                    file.write(line)

    @classmethod
    def edit_voter(cls, voter_sno):
        with open("voterlist.txt", "r") as file:
            lines = file.readlines()

        with open("voterlist.txt", "w") as file:
            for line in lines:
                if line.startswith(f"{voter_sno}\t"):
                    new_info = input(f"Enter new information for {line.strip()}: ")
                    file.write(f"{voter_sno}\t{new_info}\n")
                    print(f"Edited Voter: {new_info}")
                else:
                    file.write(line)

    @classmethod
    def send_email(cls, voter_email):
        
        print(f"Email sent to {voter_email}")

    @classmethod
    def show_voter_list(cls):
        with open("voterlist.txt", "r") as file:
            lines = file.readlines()
            data = [line.strip().split("\t") for line in lines]

        header = ["Voter SNO", "Name of Voter", "Date of Birth", "Address"]
        print(tabulate(data, headers=header, tablefmt="grid"))

    @classmethod
    def show_voter_list_admin(cls):
        with open("voterlist.txt", "r") as file:
            lines = file.readlines()
            data = [line.strip().split("\t") for line in lines]

        header = ["Voter SNO", "Name of Voter", "Date of Birth", "Address", "Password"]
        print(tabulate(data, headers=header, tablefmt="grid"))

    @classmethod
    def search_voter(cls, search_name, search_dob):
        with open("voterlist.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                voter_info = line.strip().split("\t")
                if search_name in voter_info[1] and search_dob in voter_info[2]:
                    print("You are in the voter list.")
                    return
            print("Not found in the voter list.")

    @classmethod
    def generate_serial_number(cls):
        if not os.path.exists("voterlist.txt"):
            with open("voterlist.txt", "w"):
                pass

        with open("voterlist.txt", "r") as file:
            lines = file.readlines()

        if lines:
            last_serial_number = int(lines[-1].split("\t")[0])
            voter_sno = last_serial_number + 1
        else:
            voter_sno = 1

        return voter_sno

        numbered_data1 = [[i + 1] + data[i] for i in range(len(data))]
        return str(len(numbered_data1) + 1)
    def generate_password():
        password = str(uuid.uuid4().int)[:8]
        return password
