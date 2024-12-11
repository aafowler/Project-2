
import tkinter as tk
from tkinter import ttk
import csv

class VotingApp:
    def __init__(self, master):
        self.master = master

        self.name_label = ttk.Label(master, text="Name:")
        self.name_label.grid(row=0, padx=55, pady=5, sticky='w')

        self.name_entry = ttk.Entry(master) 
        self.name_entry.grid(row=0, padx=115, pady=5, sticky='w')

        self.voter_id_label = ttk.Label(master, text="Voter ID:")
        self.voter_id_label.grid(row=1,padx=55, pady=5,sticky='w')

        self.voter_id_entry = ttk.Entry(master)
        self.voter_id_entry.grid(row=1, padx=115, pady=5, sticky='w')

        self.candidate_var = tk.StringVar(value="None")

        self.candidate1_radio = ttk.Radiobutton(master, text="Joe Schmoe", variable=self.candidate_var, value="Joe Schmoe")
        self.candidate1_radio.grid(row=2,  padx=110, pady=5, sticky='w')

        self.candidate2_radio = ttk.Radiobutton(master, text="John Smith", variable=self.candidate_var, value="John Smith")
        self.candidate2_radio.grid(row=3,  padx=110, pady=5, sticky='w')

        self.submit_button = ttk.Button(master, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=4,  padx=70, pady=5, sticky ='w')

        self.new_voter_button = ttk.Button(master, text="New Voter", command=self.reset_gui)
        self.new_voter_button.grid(row=4, padx=150, pady=5, sticky ='w')

        self.error_label = ttk.Label(master, text="", foreground="red")
        self.error_label.grid(row=5, columnspan=2, padx=5, pady=5)

        self.success_label = ttk.Label(master, text="", foreground="green")
        self.success_label.grid(row=6, columnspan=2, padx=5, pady=5)

        self.result_label = ttk.Label(master, text="")
        self.result_label.grid(row=10, padx=120, pady=5, sticky='w')

        self.update_vote_counts()
    
    def reset_gui(self):
        self.name_entry.delete(0, tk.END)
        self.voter_id_entry.delete(0, tk.END)
        self.candidate_var.set("None")
        self.error_label.config(text="")
        self.success_label.config(text="")

    def update_vote_counts(self):
        try:
            with open('votes.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                votes = [row[2] for row in reader if len(row) > 2]
            
            counts = {}
            for vote in votes:
                counts[vote] = counts.get(vote, 0) + 1
            
            result_text = ""
            for candidate, count in counts.items():
                result_text += f"{candidate}: {count}\n"
            
            self.result_label.config(text=result_text)

        except FileNotFoundError:
            self.result_label.config(text="No votes recorded yet.")
        except Exception as e:
            self.result_label.config(text=f"An error occurred: {e}")
    def submit_data(self):
        name = self.name_entry.get()
        voter_id = self.voter_id_entry.get()
        selected_candidate = self.candidate_var.get()

        if not name or not voter_id or selected_candidate == "None":
            self.error_label.config(text="Please fill all the fields.")
            return

        if not isinstance(name, str) or name.count(" ") != 1:
            self.error_label.config(text="Name is not valid. Please enter a string with one space.")
            return

        if not voter_id.isdigit() or len(voter_id) != 4:
            self.error_label.config(text="Your voter Id is not valid please try again", foreground="red")
            return
        
        self.error_label.config(text="")

        try:
            with open('votes.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                existing_voter_ids = [row[1] for row in reader]
            
            if voter_id in existing_voter_ids:
                self.error_label.config(text="Voter ID already exists. Please try again.", foreground="red")
                return

            with open('votes.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, voter_id, selected_candidate])
            self.success_label.config(text="Vote submitted successfully!")

        except FileNotFoundError:
            with open('votes.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, voter_id, selected_candidate])
            self.success_label.config(text="Vote submitted successfully!")

        self.update_vote_counts()

