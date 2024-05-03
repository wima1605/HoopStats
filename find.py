from nba_api.stats.static import players

# List of player names
player_names = [
'Hasheem Thabeet',
'Eddy Curry',
'Josh Howard',
'Kenyon Martin',
'Chris Kaman',
'Roy Hibbert',
'Michael Redd',
'OJ Mayo',
'Josh Smith',
'Andrea Bargnani',
'Danny Granger',
'Antawn Jamison',
'Clyde Drexler',
'Lou Hudson',
'Marques Johnson',
'Chauncey Billups',
'Kevin McHale',
'Shane Battier',
'Michael Cooper',
'Dikembe Mutombo',
'Gerald Wallace',
'Artis Gilmore',
'George Gervin',
'John Havlicek',
'Larry Bird',
'Oscar Robertson',
'Moses Malone',
'Dolph Schayes',
'Mark Aguirre',
'Elvin Hayes',
'Jack Sikma',
'Hal Greer',
'Bob McAdoo',
'Wilt Chamberlain',
'Sidney Moncrief',
'Bob Pettit',
'Adrian Dantley',
'Jerry West',
'Dennis Rodman',
'Alex English',
'Fat Lever',
'Scottie Pippen',
'Dominique Wilkins'
]

# Function to fetch NBA player ID
def get_player_id(name):
    player_info = players.find_players_by_full_name(name)
    
    if player_info:
        return player_info[0]['id']
    else:
        return None

# Dictionary to store player names and their NBA IDs
player_ids = {name: get_player_id(name) for name in player_names}
print(player_ids)
