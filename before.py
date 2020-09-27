import os
import subprocess
import configparser

credentials = configparser.ConfigParser()
credentials.read('/opt/media-server/credentials.ini')

IP = (subprocess.check_output(["hostname -I | cut -d' ' -f1"], shell=True)
        .split()[0]
        .decode('ascii'))

os.system('''sed -i 's/${OWNIP}/%s/g' /opt/media-server/config/bazarr/config/config.ini'''%IP)

if credentials["OPENSUBTITLES"]:
    os.system('''sed -i 's/${opensubtitles_username}/%s/g' /opt/media-server/config/bazarr/config/config.ini'''
                            %credentials["OPENSUBTITLES"]['Username'])
    os.system('''sed -i 's/${opensubtitles_password}/%s/g' /opt/media-server/config/bazarr/config/config.ini'''
                            %credentials["OPENSUBTITLES"]['Password'])

username = ''
md5_pass = ''
if credentials["INTERFACE"]:
    username = credentials["INTERFACE"]['Username']
    md5_pass = hashlib.md5(credentials["INTERFACE"]['Password'].encode()).hexdigest()

    
    os.system('''sed -i 's/${AUTH_TYPE}/%s/g' /opt/media-server/config/bazarr/config/config.ini'''
                            %'basic')
else:
    os.system('''sed -i 's/${AUTH_TYPE}/%s/g' /opt/media-server/config/bazarr/config/config.ini'''
                            %'None')


os.system('''sed -i 's/${AUTH_NAME}/%s/g' /opt/media-server/config/bazarr/config/config.ini'''
                        %username)
                        
os.system('''sed -i 's/${AUTH_PASS}/%s/g' /opt/media-server/config/bazarr/config/config.ini'''
                        %md5_pass)