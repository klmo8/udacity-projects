-- Table definitions for the tournament project.
-- Author: Kyle Moss
-- Last Modified: June 2017

CREATE DATABASE tournament;
\c tournament

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;


CREATE TABLE players (
  id serial,
  name text,
  Primary Key(id)
);

CREATE TABLE matches (
  matchid serial,
  loser int references players(id),
  winner int references players(id),
  Primary Key(matchid)
);

CREATE VIEW PlayerStandings as
  SELECT * FROM
    (SELECT players.id, players.name, count(mwon.winner) AS won, count(mwon.matchid) + count(mlost.matchid) AS totalMatches
    FROM players
    LEFT JOIN
    (SELECT winner, matchid FROM matches) AS mwon
    ON (players.id = mwon.winner)
    LEFT JOIN
    (SELECT loser, matchid
    FROM matches) AS mlost
    ON (players.id = mlost.loser)
    GROUP BY players.id, players.name) AS results
    ORDER BY results.won;

CREATE VIEW EqualWins as
  SELECT a.id as id1, b.id as id2
  FROM playerstandings AS a, playerstandings AS b
  WHERE a.won=b.won AND a.id>b.id;

CREATE VIEW Player1Matchup as
  SELECT row_number() over() as id, players.id as player1_id, players.name as player1_name FROM players JOIN equalwins on players.id=equalwins.id1;

CREATE VIEW Player2Matchup as
  SELECT row_number() over() as id, players.id as player2_id, players.name as player2_name FROM players JOIN equalwins on players.id=equalwins.id2;
