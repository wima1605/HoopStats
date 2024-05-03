import sqlite3
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
import json
# Connect to the SQLite database
conn = sqlite3.connect('nba_players.db')
c = conn.cursor()

# Create a table to store player information, career stats, season stats, and image link
c.execute('''CREATE TABLE IF NOT EXISTS player_data
             (id INTEGER PRIMARY KEY, player_id INTEGER, full_name TEXT, first_name TEXT, last_name TEXT, is_active BOOLEAN, career_stats TEXT, image_link TEXT)''')

player_ids = [
2201, 2572, 2030, 2549, 201579, 2746, 200745, 101122, 17, 1497, 1450, 87, 600014, 76804, 76970, 1449, 600015, 77449, 78076, 76979, 76882, 77498, 76375, 77847, 76504, 78497, 23, 937, 1122
]










   #ADDED TO DB- 203507, 1629027, 1629630, 1630163, 1630175,1630169, 1628369, 1626164, 1628378, 1627759
   #  1628368, 1628983, 1628389, 1629028, 1629008, 1628991, 1627742, 1628381, 1627763, 1627783
   #203944, 1626174, 1627832, 1627750, 203468, 203114, 1627732, 1626157, 203078, 202696
     #  202710, 203497, 202331, 202681, 203081, 203954, 203999, 203507, 203076, 201566,
# 201933, 201565, 202695, 201142, 201939, 201935, 101108, 1717, 959, 2548
#2544, 201142, 201939, 202695, 201935, 203076, 203507, 201566, 203081, 202681, 101108, 202331,
#1717, 1495, 2547, 2397, 1718, 1713, 1503, 947, 959, 708, 406, 977, 951, 460, 223, 165
#203076, 201935, 203507, 203081, 202681, 101108, 202331, 202710, 203954, 1626157, 1626164, 203078

for player_id in player_ids:
    # Retrieve player information
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_data = player_info.get_data_frames()[0]
    full_name = player_info_data['DISPLAY_FIRST_LAST'].iloc[0]
    first_name = player_info_data['FIRST_NAME'].iloc[0]
    last_name = player_info_data['LAST_NAME'].iloc[0]
    
    # Retrieve player career statistics
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)

    # Construct the image link
    image_link = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"

    # Store the player information, career stats, season stats, and image link in the database
    c.execute('INSERT INTO player_data (player_id, full_name, first_name, last_name, is_active, career_stats, image_link) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (player_id, full_name, first_name, last_name, None,  json.dumps(career_stats.get_dict()), image_link))

# Commit changes to the database
conn.commit()

# Close the database connection
conn.close()
