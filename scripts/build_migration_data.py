"""Build compact per-player state data (birth / high school / college / team) for active NFL players.

Usage: python3 -I scripts/build_migration_data.py data/nfl_players_2026.csv out.json
College states are a hand-built lookup on the first-listed school (assumed primary); see COLLEGE_STATE.
"""
import csv, json, re, sys

TEAM_STATE = {
 'ARI':'AZ','ATL':'GA','BAL':'MD','BUF':'NY','CAR':'NC','CHI':'IL','CIN':'OH','CLE':'OH','DAL':'TX','DEN':'CO',
 'DET':'MI','GB':'WI','HOU':'TX','IND':'IN','JAX':'FL','KC':'MO','LA':'CA','LAC':'CA','LV':'NV','MIA':'FL',
 'MIN':'MN','NE':'MA','NO':'LA','NYG':'NJ','NYJ':'NJ','PHI':'PA','PIT':'PA','SEA':'WA','SF':'CA','TB':'FL',
 'TEN':'TN','WAS':'MD'}

_c = {}
def add(st, names):
    for n in names.split('|'): _c[n.strip()] = st
add('AL','Alabama|Alabama A&M|Alabama State|Auburn|South Alabama|UAB|Jacksonville State|Troy')
add('AZ','Arizona|Arizona State|Northern Arizona')
add('AR','Arkansas|Arkansas State|Central Arkansas|Southern Arkansas')
add('CA','California|UCLA|USC|Stanford|San Diego State|San Jose State|Fresno State|UC Davis|Cal Poly (San Luis Obispo)|Azusa Pacific')
add('CO','Colorado|Colorado State|Air Force|Western State')
add('CT','Connecticut|Yale|Sacred Heart University')
add('DE','Delaware')
add('DC','Howard')
add('FL','Florida|Florida State|Miami|UCF|University of South Florida|Florida A&M|Florida Atlantic|Florida International')
add('GA','Georgia|Georgia Tech|Georgia Southern|Georgia State|Albany State (GA)|Fort Valley State College|Valdosta State')
add('HI','Hawaii')
add('ID','Boise State|Idaho')
add('IL','Illinois|Northwestern|Illinois State|Southern Illinois|Western Illinois')
add('IN','Indiana|Purdue|Notre Dame|Ball State|Indiana State|Valparaiso')
add('IA','Iowa|Iowa State|Northern Iowa|Drake')
add('KS','Kansas|Kansas State|Fort Hays|Washburn')
add('KY','Kentucky|Louisville|Western Kentucky|Murray State')
add('LA','LSU|Louisiana|Louisiana-Lafayette|Louisiana Tech|Tulane|Southeastern Louisiana')
add('ME','Maine')
add('MD','Maryland|Navy|Morgan State')
add('MA','Boston College|UMass Amherst|Holy Cross|Harvard')
add('MI','Michigan|Michigan State|Central Michigan|Eastern Michigan|Western Michigan|Ferris State|Saginaw Valley State')
add('MN','Minnesota|Minnesota State')
add('MS','Mississippi|Mississippi State|Southern Mississippi|Alcorn State|Jackson State University|Delta State University')
add('MO','Missouri|Missouri Western|Southeast Missouri State')
add('MT','Montana|Montana State')
add('NE','Nebraska')
add('NV','Nevada|UNLV')
add('NH','New Hampshire')
add('NM','New Mexico')
add('NY','Syracuse|Buffalo|Army|Marist|Canisius College')
add('NC','North Carolina|N.C. State|Duke|Wake Forest|East Carolina|Appalachian State|Charlotte|Lenoir Rhyne|Wingate|Barton College')
add('ND','North Dakota State')
add('OH','Ohio State|Cincinnati|Miami (Ohio)|Toledo|Akron|Bowling Green|Dayton|Malone|Findlay|Youngstown State')
add('OK','Oklahoma|Oklahoma State|Tulsa|East Central')
add('OR','Oregon|Oregon State')
add('PA','Penn State|Pittsburgh|Temple|Villanova|Indiana PA,  University of|Duquesne')
add('RI','Brown|Bryant')
add('SC','South Carolina|Clemson|Coastal Carolina|South Carolina State|Furman|Wofford')
add('SD','South Dakota|South Dakota State|Sioux Falls')
add('TN','Tennessee|Vanderbilt|Memphis|Middle Tennessee State|East Tennessee State|Tennessee-Chattanooga|Tusculum College')
add('TX','Texas|Texas A&M|Texas Tech|Baylor|TCU|SMU|Houston|Rice|Houston Christian University|Sam Houston State|Stephen F. Austin State|Tarleton State|Texas State-San Marcos|Texas-El Paso|Texas-San Antonio|East Texas A&M')
add('UT','Utah|Utah State|BYU|Weber State|Southern Utah State')
add('VA','Virginia|Virginia Tech|Liberty|James Madison|Virginia Commonwealth Univ.|William & Mary')
add('WA','Washington|Washington State|Eastern Washington')
add('WV','West Virginia|Marshall|Shepherd')
add('WI','Wisconsin|Wisconsin-Whitewater')
add('WY','Wyoming')
add('CAN','University of British Columbia')
add('NJ','Rutgers')
COLLEGE_STATE = _c
US = set('AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split())

def main(src, out):
    rows = [r for r in csv.DictReader(open(src)) if r['status'] == 'ACT']
    players, unmapped = [], set()
    for r in rows:
        bs, bc = r['birth_state'], r['birth_country']
        if not bs and bc in US: bs, bc = bc, 'USA'          # ESPN "City, ST" rows landed in the country column
        birth = bs if bc == 'USA' and bs in US else (bc or '?') if r['birth_city'] or bc else '?'
        m = re.search(r'\(([^)]*)\)\s*$', r['high_school'])
        hs = m.group(1) if m else '?'
        first = r['college'].split(';')[0].strip()
        col = COLLEGE_STATE.get(first, '?') if first else '?'
        if first and col == '?': unmapped.add(first)
        players.append([r['full_name'], r['team'], r['position'], birth, hs, col])
    json.dump({'teamState': TEAM_STATE, 'players': players}, open(out, 'w'), separators=(',', ':'))
    print(len(players), 'players; unmapped colleges:', sorted(unmapped))

if __name__ == '__main__': main(*sys.argv[1:3])
