from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Initialize game state
game_state = {
    'player_1_position': 1,  # Player 1 starts at tile 1
    'player_2_position': 1,  # Player 2 starts at tile 1
    'current_player': 1,     # Player 1 starts first
    'game_over': False       # Game is ongoing
}

# Helper function to check if a player has won
def check_winner():
    if game_state['player_1_position'] == 9:
        return 1  # Player 1 wins
    if game_state['player_2_position'] == 9:
        return 2  # Player 2 wins
    return None

# Helper function to update player position after roll
def update_position(player, roll):
    # Update the player's position based on the roll
    if player == 1:
        new_position = (game_state['player_1_position'] + roll - 1) % 12 + 1
        game_state['player_1_position'] = new_position
    elif player == 2:
        new_position = (game_state['player_2_position'] + roll - 1) % 12 + 1
        game_state['player_2_position'] = new_position

# Home route to render the game board and allow actions
@app.route('/')
def index():
    winner = check_winner()
    return render_template('index.html', 
                           player_1_position=game_state['player_1_position'], 
                           player_2_position=game_state['player_2_position'], 
                           current_player=game_state['current_player'],
                           game_over=game_state['game_over'],
                           winner=winner)

# Roll the die and move the current player
@app.route('/roll', methods=['POST'])
def roll():
    if game_state['game_over']:
        return redirect(url_for('index'))

    roll = random.randint(1, 6)  # Simulate a die roll between 1 and 6

    # Update the current player's position
    if game_state['current_player'] == 1:
        update_position(1, roll)
        game_state['current_player'] = 2
    else:
        update_position(2, roll)
        game_state['current_player'] = 1

    # Check if any player has won
    winner = check_winner()
    if winner:
        game_state['game_over'] = True

    return redirect(url_for('index'))

# Restart the game
@app.route('/restart')
def restart():
    # Reset the game state
    game_state['player_1_position'] = 1
    game_state['player_2_position'] = 1
    game_state['current_player'] = 1
    game_state['game_over'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
