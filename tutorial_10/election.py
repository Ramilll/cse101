from collections import defaultdict


class Vote:
    """A single vote object.

    Data attributes:
    - preference_list: a list of the preferred parties for this voter,
      in descending order of preference.
    """

    def __init__(self, preference_list):
        """Initialize the preference_list attribute of the object."""
        self.preference_list = preference_list

    def __str__(self):
        """Produce a printable string."""
        if self.preference_list:
            return " > ".join(self.preference_list)
        else:
            return "Blank"

    def __repr__(self):
        """Produce a string which, if typed into Python, would produce a Vote object with the same preference_list attribute."""
        return f"Vote({self.preference_list!r})"

    def preference(self, names):
        """Return the item in names that occurs first in the preference list,
        or None if no item in names appears.
        """
        for name in self.preference_list:
            if name in names:
                return name
        return None

    def first_preference(self):
        """Return the first party in the preference_list, or None if the list is empty."""
        if self.preference_list:
            return self.preference_list[0]
        else:
            return None


class Election:
    """A basic election class.

    Data attributes:
    - parties: a list of party names
    - blank: a list of blank votes
    - piles: a dictionary with party names for keys
      and lists of votes (allocated to the parties) for values
    """

    def __init__(self, parties):
        self.parties = parties
        self.blank = []
        self.piles = {name: [] for name in self.parties}

    def add_vote(self, vote):
        """Add a Vote object to the appropriate pile in the Election."""
        if vote.preference_list:
            first_preference = vote.first_preference()
            self.piles[first_preference].append(vote)
        else:
            self.blank.append(vote)

    def add_votes_from_file(self, filename):
        """Read the contents of a file and add each of the votes in it to the correct pile of the election."""
        with open(filename) as f:
            for line in f:
                # Split the line into a list of words
                preference_list = line.strip().split()
                # Create a Vote object with the preference_list
                vote = Vote(preference_list)
                # Add the Vote object to the election
                self.add_vote(vote)

    def status(self):
        """Return a dictionary of the number of votes for each party."""
        return {name: len(votes) for name, votes in self.piles.items()}


class FirstPastThePostElection(Election):
    """
    First-past-the-post elections: whoever gets the most first-preference votes wins.
    """

    def winner(self):
        """Return the party that won the election by getting the most first-preference votes."""
        # Get the number of votes for each party
        votes_by_party = self.status()
        # Sort the parties by the number of votes they received
        sorted_votes = sorted(votes_by_party.items(), key=lambda x: x[1], reverse=True)
        # Check if there are multiple parties with the same number of votes
        if len(sorted_votes) > 1 and sorted_votes[0][1] == sorted_votes[1][1]:
            return None
        # Return the party with the most votes
        return sorted_votes[0][0]


class WeightedElection(Election):
    """
    Weighted elections: each vote contributes to a party's total
    according to that party's position among the vote's preferences.
    """

    def status(self):
        """Returns a dictionary with keys being the parties
        and values being the number of points (counted using
        the weighted scheme) that the party got.
        """
        weighted_votes_by_party = {party: 0 for party in self.parties}
        for party, votes in self.piles.items():
            for vote in votes:
                for i, preference in enumerate(vote.preference_list):
                    weighted_votes_by_party[preference] += 5 - i

        return weighted_votes_by_party

    def winner(self):
        """Return the party that won the election by getting the most points"""
        weighted_votes_by_party = self.status()
        win_party = min(weighted_votes_by_party.items(), key=lambda x: (-x[1], x[0]))[0]
        return win_party


class PreferentialElection(Election):
    """
    Simple preferential/instant-runoff elections.
    """

    def __init__(self, parties):
        super().__init__(parties)  # Initialize as for Elections
        self.dead = []

    def eliminate(self, party):
        """Remove the given party from piles, and redistribute its
        votes among the parties not yet eliminated, according to
        their preferences.  If all preferences have been eliminated,
        then add the vote to the dead list.
        """
        # Get the list of parties that have not been eliminated
        remaining_parties = [p for p in self.parties if p != party]

        # Move the votes for the eliminated party to the dead pile
        # if all preferences have been eliminated, otherwise redistribute
        # the votes according to the preferences of the voters
        for vote in self.piles[party]:
            next_preference = vote.preference(remaining_parties)
            if next_preference:
                self.piles[next_preference].append(vote)
            else:
                self.dead.append(vote)

        # Remove the eliminated party from the piles
        self.parties.remove(party)
        self.piles.pop(party)

    def round_loser(self):
        """Return the name of the party to be eliminated from the next round."""
        # Get the party with the smallest number of votes
        return min(self.piles, key=lambda p: len(self.piles[p]))

    def winner(self):
        """Run a preferential election based on the current piles of votes,
        and return the winning party.
        """
        # Keep eliminating parties until there is only one left
        while len(self.parties) > 1:
            loser = self.round_loser()
            self.eliminate(loser)

        # Return the remaining party
        return self.parties[0]
