from nba_api.stats.static import players
def get_player_id(name):
    # Assuming you have a method to retrieve player information based on their name
    player_info =  players.find_players_by_full_name(name)
    
    if player_info:
        return player_info[0]['id']  # Access the first item in the list and then access the 'id' key
    else:
        return None


# List of player names
player_names = [
'Trae Young', 'Ja Morant', 'Cole Anthony', 'Tyrese Haliburton', 'Jayson Tatum', 'Jaylen Brown', 'De\'Aaron Fox', 'Shai Gilgeous-Alexander', 'Bam Adebayo', 'Deandre Ayton', 'Michael Porter Jr.', 'Jaren Jackson Jr.', 'Brandon Ingram', 'John Collins', 'Malcolm Brogdon', 'Pascal Siakam', 'Julius Randle', 'Christian Wood', 'Fred VanVleet', 'Jamal Murray', 'CJ McCollum', 'Khris Middleton', 'Ben Simmons', 'Nikola Vucevic', 'Rudy Gobert', 'Nikola Jokic', 'Derrick Rose', 'Hakeem Olajuwon', 'Giannis Antetokounmpo', 'Klay Thompson', 'Draymond Green', 'LaMarcus Aldridge', 'DeMar DeRozan', 'Tim Duncan', 'Yao Ming', 'Paul Pierce', 'Vince Carter', 'Tracy McGrady', 'Allen Iverson', 'Kevin Garnett', 'Shaquille O\'Neal', 'LeBron James', 'Russell Westbrook', 'Stephen Curry', 'James Harden', 'Anthony Davis', 'Kyrie Irving', 'Damian Lillard', 'Kawhi Leonard', 'Chris Paul', 'Paul George', 'Jimmy Butler', 'Joel Embiid', 'Karl-Anthony Towns', 'Devin Booker', 'Bradley Beal', 'Donovan Mitchell', 'Zach LaVine', 'Derrick Rose', 'Rajon Rondo', 'Dwight Howard', 'Carmelo Anthony', 'Amar\'e Stoudemire', 'Dwyane Wade', 'Steve Nash', 'Ray Allen', 'Chris Bosh', 'Tony Parker', 'Manu Ginobili', 'Andre Iguodala', 'Mike Conley', 'Goran Dragic', 'Luis Scola', 'Joe Johnson', 'Al Horford', 'Gordon Hayward', 'Lou Williams', 'Isaiah Thomas', 'Kyle Lowry', 'Kemba Walker', 'Jrue Holiday', 'Baron Davis', 'Gilbert Arenas', 'Shawn Marion', 'Monta Ellis', 'Al Jefferson', 'David Lee', 'Serge Ibaka', 'Marc Gasol', 'Zach Randolph', 'Andrei Kirilenko', 'Dirk Nowitzki', 'Pau Gasol', 'Paolo Banchero', 'Kristaps Porzingis', 'Kendrick Perkins', 'Michael Jordan', 'Kevin Durant', 'Seth Curry', 'DeAndre Jordan', 'Greg Oden', 'Malik Beasley', 'Brook Lopez', 'Steven Adams', 'Grant Hill', 'Mike Bibby', 'Hedo Turkoglu', 'Blake Griffin', 'Tyson Chandler', 'Ben Wallace', 'Victor Oladipo', 'Daniel Gafford', 'Mikal Bridges', 'Collin Sexton', 'John Wall', 'LaMelo Ball', 'Andre Drummond', 'Jeff Teague', 'Austin Rivers', 'Clint Capela', 'Dario Saric', 'Bobby Portis', 'Theo Ratliff', 'Jamaal Magloire', 'Tyrone Hill', 'Jayson Williams', 'Dana Barros', 'Mo Williams', 'Nick Van Exel', 'Sam Cassell', 'Kevin Love', 'Chris Gatling', 'Cedric Ceballos', 'Mehmet Okur', 'Eddy Curry', 'Josh Howard', 'Kenyon Martin', 'Chris Kaman', 'Roy Hibbert', 'Josh Smith', 'Andrea Bargnani', 'Danny Granger', 'Clyde Drexler', 'Chauncey Billups', 'Kevin McHale', 'Dikembe Mutombo', 'Artis Gilmore', 'George Gervin', 'John Havlicek', 'Larry Bird', 'Oscar Robertson', 'Moses Malone', 'Dolph Schayes', 'Elvin Hayes', 'Hal Greer', 'Bob McAdoo', 'Wilt Chamberlain', 'Bob Pettit', 'Adrian Dantley', 'Jerry West', 'Dennis Rodman', 'Scottie Pippen', 'Dominique Wilkins'
]

# Dictionary to store player names and their NBA IDs
player_ids = {name: get_player_id(name) for name in player_names}

# Write HTML content to a file
with open('players.html', 'w') as file:
    file.write("{% extends 'base.html' %}\n")
    file.write("{% block content %}\n")
    for name, player_id in player_ids.items():
        file.write(f"<li>")
        file.write(f"<h2>{name}</h2>")
        if player_id:
            file.write(f"<p>Player ID: {player_id}</p>")
            file.write(f"<img src='https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png' alt='{name} Image'>")
        else:
            file.write(f"<p>No ID found for {name}</p>")
        file.write(f"</li>")
    file.write("{% endblock %}\n")
