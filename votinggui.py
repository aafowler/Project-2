import tkinter as tk
from tkinter import ttk
from typing import Dict
from votinglogic import VotingLogic

class VotingApp:
    """
    Set the class that holds all organizations for the gui

    Args:
        master: The window for the gui
    """
    def __init__(self, master: tk.Tk):
        self.master = master
        self.logic = VotingLogic()

        self.name_label = ttk.Label(master, text='Name:')
        self.name_label.grid(row=0, padx=80, pady=5, sticky='w')
        self.name_entry = ttk.Entry(master)
        self.name_entry.grid(row=0, padx=140, pady=5, sticky='w')

        self.voter_id_label = ttk.Label(master, text='Voter ID:')
        self.voter_id_label.grid(row=1, padx=80, pady=5, sticky='w')
        self.voter_id_entry = ttk.Entry(master)
        self.voter_id_entry.grid(row=1, padx=140, pady=5, sticky='w')

        self.candidate_var = tk.StringVar(value='None')
        self.candidate1_radio = ttk.Radiobutton(master, text='Joe Schmoe', variable=self.candidate_var, value='Joe Schmoe')
        self.candidate1_radio.grid(row=2, padx=135, pady=5, sticky='w')
        self.candidate2_radio = ttk.Radiobutton(master, text='John Smith', variable=self.candidate_var, value='John Smith')
        self.candidate2_radio.grid(row=3, padx=135, pady=5, sticky='w')

        self.submit_button = ttk.Button(master, text='Submit', command=self.submit_vote)
        self.submit_button.grid(row=4, padx=95, pady=5, sticky='w')

        self.new_voter_button = ttk.Button(master, text='New Voter', command=self.reset_gui)
        self.new_voter_button.grid(row=4, padx=175, pady=5, sticky='w')

        self.error_label = ttk.Label(master, text='', foreground='red')
        self.error_label.grid(row=5, padx=120, pady=5, sticky='w')

        self.success_label = ttk.Label(master, text='', foreground='green')
        self.success_label.grid(row=6, padx=100, pady=5, sticky='w')

        self.result_label = ttk.Label(master, text='')
        self.result_label.grid(row=10, padx=140, pady=5, sticky='w')

        self.update_vote_counts()

    def reset_gui(self):
        """Reset all input made in the GUI."""
        self.name_entry.delete(0, tk.END)
        self.voter_id_entry.delete(0, tk.END)
        self.candidate_var.set('None')
        self.error_label.config(text='')
        self.success_label.config(text='')

    def update_vote_counts(self):
        """
        Updates the vote count at the bottom of the gui

        Reads vote counts from csv file and updates the totals

        Handles a possible error where the file is no longer working.
        """
        try:
            counts: Dict[str, int] = self.logic.count_votes()
            result_text = "\n".join(f"{candidate}: {count}" for candidate, count in counts.items())
            self.result_label.config(text=result_text or "No votes yet.")
        except IOError as e:
            self.result_label.config(text=f"Error: {e}")

    def submit_vote(self):
        """
        Retrieves user input, checks it, and adds it to csv with the voting logic.

        Updates the GUI with success or error messages and adds to the count if all is correct.
        """
        name: str = self.name_entry.get()
        voter_id: str = self.voter_id_entry.get()
        candidate: str = self.candidate_var.get()

        if not name or not voter_id or candidate == 'None':
            self.error_label.config(text="Please fill all fields.")
            return

        if not self.logic.validate_name(name):
            self.error_label.config(text="Invalid name format.")
            return

        if not self.logic.validate_voter_id(voter_id):
            self.error_label.config(text="Invalid voter ID format.")
            return

        if self.logic.duplicate_voter_id(voter_id):
            self.error_label.config(text="Voter ID already exists.")
            return

        try:
            self.logic.record_vote(name, voter_id, candidate)
            self.success_label.config(text="Vote submitted successfully!")
            self.update_vote_counts()
        except IOError as e:
            self.error_label.config(text=f"Error: {e}")