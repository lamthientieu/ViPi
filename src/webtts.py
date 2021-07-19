#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from actions import say
from flask import Flask, request
from flask_restful import Resource, Api
import threading
app = Flask(__name__)
api = Api(app)

def start_server():
    app.run(host='0.0.0.0',port=5001)

def main():
        class tts(Resource):
            def get(self):
                message = request.args.get('message', default = 'This is a test!')
                say(message)
                return {'status': 'OK'}
        api.add_resource(tts, '/tts')
        server = threading.Thread(target=start_server,args=())
        server.setDaemon(True)
        server.start()

if __name__ == '__main__':
    main()