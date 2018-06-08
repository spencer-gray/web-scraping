import bs4 as bs
import urllib.request
import csv
import argparse
import sys

# converts city/team name to the appropriate abbreviation #
def to_abbr(item):
    nameToAbbr = {'anaheim': 'ana', 'arizona': 'ari', 'atlanta': 'atl', 'baltimore': 'bal', 'boston': 'bos', 'brooklyn': 'bkn', 'buffalo': 'buf',
                  'calgary': 'cgy', 'carolina': 'car', 'charlotte': 'cha', 'chicago': 'chi', 'cincinnati': 'cin', 'cleveland': 'cle', 'colorado': 'col', 
                  'columbus': 'cbj', 'dallas': 'dal', 'denver': 'den', 'detroit': 'det', 'edmonton': 'edm', 'florida': 'fla', 'golden_state': 'gs',
                  'green_bay': 'gb', 'houston': 'hou', 'indiana': 'ind', 'jacksonville': 'jax', 'kansas': 'kc', 'los_angeles': 'la', 'los_angeles_clippers': 'lac',
                  'los_angeles_chargers': 'lac', 'los_angeles_rams': 'lar', 'los_angeles_lakers': 'lak', 'memphis': 'mem', 'miami': 'mia', 'milwaukee': 'mil',
                  'minnesota': 'min', 'montreal': 'mtl', 'nashville': 'nsh', 'new_england': 'ne', 'new_jersey': 'nj', 'new_orleans': 'no', 'new_york': 'ny',
                  'new_york_giants': 'nyg', 'new_york_jets': 'nyj', 'new_york_islanders': 'nyi', 'new_york_rangers': 'nyr', 'oakland': 'oak', 
                  'oklahoma_city': 'okc', 'orlando': 'orl', 'ottawa': 'ott','philadelphia': 'phi', 'phoenix': 'phx', 'pittsburgh': 'pit', 'portland': 'por', 
                  'sacramento': 'sac', 'san_antonio': 'sa', 'san_francisco': 'sf', 'san_jose': 'sj', 'seattle': 'sea', 'st_louis': 'stl', 'tampa_bay': 'tb', 
                  'tennessee': 'ten', 'toronto': 'tor', 'utah': 'utah', 'vancouver': 'van', 'vegas': 'vgs', 'washington': 'wsh', 'winnipeg': 'wpg'}

    #if city name has a team in the big 4 NA leauges
    if item in nameToAbbr:   
        return nameToAbbr[item]
    else:
        sys.exit('Invalid city name (cities with multiple teams in one sport will require team name ie: new york giants.)')


# writes the specified data to an appropriately named csv file #
def write_to_csv(file, data, url):
        
    with open(file+'.csv', 'w') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
        for table in data:
            table_rows = table.find_all('tr')#[1:] #[1:] will remove the title of the current table (espn stores it as a tr)
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                
                writeCSV.writerow(row)


parser = argparse.ArgumentParser(description='scrape specific team stats from ESPN (4 Major NA Sports)')

parser.add_argument("city_input", help="the city name to be searched")
parser.add_argument("yr_input", help="the year to be searched")
parser.add_argument("league_input", help="which league will be searched (nhl/nba/nfl/mlba)")

args = parser.parse_args()

city = args.city_input.lower()
year = args.yr_input
previous_year = str(int(year)-1)
league = args.league_input.lower()

city_abr = to_abbr(city)

url = 'http://www.espn.com/'+league+'/team/stats/_/name/'+city_abr+'/year/'+year+'/seasontype/2'
file_name = city_abr+'_'+league+'_team_stats_'+previous_year+'-'+year

# read in required tables from the url
sauce = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(sauce, 'lxml')
tables = soup.find_all('table', {'class': "tablehead"})   

write_to_csv(file_name, tables, url)
