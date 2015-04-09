import requests # installed with C:\Python34\ > python -m pip install requests
import re
import socket
import time
#import json
 
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname) # or just write ex. 192.168.1.7
 
UTORRENT_URL = 'http://%s:%s/gui/' % (IP, '2323')
UTORRENT_URL_TOKEN = '%stoken.html' % UTORRENT_URL
UTORRENT_TORRENT_LIST = UTORRENT_URL + '?list=1&'
REGEX_UTORRENT_TOKEN = r'<div[^>]*id=[\"\']token[\"\'][^>]*>([^<]*)</div>'
 
auth = requests.auth.HTTPBasicAuth('admin', 'admin')
json_data = ""
 
def progresso_torrent():
    global json_data
    l = requests.get(UTORRENT_TORRENT_LIST, auth=auth, cookies=cookies)
 
    json_data = l.text
    #data = json.loads(json_data) # non parsiamo il json, ma effettuiamo una semplice ricerca all'interno del documento.
    indice_start = json_data.find(',"Downloading', 0) + 2
    if indice_start > 5:
        indice_stop = json_data.find('"', indice_start)
        string_progresso = json_data[indice_start:indice_stop]
        perc_progresso = string_progresso.split()[1] # progress in percentage
 
        try:
          if type(float(perc_progresso)) is not float:
            perc_progresso = float(perc_progresso)
        except ValueError:
          perc_progresso = 0
    else:
        perc_progresso = 100
 
    print("Progresso torrent: "+str(perc_progresso)+"%")
    return perc_progresso
 
try:
    r = requests.get(UTORRENT_URL_TOKEN, auth=auth)
    #print(r)
 
    token = re.search(REGEX_UTORRENT_TOKEN, r.text).group(1)
    guid = r.cookies['GUID']
    cookies = dict(GUID = guid)
    print("Token uTorrent: "+ token)
    UTORRENT_TORRENT_LIST += ('token=%s' % token)
 
 
except requests.exceptions.ConnectionError:
    print("Connection refused, make sure the uTorrent WebAPI are running with the right port number and access credentials")
 
except requests.packages.urllib3.exceptions.ProtocolError:
    print("protocol error")
 
# function to get the file list in uTorrent...
 
'''
params = {'action':'add-file','token': token}
files = {'torrent_file': open('C:\\x.torrent', 'rb')}
r = requests.post(url=UTORRENT_URL, auth=auth, cookies=cookies, params=params, files=files)
'''
 
if __name__ == "__main__":
    mins = 1
    while mins:
            print("request number "+str(mins))
 
            # printing torrent download progress
            progresso_torrent()
            print("...")
 
            # Sleep for half a minute
            time.sleep(30)
            # Increment the mins total
            mins += 1
