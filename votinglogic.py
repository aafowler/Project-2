import csv

class VotingLogic:
    """
    A class to process votes in a CSV file.

    """
    def __init__(self, file_name='votes.csv'):
        """
        Sets the VotingLogic object with the specific chosen name.

        Args:
            file_name (str): The name of the CSV file..
        """
        self.file_name = file_name

    def validate_name(self, name):
        """
        Check voters name.

        Args:
            name (str): voter name.

        Returns:
            True if name is valid aka has 1 space and only a string, otherwise returns False.
        """
        return isinstance(name, str) and name.count(' ') == 1

    def validate_voter_id(self, voter_id):

        return voter_id.isdigit() and len(voter_id) == 4

    def duplicate_voter_id(self, voter_id):
        """
        Check Voter ID

        Args:
            voter_id (str): Voter ID variable.

        Returns:
            True if voter ID is valid aka 4-digit int, otherwise returns False.
        """
        try:
            with open(self.file_name, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                existing_ids = [row[1] for row in reader if len(row) > 1]
                return voter_id in existing_ids
        except FileNotFoundError:
            return False

    def record_vote(self, name, voter_id, candidate):
        """
        Adds vote to file

        Args:
            name (str): voter name.
            voter_id (str): voter ID.
            candidate (str): Election Pick

        Raises:
            IOError: Makes it so we know if there is a writing issue
        """
        try:
            with open(self.file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, voter_id, candidate])
        except Exception as e:
            raise IOError(f"Error writing to file: {e}")

    def count_votes(self):
        """
        Tally votes per candidate

        Returns:
            counts: Dictionary where keys are candidate and values are the product of the votes.
        
        Raises:
            IOError: Makes it so we know if there is a reading issue
        """
        try:
            with open(self.file_name, 'r') as csvfile:
                reader = csv.reader(csvfile)
                votes = [row[2] for row in reader if len(row) > 2]
            counts = {}
            for vote in votes:
                counts[vote] = counts.get(vote, 0) + 1
            return counts
        except FileNotFoundError:
            return {}
        except Exception as e:
            raise IOError(f"Error reading file: {e}")
