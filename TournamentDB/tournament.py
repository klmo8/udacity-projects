#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
# Author: Kyle Moss
# Last Modified: June 2017

import psycopg2, bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("SELECT count(id) FROM players;")
    count = c.fetchone()
    conn.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s);", (bleach.clean(name),))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins."""
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("SELECT * FROM PlayerStandings;")
    standings = c.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);", (bleach.clean(winner), bleach.clean(loser),))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record.
    """

    conn = psycopg2.connect("dbname=tournament")
    c = conn.cursor()
    c.execute("SELECT * FROM PlayerStandings;")
    standings = playerStandings()
    pairings = []
    enteredPlayers = []

    for row1 in standings:
        for row2 in standings:
            if (row1[0] != row2[0] and row1[0] not in enteredPlayers and row2[0] not in enteredPlayers and row1[2] == row2[2]):
                pairings.append((row1[0], row1[1], row2[0], row2[1]))
                enteredPlayers.append(row1[0])
                enteredPlayers.append(row2[0])

    return pairings
    conn.close()
