# Web Scraping Rough
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd

# First NBA Season we will analyze
year = 1983

# URL page we will scraping + the year
url_players = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
url_teams = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html".format(year)

# HTML from the url and Beautiful soup formatting
html = uReq(url_players)
html_teams = uReq(url_teams)

page_soup = soup(html)
page_soup_teams = soup(html_teams)


# Team Data per Conference
table_east = page_soup_teams.find('table', id="divs_standings_E")
table_west = page_soup_teams.find('table', id="divs_standings_W")

# Extracting headers we needed and put them into list
headers = [th.getText() for th in page_soup.findAll('tr', limit=2)[0].findAll('th')]
headers_teams_east = [th.getText() for th in table_east.findAll('tr', limit=2)[0].findAll('th')]
headers_teams_west = [th.getText() for th in table_west.findAll('tr', limit=2)[0].findAll('th')]

# Exclude rankings column
headers = headers[1:]
headers_teams_east = headers_teams_east[1:]
headers_teams_west = headers_teams_west[1:]


# Getting each row data (avoids headers)
rows = page_soup.findAll('tr')[1:]
rows_teams_east = table_east.findAll('tr')[1:]
rows_teams_west = table_west.findAll('tr')[1:]

# Teams names table
team_names_east = [[th.getText() for th in rows_teams_east[i].findAll('th')]
            for i in range(len(rows_teams_east))]
team_names_west = [[th.getText() for th in rows_teams_west[j].findAll('th')]
            for j in range(len(rows_teams_west))]

# Formatting team_names 
for i in team_names_east:
    if "Division" in i[0]: # Removing Divisions caught up in the list
        team_names_east.remove(i)
        
for j in team_names_west:
    if "Division" in j[0]:
        team_names_west.remove(j)
        
new_team_names_east = []
new_team_names_west = []

# Moving into List of strings
for i in team_names_east:
    if "*" in i[0]: # Removing Asterisks from team names
        i[0] = i[0].replace("*", "")
    new_team_names_east.append(i[0])

for j in team_names_west:
    # Removing Asterisks from team names
    if "*" in j[0]:
        j[0] = j[0].replace("*", "")
    new_team_names_west.append(j[0])

# Get player data
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
# Get Team Data
f_team_stats_east = [[td.getText() for td in rows_teams_east[i].findAll('td')]
            for i in range(len(rows_teams_east))]
f_team_stats_west = [[td.getText() for td in rows_teams_west[i].findAll('td')]
            for i in range(len(rows_teams_west))]

# Moving into List of strings
s_team_stats_east = [x for x in f_team_stats_east if x != []]
s_team_stats_west = [x for x in f_team_stats_west if x != []]


# Format data onto DataFrame
stats = pd.DataFrame(player_stats, columns = headers)
team_stats = pd.DataFrame(s_team_stats_east, columns = headers_teams_east)
team_stats_west = pd.DataFrame(s_team_stats_west, columns = headers_teams_west)

# Add 'Season' & 'Team'
stats['Season'] = year
team_stats['Season'] = year
team_stats['Team'] = new_team_names_east
team_stats_west['Season'] = year
team_stats_west['Team'] = new_team_names_west

team_stats = team_stats.append(team_stats_west)

year+=1
while year < 2020:
    # Repeating process for year + 1
    url_players = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
    url_teams = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html".format(year)
    html = uReq(url_players)
    html_teams = uReq(url_teams)
    page_soup = soup(html)
    page_soup_teams = soup(html_teams)
    table_east = page_soup_teams.find('table', id="divs_standings_E")
    table_west = page_soup_teams.find('table', id="divs_standings_W")
    headers = [th.getText() for th in page_soup.findAll('tr', limit=2)[0].findAll('th')]
    headers_teams_east = [th.getText() for th in table_east.findAll('tr', limit=2)[0].findAll('th')]
    headers_teams_west = [th.getText() for th in table_west.findAll('tr', limit=2)[0].findAll('th')]
    headers = headers[1:]
    headers_teams_east = headers_teams_east[1:]
    headers_teams_west = headers_teams_west[1:]
    rows = page_soup.findAll('tr')[1:]
    rows_teams_east = table_east.findAll('tr')[1:]
    rows_teams_west = table_west.findAll('tr')[1:]
    team_names_east = [[th.getText() for th in rows_teams_east[i].findAll('th')]
            for i in range(len(rows_teams_east))]
    team_names_west = [[th.getText() for th in rows_teams_west[j].findAll('th')]
            for j in range(len(rows_teams_west))]    
    for i in team_names_east:
        if "Division" in i[0]:
            team_names_east.remove(i)
    for j in team_names_west:
        if "Division" in j[0]:
            team_names_west.remove(j)
    new_team_names_east = []
    new_team_names_west = []
    for i in team_names_east:
        if "*" in i[0]:
            i[0] = i[0].replace("*", "")
        new_team_names_east.append(i[0])
    for j in team_names_west:
        if "*" in j[0]:
            j[0] = j[0].replace("*", "")
        new_team_names_west.append(j[0])
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
    f_team_stats_east = [[td.getText() for td in rows_teams_east[i].findAll('td')]
            for i in range(len(rows_teams_east))]
    f_team_stats_west = [[td.getText() for td in rows_teams_west[i].findAll('td')]
            for i in range(len(rows_teams_west))]
    s_team_stats_east = [x for x in f_team_stats_east if x != []]
    s_team_stats_west = [x for x in f_team_stats_west if x != []]
    stats_temp = pd.DataFrame(player_stats, columns = headers)
    team_stats_east = pd.DataFrame(s_team_stats_east, columns = headers_teams_east)
    team_stats_west = pd.DataFrame(s_team_stats_west, columns = headers_teams_west)
    stats_temp['Season'] = year
    team_stats_east['Season'] = year
    team_stats_east['Team'] = new_team_names_east
    team_stats_west['Season'] = year
    team_stats_west['Team'] = new_team_names_west

    # Appending the extracted data onto existing DataFrame.
    stats = stats.append(stats_temp)
    team_stats_east = team_stats_east.append(team_stats_west)
    team_stats = team_stats.append(team_stats_east)
    year+=1

# Dropping NaN Columns
nan_val = float("NaN")
stats.replace("", nan_val, inplace=True)
stats.dropna(subset = ["Player"], inplace=True)

# Taking out '*' from Player's names in df
for i, row in stats.iterrows():
    if "*" in row['Player']:
        stats['Player'].loc[(stats['Player'] == row['Player'])] = row['Player'].replace("*", "")

# Only keep total averages for players that played for more than one team in a season
stats = stats.drop_duplicates(subset=['Player', 'Season'], keep='first')

# Adding MVP, DPOY, and Sixth Man of the Year Awards
MVP_Awards = pd.DataFrame(['Moses Malone','Larry Bird','Larry Bird','Larry Bird','Magic Johnson','Michael Jordan','Magic Johnson','Magic Johnson','Michael Jordan','Michael Jordan','Charles Barkley','Hakeem Olajuwon','David Robinson','Michael Jordan','Karl Malone','Michael Jordan','Karl Malone','Shaquille O\'Neal','Allen Iverson','Tim Duncan','Tim Duncan','Kevin Garnett','Steve Nash','Steve Nash','Dirk Nowitzki','Kobe Bryant','LeBron James','LeBron James','Derrick Rose','LeBron James','LeBron James','Kevin Durant','Stephen Curry','Stephen Curry','Russell Westbrook','James Harden','Giannis Antetokounmpo'],index=[1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019])
DPOY_Awards = pd.DataFrame(['Sidney Moncrief','Sidney Moncrief','Mark Eaton','Alvin Robertson','Michael Cooper','Michael Jordan','Mark Eaton','Dennis Rodman','Dennis Rodman','David Robinson','Hakeem Olajuwon','Hakeem Olajuwon','Dikembe Mutombo','Gary Payton','Dikembe Mutombo','Dikembe Mutombo','Alonzo Mourning','Alonzo Mourning','Dikembe Mutombo','Ben Wallace','Ben Wallace','Metta World Peace','Ben Wallace','Ben Wallace','Marcus Camby','Kevin Garnett','Dwight Howard','Dwight Howard','Dwight Howard','Tyson Chandler','Marc Gasol','Joakim Noah','Kawhi Leonard','Kawhi Leonard','Draymond Green','Rudy Gobert','Rudy Gobert'],index=[1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019])
Sixth_Man_Awards = pd.DataFrame(['Bobby Jones','Kevin McHale','Kevin McHale','Bill Walton','Ricky Pierce','Roy Tarpley','Eddie Johnson','Ricky Pierce','Detlef Schrempf','Detlef Schrempf','Clifford Robinson','Dell Curry','Anthony Mason','Toni Kukoc','John Starks','Danny Manning','Darrel Armstrong','Rodney Rogers','Aaron McKie','Corliss Williamson','Bobby Jackson','Antawn Jamison','Ben Gordon','Mike Miller','Leandro Barbosa','Manu Ginobili','Jason Terry','Jamal Crawford','Lamar Odom','James Harden','JR Smith','Jamal Crawford','Lou Williams','Jamal Crawford','Eric Gordon','Lou Williams','Lou Williams'],index=[1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019])

stats['MVP'] = 0
stats['DPOY'] = 0
stats['Sixth Man'] = 0

for i in MVP_Awards.index:
    stats['MVP'].loc[(stats['Player'] == MVP_Awards[0][i]) & (stats['Season'] == i)] = 1
    
for i in DPOY_Awards.index:
    stats['DPOY'].loc[(stats['Player'] == DPOY_Awards[0][i]) & (stats['Season'] == i)] = 1
    
for i in Sixth_Man_Awards.index:
    stats['Sixth Man'].loc[(stats['Player'] == Sixth_Man_Awards[0][i]) & (stats['Season'] == i)] = 1


# Resetting Indexes so data is traversable
stats = stats.reset_index()
stats.drop('index',inplace=True,axis=1)

team_stats = team_stats.reset_index()
team_stats.drop('index',inplace=True,axis=1)

# Dropping 'Games Behind' Statistic from team stats
team_stats.drop('GB',inplace=True,axis=1)

# Changing team_stats datatypes    
team_stats = team_stats.astype({'W': 'int32', 'L: 'int32', 'PS/G': 'float', 'W/L%': 'float', 'PS/G': 'float', 'PA/G': 'float', 'SRS': 'float'})

   
