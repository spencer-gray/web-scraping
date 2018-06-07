import bs4 as bs
import urllib.request
import csv

city_abr = 'chi'
year = '1988'
previous_year = str(int(year)-1)
league = 'nba'

url = 'http://www.espn.com/'+league+'/team/stats/_/name/'+city_abr+'/year/'+year+'/seasontype/2'

sauce = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(sauce, 'lxml')

file_name = city_abr+'_'+league+'_team_stats_'+previous_year+'-'+year

tables = soup.find_all('table', {'class': "tablehead"})


with open(file_name+'.csv', 'w') as csvfile:
    writeCSV = csv.writer(csvfile, delimiter=',')
    for table in tables:
        table_rows = table.find_all('tr')[1:] #[1:] will remove the title of the current table (espn stores it as a tr)
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            
            writeCSV.writerow(row)





