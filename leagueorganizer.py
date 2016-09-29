#!\usr\bin\env python
''' leagueorganizer.py - Keep records for a league of teams. Emter match results to update
team standings. Data for each league is saved in .json'''

import json

def log_match(team1, team2, records):
    # Enter match results and update team records
    while True:    
        result = raw_input('{0} vs {1}: Which team won?\n'.format(team1, team2))
        if result in [team1, 1]:
            records[team1][0] += 1 # Increase win counter by one for winner
            records[team2][1] -= 1 # Increase lose counter by one for loser
            print 'Match result has been logged.'
            return records
            break
        elif result in [team2, 2]:
            records[team1][1] -= 1
            records[team2][0] += 1
            print 'Match result has been logged.'
            return records
            break
        elif result in ['exit', 'cancel']:
            break
        else:
            print 'Invalid answer. Please answer either {0} or {1}'.format(team1, team2)

def show_standings(records):
    # Show league standings and win/loss record of each team
    standings = sorted(records, key = records.get, reverse = True)
    for i in range(len(standings)):
        win_count = records.get(standings[i])[0]
        loss_count = abs(records.get(standings[i])[1])
        print ('{0}. {1} (W:{2} L:{3})'.format(i+1, standings[i], win_count, loss_count))

def save_league(league_name, records):
    # Save league info to .json
    with open('{}.json'.format(league_name), 'w') as f:
        f.write(json.dumps(records))
    print '{} League data has been saved!'.format(league_name)

def load_league(league_name):
    # Load league data from .json
    with open('{}.json'.format(league_name), 'r') as f:
        content = f.read()
        records = json.loads(content)
        return records

def new_league(league_name):
    # Creates a new league
    print league_name
    records = {}
    i = 1
    while True:
        team_name = raw_input('Enter name for team {}:\n'.format(i))
        if team_name.lower() in ['done', 'stop']:
            break
        records.setdefault(team_name, [0, 0])
        i += 1
    with open('{}.json'.format(league_name), 'w') as f:
              f.write(json.dumps(records))
    return records
    
def main():

    try:
        league_name = raw_input('Enter League Name to Load:\n')
        records = load_league(league_name)
    except IOError:
        answer = raw_input('The league, {}, was not found. Create new league with this name?:\n'.format(league_name))
        if answer.lower() in ['y', 'yes']:
            records = new_league(league_name)

    show_standings(records)

    options = ('1. Enter Match Result', '2. Check Standings', '3. Save League Data')
    while True:
        action = raw_input('\nWhat would you like to do?\n\n{0}\n{1}\n{2}\n\n'.format(*options)).lower()
        
        if action in ['1', 'enter match result']:
            team1 = raw_input('Enter Team 1:\n')
            team2 = raw_input('Enter Team 2:\n')
            log_match(team1, team2, records)

        if action in ['2', 'check standings']:
            show_standings(records)

        if action in ['3', 'save']:
            save_league(league_name, records)

if __name__ == '__main__':
    main()
