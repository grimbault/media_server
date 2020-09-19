import os 
import json
import sqlite3
import xml.etree.ElementTree as ET
import subprocess
import configparser

# Country codes (for subtitles download)
languages=['EN', 'FR']

credentials = configparser.ConfigParser()
credentials.read('credentials.ini')

IP = subprocess.check_output(["hostname -I | cut -d' ' -f1"], shell=True)
        .split()[0]
        .decode('ascii')

os.system('''sed -i 's/${OWNIP}/%s/g' config/bazarr/config/config.ini'''%IP)

if credentials["OPENSUBTITLES"]:
    os.system('''sed -i 's/${opensubtitles_username}/%s/g' config/bazarr/config/config.ini'''
                            %credentials["OPENSUBTITLES"]['Username'])
    os.system('''sed -i 's/${opensubtitles_password}/%s/g' config/bazarr/config/config.ini'''
                            %credentials["OPENSUBTITLES"]['Password'])

with open('config/jackett/Jackett/ServerConfig.json') as f:
    data = json.load(f)
jackettAPI=data['APIKey']

radarrAPI=''
root = ET.fromstring('config/radarr/config.xml')
for child in root:
    if (child.tag=='ApiKey'):
        os.system('''sed -i 's/${sonarr_key}/%s/g' config/bazarr/config/config.ini'''
                                %child.text)

sonarrAPI=''
root = ET.fromstring('config/sonarr/config.xml')
for child in root:
    if (child.tag=='ApiKey'):
        os.system('''sed -i 's/${sonarr_key}/%s/g' config/bazarr/config/config.ini'''
                                %child.text)

for tool in ['sonarr', 'radarr']:
    conn = sqlite3.connect('config/%s/nzbdrone.db'%i)

    c = conn.cursor()

    # Adding the deluge client
    c.execute('''CREATE TABLE IF NOT EXISTS "DownloadClients" (
        "Id" INTEGER NOT NULL,
        "Enable" INTEGER NOT NULL,
        "Name" TEXT NOT NULL,
        "Implementation" TEXT NOT NULL,
        "Settings" TEXT NOT NULL,
        "ConfigContract" TEXT NOT NULL,
        PRIMARY KEY ("Id" AUTOINCREMENT));''')

    c.execute('''DELETE FROM "DownloadClients"''')
    c.execute('''INSERT INTO "DownloadClients" VALUES (1,1,'deluge','Deluge',
        '{  
            "host": "%s",  
            "port": 8112,  
            "password": "deluge",  
            "movieCategory": "%s",  
            "recentMoviePriority": 0,  
            "olderMoviePriority": 0,  
            "addPaused": false,  
            "useSsl": false
        }','DelugeSettings')''' % IP, tool)


    # Additionals columns for radarr
    columns=''
    if tool=='radarr':
        columns=''', NULL, '[{ "format": 0, "allowed": true }]', 0'''

    # Adding/Modifying the profiles
    c.execute('''DELETE FROM "Profiles"''')

    for index, language in enumerate(languages):
        
        c.execute('''INSERT INTO "Profiles" VALUES (%s,'Any %s',3,'[  
            {    "quality": 0,    "allowed": false  },  
            {    "quality": 1,    "allowed": false  },  
            {    "quality": 8,    "allowed": false  },  
            {    "quality": 2,    "allowed": false  },  
            {    "quality": 4,    "allowed": true  },  
            {    "quality": 9,    "allowed": true  },  
            {    "quality": 10,    "allowed": false  },  
            {    "quality": 5,    "allowed": true  },  
            {    "quality": 6,    "allowed": true  },  
            {    "quality": 3,    "allowed": true  },  
            {    "quality": 7,    "allowed": true  },  
            {    "quality": 16,    "allowed": false  },  
            {    "quality": 18,    "allowed": false  }, 
            {    "quality": 19,    "allowed": false  }
            ]',%s %s)'''%((index-1)*4)+index, language, index, columns))
        c.execute('''INSERT INTO "Profiles" VALUES (%s,'720p %s',5,'[  
            {    "quality": 0,    "allowed": false  },  
            {    "quality": 1,    "allowed": false  },  
            {    "quality": 8,    "allowed": false  },  
            {    "quality": 2,    "allowed": false  },  
            {    "quality": 4,    "allowed": true  },  
            {    "quality": 9,    "allowed": false  },  
            {    "quality": 10,    "allowed": false  },  
            {    "quality": 5,    "allowed": true  },  
            {    "quality": 6,    "allowed": true  },  
            {    "quality": 3,    "allowed": false  },  
            {    "quality": 7,    "allowed": false  },  
            {    "quality": 16,    "allowed": false  },  
            {    "quality": 18,    "allowed": false  },  
            {    "quality": 19,    "allowed": false  }
            ]',%s %s)'''%((index-1)*4)+index+1, language, index, columns))
        c.execute('''INSERT INTO "Profiles" VALUES (%s,'1080p %s',3,'[  
            {    "quality": 0,    "allowed": false  },  
            {    "quality": 1,    "allowed": false  },  
            {    "quality": 8,    "allowed": false  },  
            {    "quality": 2,    "allowed": false  },  
            {    "quality": 4,    "allowed": false  }, 
            {    "quality": 9,    "allowed": true  },  
            {    "quality": 10,    "allowed": false  },  
            {    "quality": 5,    "allowed": false  },  
            {    "quality": 6,    "allowed": false  },  
            {    "quality": 3,    "allowed": true  },  
            {    "quality": 7,    "allowed": true  },  
            {    "quality": 16,    "allowed": false  },  
            {    "quality": 18,    "allowed": false  },  
            {    "quality": 19,    "allowed": false  }
            ]',%s %s)'''%((index-1)*4)+index+2, language, index, columns))
        c.execute('''INSERT INTO "Profiles" VALUES (%s,'Ultra-HD %s',19,'[  
            {    "quality": 0,    "allowed": false  }, 
            {    "quality": 1,    "allowed": false  },  
            {    "quality": 8,    "allowed": false  },  
            {    "quality": 2,    "allowed": false  },  
            {    "quality": 4,    "allowed": false  },  
            {    "quality": 9,    "allowed": false  },  
            {    "quality": 10,    "allowed": false  },  
            {    "quality": 5,    "allowed": false  },  
            {    "quality": 6,    "allowed": false  },  
            {    "quality": 3,    "allowed": false  },  
            {    "quality": 7,    "allowed": false  },  
            {    "quality": 16,    "allowed": true  },  
            {    "quality": 18,    "allowed": true  },  
            {    "quality": 19,    "allowed": true  }
            ]',%s %s)'''%((index-1)*4)+index+3, language, index, columns))

    # Specificities from radarr & sonarr
    columns=''
    if tool=='radarr':
        columns=''',"requiredFlags": [],  "multiLanguages": [],  "categories": [    
            2000,   
            2010,   
            2020,    
            2030,    
            2035,    
            2040,   
            2045,    
            2050,    
            2060  
            ], "animeCategories": [], "removeYear": false, "searchByTitle": false'''
    else:
        columns=''',"seedCriteria": {},  "apiPath": "/api",  "categories": [
            5030,    
            5040, 
            5070  
            ], "animeCategories": [5070]'''

    indexers=[
        {
            "name":"1337x", 
            "url":"http://%s:9117/api/v2.0/indexers/1337x/results/torznab/"% IP
        }, {
            "name":"anirena", 
            "url":"http://%s:9117/api/v2.0/indexers/aniRena/results/torznab/"% IP
        }, {
            "name":"epizod", 
            "url":"http://%s:9117/api/v2.0/indexers/epizod/results/torznab/"% IP
        }, {
            "name":"gktorrent", 
            "url":"http://%s:9117/api/v2.0/indexers/gktorrent/results/torznab/"% IP
        }, {
            "name":"kickasstorrent", 
            "url":"http://%s:9117/api/v2.0/indexers/kickasstorrent/results/torznab/"% IP
        }, {
            "name":"nyaa", 
            "url":"http://%s:9117/api/v2.0/indexers/nyaasi/results/torznab/"% IP
        }, {
            "name":"oxtorrent", 
            "url":"http://%s:9117/api/v2.0/indexers/oxtorrent/results/torznab/"% IP
        }, {
            "name":"tpb", 
            "url":"http://%s:9117/api/v2.0/indexers/thepiratebay/results/torznab/"% IP
        }, {
            "name":"torrent9", 
            "url":"http://%s:9117/api/v2.0/indexers/torrent9/results/torznab/"% IP
        },
    ]
    
    # Adding Indexers
    c.execute('''DELETE FROM "Indexers"''')
    uKey=1
    for indexer in indexers:
        c.execute('''INSERT INTO "Indexers" VALUES (%d,'%s','Torznab','{  
            "minimumSeeders": 1,  
            "baseUrl": "%s",  
            "apiKey": "%s" %s
            }','TorznabSettings',1,1)'''%(uKey, 
                                          indexer["name"], 
                                          indexer["url"], 
                                          jackettAPI, 
                                          columns) )
        uKey+=1
    
    # Adding RootFolders
    columns=''
    if tool=='radarr':
        columns='''/movies/'''
    else:
        columns='''/tv/'''

    c.execute('''DELETE FROM "RootFolders"''')
    c.execute('''INSERT INTO "RootFolders" VALUES (1,'%s')'''%columns)
    
    conn.commit()
    conn.close()
