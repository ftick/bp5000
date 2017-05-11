### File Format of Bracket files (*.bp5)

(1-4) version code (current = 1) ex. 00000001 (1)

(5-8) number of players/entrants ex. 00000080 (128)

each participant (9-?)

Participants format is
- (1-4) number of bytes in the participants name
- (5-n) participants name
- (n-n+3) participants seed
- (n+4-n+7) participants ID

then 4 bytes representing the # of eliminations.

then for each elimination, another 4 bytes representing the number of matches in that bracket, each followed by their matches
(so # elim, # matches, matches, # LB matches, matches, etc.)

each match has format
 - (1) whether it is a first round match
 - (2-5) match id
 - (6) has a winner match
 - (7-10) winner match code
 - (11) has a loser match
 - (12-15) loser match code
 - (16) has participant 1
 - (17-20) participant 1 code
 - (21) has participant 2
 - (22-25) participant 2 code
 - (26-29) 1 if participant 1 won, 2 if participant 2 won, 0 if no result
 - (30) if the match is a special match
 - (31-34) the lower # of sets left
 - (35-38) the upper # of sets left
