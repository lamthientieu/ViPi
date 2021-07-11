# !/usr/bin/python3
# -*- coding: utf-8 -*-
#-*-coding:gb2312-*-

"""Run small webservice for oath."""
import json
import sys
from pathlib import Path
import os
from pathlib import Path
import os.path
import pathlib2 as pathlib
import cherrypy
import socket
from requests_oauthlib import OAuth2Session
from google.oauth2.credentials import Credentials
from google.assistant.library.file_helpers import existing_file
ROOT_PATH = os.path.realpath(os.path.join(__file__, '..', '..'))
USER_PATH = os.path.realpath(os.path.join(__file__, '..', '..','..'))
oauth_json = os.path.join(os.path.expanduser('~/'),'ViPi','vipi.json')
data = {"installed":{"client_id":"id","project_id":"project_id","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"secret","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}
if os.path.exists(oauth_json)==False:
    with open  (oauth_json,"w") as f:
        json.dump(data,f,ensure_ascii=False,indent=4)
class oauth2Site(object):
    """Website for handling oauth2."""


    def __init__(self):
        """Init webpage."""
        self.cred_file = os.path.join(os.path.expanduser('~/.config'),'google-oauthlib-tool','credentials.json')
        self.user_data = self.readf()
        self.oauth2 = OAuth2Session(
                self.user_data['client_id'],
                redirect_uri='urn:ietf:wg:oauth:2.0:oob',
                scope=["https://www.googleapis.com/auth/assistant-sdk-prototype", "https://www.googleapis.com/auth/gcm"]
            )
        self.auth_url, _ = self.oauth2.authorization_url(self.user_data['auth_uri'], access_type='offline', prompt='consent')  
        self.ip_address = socket.gethostbyname(socket.gethostname()+ ".local")
    def readf(self):
        with open(oauth_json,'r') as data:
            user_data = json.load(data)['installed']
        return  user_data
        
    @cherrypy.expose
    def index(self):
        return str("""
        <html><body>
            <h2>Hãy chắc chắn bạn đã chuẩn bị file json</h2>
            <form action="upload" method="post" enctype="multipart/form-data">
            Bước 1: Chọn file json <input type="file" name="myFile" /><br />
            <button type="submit"> Bước 2: Tải tệp lên </button>
            </form>
            <form action="edit_config" method="get" >      
            <button type="submit"> Chỉnh sửa config </button> <a href="http://{ip_address}:8081" target="_blank">>> Bấm vào đây</a>           
            </form>
        </body></html>
        """).format(ip_address=self.ip_address)

    @cherrypy.expose
    def upload(self, myFile):
        size = 0
        whole_data = bytearray() # Neues Bytearray
        while True:
            data = myFile.file.read(8192)
            whole_data += data # Save data chunks in ByteArray whole_data
            if not data:
                break
            written_file = open(oauth_json, "wb") # open file in write bytes mode
            written_file.write(whole_data) # write file
        return str("""<html>
          <head>Liên kết Google</head>
          <body>
          <h2>Liên kết Google</h2>
            <p>
                Bước 3: Lấy token: <a href="{url}" target="_blank">>> Bấm vào đây, sau đó copy mã</a>
            </p>
            <form method="get" action="token">
              <input type="text" value="" name="token" />
              <button type="submit">Bước 4: Dán mã vào ô bên cạnh rồi bấm vào đây</button>
            </form>
            <form action="edit_config" method="get" >      
            <button type="submit"> Chỉnh sửa config </button>
            <a href="http://{ip_address}:8081" target="_blank">>> Bấm vào đây</a>          
            </form>            
          </body>
        </html>""").format(url=self.auth_url,ip_address=self.ip_address)
    @cherrypy.expose

    def token(self, token):
        self.oauth2.fetch_token(self.user_data['token_uri'], client_secret=self.user_data['client_secret'], code=token)
        # create credentials
        credentials = Credentials(
            self.oauth2.token['access_token'],
            refresh_token=self.oauth2.token.get('refresh_token'),
            token_uri=self.user_data['token_uri'],
            client_id=self.user_data['client_id'],
            client_secret=self.user_data['client_secret'],
            scopes=self.oauth2.scope
        )
        pathlib.Path(os.path.dirname(self.cred_file)).mkdir(exist_ok=True)
        with open(self.cred_file,'w') as json_file:
            json.dump({
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes,
            },json_file)

        return str("""
        <html><body>
            <h2>Chỉnh sửa config.yaml</h2>
            <form action="edit_config" method="get" >      
            <button type="submit"> Chỉnh sửa config </button>
            <a href="http://{ip_address}:8081" target="_blank">>> Bấm vào đây</a>            
            </form>
        </body></html>
        """).format(ip_address=self.ip_address)
    @cherrypy.expose
    def edit_config(self):
        data = ROOT_PATH + '/src/config.yaml'
        from yaml_editor.editor import main
        main(data)
        return str("""
        <html><body>
            <h2>Chỉnh sửa config.yaml</h2>
            <form action="edit_config" method="get" >      
            <button type="submit"> Chỉnh sửa config </button>
            <a href="http://{ip_address}:8081" target="_blank">>> Bấm vào đây</a>            
            </form>
        </body></html>
        """).format(ip_address=self.ip_address)       

if __name__ == '__main__':
    config_dir =  os.path.join(os.path.expanduser('~/'),'.config','google')
    pathlib.Path(os.path.dirname(config_dir)).mkdir(exist_ok=True)
    cherrypy.config.update({'server.socket_port': 8080, 'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(oauth2Site())