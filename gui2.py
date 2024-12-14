
import tkinter as tk
from tkinter import ttk
import csv

class VotingApp:
    def __init__(self, master):
        self.master = master
        #Name Label
        self.name_label = ttk.Label(master, text='Name:')
        self.name_label.grid(row=0, padx=80, pady=5, sticky='w')
        #Name Entry Box
        self.name_entry = ttk.Entry(master) 
        self.name_entry.grid(row=0, padx=140, pady=5, sticky='w')
        #Voter ID Label
        self.voter_id_label = ttk.Label(master, text='Voter ID:')
        self.voter_id_label.grid(row=1,padx=80, pady=5,sticky='w')
        #Voter ID Entry Box
        self.voter_id_entry = ttk.Entry(master)
        self.voter_id_entry.grid(row=1, padx=140, pady=5, sticky='w')
        #Gives candidates a variable
        self.candidate_var = tk.StringVar(value='None')
        #Set candidate radio buttons
        self.candidate1_radio = ttk.Radiobutton(master, text='Joe Schmoe', variable=self.candidate_var, value='Joe Schmoe')
        self.candidate1_radio.grid(row=2,  padx=135, pady=5, sticky='w')

        self.candidate2_radio = ttk.Radiobutton(master, text='John Smith', variable=self.candidate_var, value='John Smith')
        self.candidate2_radio.grid(row=3,  padx=135, pady=5, sticky='w')
        #Button to enter radio selections using the submit function
        self.submit_button = ttk.Button(master, text='Submit', command=self.submit_data)
        self.submit_button.grid(row=4,  padx=95, pady=5, sticky ='w')
        #Button that clears all fields using the reset function
        self.new_voter_button = ttk.Button(master, text='New Voter', command=self.reset_gui)
        self.new_voter_button.grid(row=4, padx=175, pady=5, sticky ='w')
        #Input error explaination button
        self.error_label = ttk.Label(master, text='', foreground='red')
        self.error_label.grid(row=5, padx=120, pady=5, sticky='w')
        #Label to say input worked
        self.success_label = ttk.Label(master, text='', foreground='green')
        self.success_label.grid(row=6, padx=100, pady=5, sticky='w')
        #Label to show total votes per candidate 
        self.result_label = ttk.Label(master, text='')
        self.result_label.grid(row=10, padx=140, pady=5, sticky='w')
        #Calls function to update result_label
        self.update_vote_counts()
    
    def reset_gui(self):
        #Clears all selections
        self.name_entry.delete(0, tk.END)
        self.voter_id_entry.delete(0, tk.END)
        self.candidate_var.set('None')
        self.error_label.config(text='')
        self.success_label.config(text='')

    def update_vote_counts(self):
        try:
            #Opens csv and creates variable to count votes
            with open('votes.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                votes = [row[2] for row in reader if len(row) > 2]
            #Adds total of each vote
            counts = {}
            for vote in votes:
                counts[vote] = counts.get(vote, 0) + 1
            #Creates the text for result_label using the count
            result_text = ""
            for candidate, count in counts.items():
                result_text += f"{candidate}: {count}\n"
            
            self.result_label.config(text=result_text)
        #Exceptions if the file is not able to be created
        except FileNotFoundError:
            self.result_label.config(text='No votes yet.')
        except Exception as e:
            self.result_label.config(text=f'An error occurred: {e}')
    def submit_data(self):
        #Creates variables for the columns in the csv file
        name = self.name_entry.get()
        voter_id = self.voter_id_entry.get()
        selected_candidate = self.candidate_var.get()
        #Addressed Missed inputs
        if not name or not voter_id or selected_candidate == 'None':
            self.error_label.config(text='Please fill all the fields.')
            return
        #Address incorrect name format
        if not isinstance(name, str) or name.count(' ') != 1:
            self.error_label.config(text='Name is not valid.')
            return
        #Address incorrect voter ID format
        if not voter_id.isdigit() or len(voter_id) != 4:
            self.error_label.config(text='Your voter Id is not valid.', foreground='red')
            return
        #Clears error label
        self.error_label.config(text='')

        try:
            with open('votes.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                existing_voter_ids = [row[1] for row in reader]
            
            if voter_id in existing_voter_ids:
                self.error_label.config(text='Voter ID already exists.', foreground='red')
                return

            with open('votes.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, voter_id, selected_candidate])
            self.success_label.config(text='Vote submitted successfully!')

        except FileNotFoundError:
            with open('votes.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, voter_id, selected_candidate])
            self.success_label.config(text='Vote submitted successfully!')

        self.update_vote_counts()

