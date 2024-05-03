from flask import Flask, render_template, session, url_for, send_from_directory, jsonify, g, redirect, request
import os
import sqlite3
import json, random

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)
@app.route('/')
def home():
    session['current_score'] = 0
    session['highest_score'] = 0

    # This route now just returns the initial HTML page.
    return render_template('options.html')

@app.route('/choose_option/<option>')
def choose_option(option):
    session['option_selected'] = option
    print(option)
    return render_template('index.html')


def get_play_count_db():
    if 'play_count_db' not in g:
        g.play_count_db = sqlite3.connect('play_count.db')
        g.play_count_db.row_factory = sqlite3.Row
    return g.play_count_db

@app.teardown_appcontext
def close_play_count_db(error):
    if 'play_count_db' in g:
        g.play_count_db.close()
def increment_play_count():
    db = get_play_count_db()
    db.execute('UPDATE play_counts SET count = count + 1 WHERE id = 1')  # Assuming only one record
    db.commit()

@app.route('/get-players')
def get_players():
    db = get_db()
    c = db.cursor()
    increment_play_count()
    
    option = session.get('option_selected')

    if option == 'single_season_ppg':
        # Implement logic for single season PPG option
        # Select all players from the database
        c.execute('SELECT * FROM player_data')
        players = c.fetchall()
        random_players = random.sample(players, 2)

        # Calculate highest PPG for each player in a single season
        ppg_dict = {}
        for player in random_players:
            player_name = player['full_name']
            player_image = player['image_link']  # New: Get the player's image URL
            career_stats = json.loads(player['career_stats'])
            for season_stats in career_stats['resultSets'][0]['rowSet']:
                season_id = season_stats[1]
                points = season_stats[26]
                games_played = season_stats[6]
                if games_played > 0:
                    ppg = points / games_played
                    # Round the ppg value to the tenths place
                    ppg = round(ppg, 1)
                    if player_name not in ppg_dict or ppg_dict[player_name]['ppg'] < ppg:
                        ppg_dict[player_name] = {'full_name': player_name, 'season_id': season_id, 'ppg': ppg, 'image': player_image}

        top_players = sorted(ppg_dict.values(), key=lambda x: x['ppg'], reverse=True)[:2]
        session['player_1'] = top_players[0]
        session['player_2'] = top_players[1]

    elif option == 'career_scoring_average':
        c.execute('SELECT * FROM player_data')
        players = c.fetchall()
        random_players = random.sample(players, 2)
                    # Initialize an empty dictionary to hold player information and their highest scoring game
        ppg_dict = {}
        for player in random_players:
            player_name = player['full_name']
            player_image = player['image_link']  # Include the player's image URL
            career_stats = json.loads(player['career_stats'])

            # Find the resultSet for CareerTotalsRegularSeason
            career_totals = next((rs for rs in career_stats['resultSets'] if rs['name'] == 'CareerTotalsRegularSeason'), None)
            
            if career_totals:
                # Extract total points and games played from the career totals
                # This assumes the PTS index is 23 and GP index is 3 based on your initial data description
                total_points = career_totals['rowSet'][0][23]  # PTS index
                total_games = career_totals['rowSet'][0][3]   # GP index

                if total_games > 0:
                    career_ppg = total_points / total_games
                    career_ppg = round(career_ppg, 1)  # Round the PPG value to the tenths place

                    # Save or update the player's career PPG in the dictionary
                    ppg_dict[player_name] = {
                        'full_name': player_name,
                        'ppg': career_ppg,
                        'image': player_image
                    }

        # Sort the players by their career PPG and get the top two
        top_players = sorted(ppg_dict.values(), key=lambda x: x['ppg'], reverse=True)[:2]
        session['player_1'] = top_players[0]
        session['player_2'] = top_players[1]

    elif option == 'career_fg_percent': 
        c.execute('SELECT * FROM player_data')
        players = c.fetchall()
        random_players = random.sample(players, 2)

        # Initialize an empty dictionary to hold player information and their career field goal percentage
        fgp_dict = {}
        for player in random_players:
            player_name = player['full_name']
            player_image = player['image_link']  # Include the player's image URL
            career_stats = json.loads(player['career_stats'])

            # Find the resultSet for CareerTotalsRegularSeason
            career_totals = next((rs for rs in career_stats['resultSets'] if rs['name'] == 'CareerTotalsRegularSeason'), None)
            
            if career_totals:
                # Extract total field goals made and attempted
                total_fgm = career_totals['rowSet'][0][6]  # Index for FGM
                total_fga = career_totals['rowSet'][0][7]  # Index for FGA

                if total_fga > 0:
                    career_fgp = (total_fgm / total_fga) * 100
                    career_fgp = round(career_fgp, 1)  # Round the FG% to two decimal places

                    # Save or update the player's career FG% in the dictionary
                    fgp_dict[player_name] = {
                        'full_name': player_name,
                        'fgp': career_fgp,
                        'image': player_image
                    }

        # Sort the players by their career FG% and get the top two
        top_players = sorted(fgp_dict.values(), key=lambda x: x['fgp'], reverse=True)[:2]
        session['player_1'] = top_players[0]
        session['player_2'] = top_players[1]
    elif option == "career_blocks": 
        c.execute('SELECT * FROM player_data')
        players = c.fetchall()
        random_players = random.sample(players, 2)

        # Initialize an empty dictionary to hold player information and their career blocks per game
        bpg_dict = {}
        for player in random_players:
            player_name = player['full_name']
            player_image = player['image_link']  # Include the player's image URL
            career_stats = json.loads(player['career_stats'])

            # Find the resultSet for CareerTotalsRegularSeason
            career_totals = next((rs for rs in career_stats['resultSets'] if rs['name'] == 'CareerTotalsRegularSeason'), None)
            
            if career_totals:
                total_blocks = career_totals['rowSet'][0][20]  # Index for BLK

                career_bpg = total_blocks

                    # Save or update the player's career blocks per game in the dictionary
                bpg_dict[player_name] = {
                        'full_name': player_name,
                        'bc': career_bpg,
                        'image': player_image
                    }

        # Sort the players by their career blocks per game and get the top two
        top_players = sorted(bpg_dict.values(), key=lambda x: x['bc'], reverse=True)[:2]
        session['player_1'] = top_players[0]
        session['player_2'] = top_players[1]
        print(session['player_1'])
    else: 
        print("HI")

    return jsonify({
        'player1': session['player_1'],
        'player2': session['player_2'],
        'comparisonType': session['option_selected']
    })



def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('nba_players.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/guess/<choice>', methods=['GET'])
def make_guess(choice):
    if choice not in ['lower', 'higher']:
        return jsonify({'error': 'Invalid choice'}), 400
    option = session.get('option_selected')
    if option == 'single_season_ppg':
        player1_ppg = session['player_1']['ppg']
        player2_ppg = session['player_2']['ppg']
    elif option == 'career_scoring_average':
        player1_ppg = session['player_1']['ppg']
        player2_ppg = session['player_2']['ppg'] 
    elif option == 'career_fg_percent':
        player1_ppg = session['player_1']['fgp']
        player2_ppg = session['player_2']['fgp']
    elif option == 'career_blocks':
        player1_ppg = session['player_1']['bc']
        player2_ppg = session['player_2']['bc']
    
    
    correct_guess = False
    if choice == 'higher':
        # Check if player 1 has a higher PPG than player 2
        if player1_ppg < player2_ppg:
            correct_guess = True
        elif player1_ppg== player2_ppg:
            correct_guess = True
        else :
            correct_guess = False
    else:
        # Check if player 1 has a lower PPG than player 2
        if player1_ppg > player2_ppg:
            correct_guess = True
        elif player1_ppg== player2_ppg:
            correct_guess = True
        else :
            correct_guess = False



    if correct_guess:
            # Increment current score if guess is correct
            session['current_score'] += 1
            return jsonify({
            'current_score': session['current_score'],
            'highest_score': session['highest_score'],
            'correct_guess': correct_guess
        })
    else:
        # If guess is incorrect, return an empty response or an error message
        if session['current_score'] > session['highest_score']:
            session['highest_score'] = session['current_score']

        return jsonify({
            'current_score': session['current_score'],
            'highest_score': session['highest_score'],
            'game_over': correct_guess
        })

@app.route('/game_over', methods=['POST'])
def game_over():
  
    data = request.get_json()  # Get JSON data sent from the client
    high_score = data.get('high_score', 0)  # Default to 0 if not provided
    session['high_score'] = high_score
    # Assuming you have a separate endpoint or URL for viewing the game over page
    game_over_url = url_for('view_game_over', _external=True)
    return jsonify({'redirect_url': game_over_url})

@app.route('/view_game_over')
def view_game_over():

    high_score = session.get('high_score', 0)
    player1=session['player_1']
    player2=session['player_2']
 
    option = session.get('option_selected')
    if option == 'career_fg_percent':
        return render_template('game_over_fg.html', player1=player1, player2=player2, current_score=session['current_score'], high_score=high_score)
    elif option == 'single_season_ppg':
        return render_template('game_over_season.html', player1=player1, player2=player2, current_score=session['current_score'], high_score=high_score)
    elif option == 'career_scoring_average':
        return render_template('game_over_career.html', player1=player1, player2=player2, current_score=session['current_score'], high_score=high_score)
    elif option == 'career_blocks':
        return render_template('game_over_blocks.html', player1=player1, player2=player2, current_score=session['current_score'], high_score=high_score)


@app.route('/correct_guess')
def correct_guess():
    app.logger.info('Redirecting to /correct_guess')
    db = get_db()
    c = db.cursor()
    print("initial-1,", session['player_1'])
    print("initial-2,", session['player_2'])
    option = session.get('option_selected')

    if option == 'single_season_ppg':
        c.execute('SELECT * FROM player_data')
        players = c.fetchall()
        player1 = session['player_2']
        if player1 is None:
            return 'Player 1 not found', 404

        player2 = player1
        while player2 == player1:
            player2 = random.choice(players)

            ppg_dict = {}
            player_name = player2['full_name']
            player_image = player2['image_link']  # New: Get the player's image URL
            career_stats = json.loads(player2['career_stats'])
            for season_stats in career_stats['resultSets'][0]['rowSet']:
                season_id = season_stats[1]
                points = season_stats[26]
                games_played = season_stats[6]
                if games_played > 0:
                    ppg = points / games_played
                    # Round the ppg value to the tenths place
                    ppg = round(ppg, 1)
                    if player_name not in ppg_dict or ppg_dict[player_name]['ppg'] < ppg:
                        ppg_dict[player_name] = {'full_name': player_name, 'season_id': season_id, 'ppg': ppg, 'image': player_image}
        
        top_players = sorted(ppg_dict.values(), key=lambda x: x['ppg'], reverse=True)[:1]
        session['player_1'] = player1
        session['player_2'] = top_players[0]


    elif option == 'career_scoring_average':
        c.execute('SELECT * FROM player_data')
        players = c.fetchall()
        player1 = session['player_2']
        if player1 is None:
            return 'Player 1 not found', 404

        player2 = player1
        while player2 == player1:
            player2 = random.choice(players)

            ppg_dict = {}
            player_name = player2['full_name']
            player_image = player2['image_link']
            career_stats = json.loads(player2['career_stats'])

                # Extract data for career scoring averages
            career_totals = next((rs for rs in career_stats['resultSets'] if rs['name'] == 'CareerTotalsRegularSeason'), None)
            if career_totals:
                    total_points = career_totals['rowSet'][0][23]  # Assume PTS index is 23
                    total_games = career_totals['rowSet'][0][3]   # Assume GP index is 3
                    if total_games > 0:
                        career_ppg = total_points / total_games
                        career_ppg = round(career_ppg, 1)  # Round the PPG value to the tenths place
                        ppg_dict[player_name] = {
                            'full_name': player_name,
                            'ppg': career_ppg,
                            'image': player_image
                        }

        # Sort the players by their career PPG and get the top two
        top_players = sorted(ppg_dict.values(), key=lambda x: x['ppg'], reverse=True)[:1]
        session['player_1'] = player1
        session['player_2'] = top_players[0]


    elif option == 'career_fg_percent':
            c.execute('SELECT * FROM player_data')
            players = c.fetchall()
            player1 = session['player_2']
            if player1 is None:
                return 'Player 1 not found', 404

            player2 = player1
            while player2 == player1:
                player2 = random.choice(players)

                ppg_dict = {}
                player_name = player2['full_name']
                player_image = player2['image_link']
                career_stats = json.loads(player2['career_stats'])

                # Extract data for career field goal percentage
                career_totals = next((rs for rs in career_stats['resultSets'] if rs['name'] == 'CareerTotalsRegularSeason'), None)
                if career_totals:
                    total_field_goals_made = career_totals['rowSet'][0][6]  # Assume FGM index is 6
                    total_field_goals_attempted = career_totals['rowSet'][0][7]  # Assume FGA index is 7
                    if total_field_goals_attempted > 0:
                        career_fgp = (total_field_goals_made / total_field_goals_attempted) * 100
                        career_fgp = round(career_fgp, 1)  # Round the FG% to one decimal place
                        ppg_dict[player_name] = {
                            'full_name': player_name,
                            'fgp': career_fgp,  # Store career field goal percentage
                            'image': player_image
                        }


            # Sort the players by their career PPG and get the top two
            top_players = sorted(ppg_dict.values(), key=lambda x: x['fgp'], reverse=True)[:1]
            session['player_1'] = player1
            session['player_2'] = top_players[0]
    elif option == 'career_blocks':
            c.execute('SELECT * FROM player_data')
            players = c.fetchall()
            player1 = session.get('player_2')  # Ensure player1 is taken from the session
            if player1 is None:
                return 'Player 1 not found', 404

            # Select a different player for comparison
            player2 = random.choice(players)
            while player2 == player1:
                player2 = random.choice(players)

            blocks_dict = {}
            player_name = player2['full_name']
            player_image = player2['image_link']
            career_stats = json.loads(player2['career_stats'])

            # Extract data for career blocks
            career_totals = next((rs for rs in career_stats['resultSets'] if rs['name'] == 'CareerTotalsRegularSeason'), None)
            if career_totals:
                total_blocks = career_totals['rowSet'][0][20]  # Assume BLK index is 20

                # Store the player's total career blocks in the dictionary
                blocks_dict[player_name] = {
                    'full_name': player_name,
                    'bc': total_blocks,  # Store career blocks
                    'image': player_image
                }
            top_player = sorted(blocks_dict.values(), key=lambda x: x['bc'], reverse=True)[:1]
            session['player_2'] = top_player[0]
            session['player_1'] = player1


    return jsonify({
        'player1': session['player_1'],
        'player2': session['player_2'],
        'comparisonType': session['option_selected']
    })


if __name__ == '__main__':
    app.run(debug=True)
