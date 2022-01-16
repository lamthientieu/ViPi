#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-*-coding:gb2312-*-
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
# ViPi_0.2_13_04_2014_Thay đổi trình phát nhạc Youtube
"""Sample that implements a gRPC client for the Google Assistant API."""
print('[ViPi_0.2] + [KHỞI ĐỘNG CHƯƠNG TRÌNH]')

import concurrent.futures 
import json, logging, os, os.path, sys, time, uuid
import pathlib2 as pathlib
try:
    import RPi.GPIO as GPIO
except Exception as e:
    GPIO = None
 
import argparse, subprocess, click, grpc, psutil, re, requests, random, google.auth.transport.grpc, google.auth.transport.requests, google.oauth2.credentials,signal, pvporcupine, pyaudio, soundfile, struct
from actions import say, app_music, app_music_auto, app_music_random, on_ir_receive,stop, radio, feed, command_read_story, vlcplayer, configuration, custom_action_keyword, app_custom_weather, say, say_save, command_lunar_calendar, install
from news import app_news_radio
from termcolor import colored
from threading import Thread
from knowledge_base import kb
if GPIO!=None and configuration['Gpios']['control']=='Enabled':
    from indicator import ctr_led, stoppushbutton,irreceiver
    ctr_led('off')
    ctr_led('speaking')                                        
    GPIOcontrol=True
else:
    irreceiver=None
    GPIOcontrol=False
from actions import gender

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)
from tenacity import retry, stop_after_attempt, retry_if_exception

try:
    from googlesamples.assistant.grpc import (
        assistant_helpers,
        audio_helpers,
        browser_helpers,
        device_helpers
    )
except (SystemError, ImportError):
    import assistant_helpers, audio_helpers, browser_helpers, device_helpers

ROOT_PATH = os.path.realpath(os.path.join(__file__, '..', '..'))
USER_PATH = os.path.realpath(os.path.join(__file__, '..', '..','..'))
hotword = ROOT_PATH+'/src/hotword.detect'
if GPIOcontrol:
    #GPIO Declarations
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pushbuttontrigger=configuration['Gpios']['pushbutton_trigger'][0]
    GPIO.setup(pushbuttontrigger, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#Sonoff-Tasmota Declarations
#Make sure that the device name assigned here does not overlap any of your smart device names in the google home app
#tasmota_devicelist=configuration['Tasmota_devicelist']['friendly-names']
#tasmota_deviceip=configuration['Tasmota_devicelist']['ipaddresses']
api_endpoint = ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
END_OF_UTTERANCE = embedded_assistant_pb2.AssistResponse.END_OF_UTTERANCE
DIALOG_FOLLOW_ON = embedded_assistant_pb2.DialogStateOut.DIALOG_FOLLOW_ON
CLOSE_MICROPHONE = embedded_assistant_pb2.DialogStateOut.CLOSE_MICROPHONE
PLAYING = embedded_assistant_pb2.ScreenOutConfig.PLAYING
grpc_deadline = DEFAULT_GRPC_DEADLINE = 600 * 3 + 5
language_code, display, device_id, device_model_id, project_id  = 'en-US',True,'Loa-ViPi',configuration['Google_Assistant']['device_model_id'], configuration['Google_Assistant']['project_id']
device_config=os.path.join(os.path.expanduser('~/.config'),'googlesamples-assistant','device_config_library.json')
credential=os.path.join(os.path.expanduser('~/.config'),'google-oauthlib-tool','credentials.json')
audio_sample_rate,audio_sample_width, audio_iter_size,audio_block_size, audio_flush_size=audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE, audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH, audio_helpers.DEFAULT_AUDIO_ITER_SIZE, audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE, audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE 

with open(credential, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))
http_request = google.auth.transport.requests.Request()
credentials.refresh(http_request)
grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
    credentials, http_request, api_endpoint)

# Configure audio source and sink.
audio_device = None
audio_source = audio_device = (
    audio_device or audio_helpers.SoundDeviceStream(
        sample_rate=audio_sample_rate,
        sample_width=audio_sample_width,
        block_size=audio_block_size,
        flush_size=audio_flush_size
    )
)

audio_sink = audio_device = (
    audio_device or audio_helpers.SoundDeviceStream(
        sample_rate=audio_sample_rate,
        sample_width=audio_sample_width,
        block_size=audio_block_size,
        flush_size=audio_flush_size
    )
)
# Create conversation stream with the given audio source and sink.
conversation_stream = audio_helpers.ConversationStream(
    source=audio_source,
    sink=audio_sink,
    iter_size=audio_iter_size,
    sample_width=audio_sample_width,
)

once = False
try:
    import speech_recognition as sr
except:
    install('speech-recognition-fork')
    import speech_recognition as sr
    
import time
from ctypes import *
from contextlib import contextmanager
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)
WIT_AI_KEY = "S55S7HV3KOHKBZNTJXR6YJRX2PFFSVGV"
# Check if VLC is paused
def checkvlcpaused():
    state=vlcplayer.state()
    if str(state)=="State.Paused":
        currentstate=True
    else:
        currentstate=False
    return currentstate
if configuration['Home_Assistant']['control']=='Enabled':
    from hass_skill import hass

#Function to control Sonoff Tasmota Devices
def tasmota_control(phrase,devname,devip):
    if custom_action_keyword['Dict']['On'] in phrase:
        try:
            rq=requests.head("http://"+devip+"/cm?cmnd=Power%20on")
            say("Tunring on "+devname)
        except requests.exceptions.ConnectionError:
            say("Device not online")
    elif custom_action_keyword['Dict']['Off'] in phrase:
        try:
            rq=requests.head("http://"+devip+"/cm?cmnd=Power%20off")
            say("Tunring off "+devname)
        except requests.exceptions.ConnectionError:
            say("Device not online")

#Check if custom wakeword has been enabled
if configuration['Wakewords']['Custom_Wakeword']=='Enabled':
    custom_wakeword=True
elif GPIOcontrol==False:
    print("Pushbutton trigger is not configured. So forcing custom wakeword ON.")
    custom_wakeword=True
else:
    custom_wakeword=False
picovoice_models=configuration['Wakewords']['Picovoice_wakeword_models']
keyword_paths = picovoice_models
wakeword_length=len(picovoice_models)
interrupted=False                 


def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted
mediastopbutton=True

#Custom Conversation
numques,numans =len(configuration['Conversation']['question']), len(configuration['Conversation']['answer'])
kw,cw,allcmd=custom_action_keyword['keyword'],custom_action_keyword['Cutwords'],custom_action_keyword['commands']
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
url, thoigian, thoitiet, thongdich, timdt, duocroi, amluong,   = 'http://127.0.0.1:5001/command', {'message':'mấy giờ rồi'}, {'message':'thời tiết hôm nay thế nào'}, {'message':'thông dịch'}, {'message':'tìm điệN thoại'},  {'message':'tất nhiên'}, {'message':'âm lượng tối đa'}
app = Flask(__name__)
api = Api(app)
class GoogleAssistant(object):
    def __init__(self, language_code, device_model_id, device_id,
                 conversation_stream, display,
                 channel, deadline_sec,device_handler):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_stream = conversation_stream
        self.display = display
        if GPIOcontrol and stoppushbutton != 0:
            self.t3 = Thread(target=self.stopbutton)
            self.t3.start()
        if GPIOcontrol and irreceiver!=None:
            self.t4 = Thread(target=self.ircommands)
            self.t4.start()
        self.conversation_state = None
        # Force reset of first conversation.
        self.is_new_conversation = True
        # Create Google Assistant API gRPC client.
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(
            channel
        )
        self.deadline = deadline_sec
        self.device_handler = device_handler
    def stopbutton(self):
        if GPIOcontrol:
            while mediastopbutton:
                time.sleep(0.25)
                if not GPIO.input(stoppushbutton):
                    print('Stopped')
                    vlcplayer.stop_vlc()
    
    def ircommands(self):
        try:
            requests.get(url,amluong)
        except:
            pass
        try:
            requests.get(url,'max volume')
        except:
            pass
        if GPIOcontrol:
            ctr_led('off')
        if irreceiver!=None:
            try:
                print("IR Sensor Started")
                while 1:
                    time.sleep(.1)
                    GPIO.wait_for_edge(irreceiver, GPIO.FALLING)
                    code = on_ir_receive(irreceiver)
                    if code:
                        for codenum, usercode in enumerate(configuration['IR']['Codes']):
                            if usercode==code:
                                print (configuration['IR']['Commands'][codenum])
                                if 'next' in (configuration['IR']['Commands'][codenum]).lower():
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    self.ctr_med('med_next_player',configuration['IR']['Commands'][codenum].lower())
                                elif 'prev' in (configuration['IR']['Commands'][codenum]).lower():
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    self.ctr_med('med_previous_player',configuration['IR']['Commands'][codenum].lower())
                                elif 'play' in (configuration['IR']['Commands'][codenum]).lower():
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    self.ctr_med('med_pause_player','Play')
                                elif 'volup' in (configuration['IR']['Commands'][codenum]).lower():
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    self.ctr_med('med_volume_up',configuration['IR']['Commands'][codenum].lower())
                                elif 'voldown' in (configuration['IR']['Commands'][codenum]).lower():
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    self.ctr_med('med_volume_down',configuration['IR']['Commands'][codenum].lower())
                                elif 'news' in (configuration['IR']['Commands'][codenum]).lower():
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    self.ctr_app('app_news_radio','')
                                elif 'story' in (configuration['IR']['Commands'][codenum]).lower():
                                    co_tich=configuration['IR']['Story_list']
                                    truyen = random.choice(co_tich)
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    self.ctr_app('app_read_story',truyen)
                                elif 'music' in (configuration['IR']['Commands'][codenum]).lower():
                                    nhac=configuration['IR']['Music_list']
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    self.ctr_app('app_music_auto',random.choice(nhac))
                                elif 'stop' in (configuration['IR']['Commands'][codenum]).lower():
                                    vlcplayer.stop_vlc()
                                elif 'assistant' in (configuration['IR']['Commands'][codenum]).lower():
                                    self.assist()
                                elif 'mute' in (configuration['IR']['Commands'][codenum]).lower():
                                    self.stopbutton()
                                elif 'time' in (configuration['IR']['Commands'][codenum]).lower():
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    try:
                                        requests.get(url,thoigian)
                                    except:
                                        pass
                                elif 'weather' in (configuration['IR']['Commands'][codenum]).lower():
                                    if GPIOcontrol:
                                        ctr_led('speaking')
                                    try:   
                                        requests.get(url,thoitiet)
                                    except:
                                        pass
            except KeyboardInterrupt:
                pass
            except RuntimeError:
                pass
            print("Stopping IR Sensor")

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False
        self.conversation_stream.close()

    def is_grpc_error_unavailable(e):
        is_grpc_error = isinstance(e, grpc.RpcError)
        if is_grpc_error and (e.code() == grpc.StatusCode.UNAVAILABLE):
            logging.error('grpc unavailable error: %s', e)
            return True
        return False

    @retry(reraise=True, stop=stop_after_attempt(100),
           retry=retry_if_exception(is_grpc_error_unavailable))
    def ctr_app(self,skill,pure_data):
        if skill=='app_music_play':
            vlcplayer.stop_vlc()
            say_save('Chuẩn bị phát nhạc')
            for item in kw[skill]:
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())
            app_music(pure_data.lower())
            return False
        if skill=='app_music_auto':
            vlcplayer.stop_vlc()
            for item in kw[skill]:
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())
            say_save('Chuẩn bị phát danh sách nhạc'+pure_data)
            app_music_auto(str(pure_data).lower())
            if GPIOcontrol:
                ctr_led('off')
            return False      
        if skill=='app_read_story':
            vlcplayer.stop_vlc()
            for item in kw[skill]:
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())
            say_save('Chuẩn bị kể chuyện'+pure_data)
            command_read_story(str(pure_data).lower())
            if GPIOcontrol:
                ctr_led('off') 
            return False
        if skill=='app_lunar_calendar':
            say_save('Xin chờ tôi kiểm tra lịch')
            for item in kw[skill]:
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())
            command_lunar_calendar(pure_data.lower())
            return self.assist()
        if skill=='app_news_radio' and configuration['app_news_radio'] == 'Enabled' :
            import time
            for item in kw[skill]:
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())
            if ('thời sự' or 'hài' or 'báo mới' or 'thể thao' or 'hài' or 'báo nói' or 'âm nhạc') not in pure_data:
                vlcplayer.stop_vlc()
                say_save('Bạn muốn nghe thời sự, âm nhạc, thể thao, hài, 18 cộng, hay tin mới?')
                time.sleep(1)
            pure_data = re_ask()
            app_news_radio(pure_data.lower())
            if GPIOcontrol:
                ctr_led('off')
            return False
        if skill=='app_custom_weather' and configuration['Weather']['control'] == 'Enabled':
            import time
            for item in kw[skill]:
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())
            app_custom_weather(pure_data.lower())
            time.sleep(5)
            return self.assist()
        if skill=='app_chromecast_play' and configuration['Chromecast']['Chromecast_Control'] == 'Enabled':
            vlcplayer.stop_vlc()
            for item in (kw[skill]+kw['app_music_play']):
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())                          
            try:
                chromecast_play_video(str(pure_data).lower())
            except:
                chromecast_control(pure_data) 
            return True
        if skill=='app_radio_play':
            vlcplayer.stop_vlc()
            for item in kw[skill]:
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())
            radio(str(pure_data).lower())
            if GPIOcontrol:
                ctr_led('off')
            return False
        if skill == 'app_translate_language':
            self.conversation_stream.stop_playback()
            continue_conversation = False
            try:    
                requests.get(url,thongdich)
            except:
                requests.get(url,'interprer')
            return False
        if skill=='app_read_note':
            say_save('Chuẩn bị ghi chép')
            import json, time
            from fuzzywuzzy import fuzz
            filename = '{}/ViPi/src/.note.json'.format(USER_PATH)
            for item in kw[skill]:
                pure_data = ' '.join(pure_data.lower().replace(str(item).lower(),"").split())
            with open(filename, 'r') as f:
                data = json.load(f)
                #time.sleep(.25)
            vlcplayer.stop_vlc()
            compare_ratio = [fuzz.ratio(pure_data,people['ten']) for people in data['names']]
            sinh_nhat = [people['sinh_nhat'] for people in data['names']]
            if max(compare_ratio) > 90:
                index=compare_ratio.index(max(compare_ratio))
                ngay_sinh=sinh_nhat[index]
                say_save('sinh nhật của ' + pure_data + ' vào ngày ' + ngay_sinh)
            else:
                say_save('Chưa có thông tin, bạn có muốn bổ sung thêm')
                answer=re_ask()
                if ("có" or "được") in answer:
                    with open (filename,'r') as json_file:
                        data = json.load(json_file)
                    time.sleep(1)
                    ten=pure_data
                    say_save('Đọc ngày tháng năm sinh')
                    time.sleep(1)
                    sinh_nhat=re_ask()
                    new_person = {"ten":ten,"sinh_nhat":sinh_nhat}
                    data['names'].append(new_person)
                    with open  (filename,"w") as f:
                        json.dump(data,f,ensure_ascii=False,indent=4)
                        time.sleep(1)
                    say_save('Đã thực hiện xong việc thêm dữ liệu')
                    return self.back()
                else:
                    say_save('Tạm biệt')
                    return self.back()           

    def ctr_med(self,skill,usrcmd):
        if skill=='med_stop_music':
            vlcplayer.stop_vlc()
            return False
        if skill=='med_pause_player':
            if vlcplayer.is_vlc_playing():
                if skill=='med_pause_player':
                    vlcplayer.pause_vlc()
                if checkvlcpaused():
                    if skill=='med_pause_player':
                        vlcplayer.play_vlc()
                    if vlcplayer.is_vlc_playing()==False and checkvlcpaused()==False:
                        say("Đang không phát nhạc")
            return self.back()
        if skill=='med_next_player':
            ctr_led('speaking')
            if vlcplayer.is_vlc_playing() or checkvlcpaused()==True:
                vlcplayer.stop_vlc()
                vlcplayer.change_media_next()
            return False
        if skill=='med_previous_player':
            ctr_led('speaking')
            if vlcplayer.is_vlc_playing() or checkvlcpaused()==True:
                vlcplayer.stop_vlc()
                vlcplayer.change_media_previous()
            return False
        if skill=='med_volume_up':
            ctr_led('speaking')
            try:
                os.system("amixer set Master 5+ >> /dev/null")
            except:
                os.system("amixer -q -D pulse set Master 5+ unmute >> /dev/null")
                pass
            try:
                os.system("amixer set Speaker 5+ >> /dev/null")
            except:
                os.system("amixer set Headphone 5+ >> /dev/null")
                pass
            return self.back()
        if skill=='med_volume_down':
            ctr_led('speaking')
            try:
                os.system("amixer set Master 5- >> /dev/null")
            except:
                os.system("amixer -q -D pulse set Master 5- unmute >> /dev/null")
                pass
            try:
                os.system("amixer set Speaker 5- >> /dev/null")
            except:
                os.system("amixer set Headphone 5- >> /dev/null")
                pass
            return self.back()            
    def ctr_sma(self,skill,action, types, pure_data):
        if (skill[:5]=='sma_o' and (configuration['Home_Assistant']['control']=='Enabled')) and not (skill=='sma_on_all' or skill=='sma_off_all'):
            hass.command_single(action,types,pure_data)
            time.sleep(3)
            return self.back()
        if (skill=='sma_on_all' or skill=='sma_off_all') and (configuration['Home_Assistant']['control']=='Enabled'):
            hass.command_all(action,types,pure_data)
            time.sleep(3)
            return self.back()
        if ('status' in skill) and (configuration['Home_Assistant']['control']=='Enabled'):
            hass.check_state(action,types,pure_data)
            time.sleep(3)
            return self.back()
    def back(self):
        if GPIOcontrol:
            ctr_led('off')

    def data_processing(self,data):
        import fuzzywuzzy
        from fuzzywuzzy import fuzz
        match_key,compare_ratio = [],[]
        for item in cw:
            data = ' '.join(data.lower().replace(str(item).lower(),'').split())
        for key,value in kw.items():
            for item in value:
                match_key.append(key)
                compare_ratio.append(fuzz.partial_ratio(item,data))
        for item in allcmd:
            data = ' '.join(data.lower().replace(str(item).lower(),'').split())
        if max(compare_ratio) > 90:
            index=compare_ratio.index(max(compare_ratio))
            skill = match_key[index]
            return skill, data 
        else:
            return None

    def assist(self):
        continue_conversation = False        
        device_actions_futures = []
        try:
            os.remove(hotword)
        except:
            pass
        if GPIOcontrol:
                ctr_led('listening')
        subprocess.Popen(["aplay", "{}/sample-audio-files/Fb.wav".format(ROOT_PATH)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        self.conversation_stream.start_recording()
        if vlcplayer.is_vlc_playing():
            if os.path.isfile("{}/.mediavolume.json".format(USER_PATH)):
                try:
                    with open('{}/.mediavolume.json'.format(USER_PATH), 'r') as vol:
                        volume = json.load(vol)
                    vlcplayer.set_vlc_volume(15)
                except json.decoder.JSONDecodeError:
                    currentvolume=vlcplayer.get_vlc_volume()
                    print(currentvolume)
                    with open('{}/.mediavolume.json'.format(USER_PATH), 'w') as vol:
                       json.dump(currentvolume, vol)
                    vlcplayer.set_vlc_volume(20)
            else:
                currentvolume=vlcplayer.get_vlc_volume()
                print(currentvolume)
                with open('{}/.mediavolume.json'.format(USER_PATH), 'w') as vol:
                   json.dump(currentvolume, vol)
                vlcplayer.set_vlc_volume(20)
        def iter_log_assist_requests():
            for c in self.gen_assist_requests():
                assistant_helpers.log_assist_request_without_audio(c)
                yield c

        for resp in self.assistant.Assist(iter_log_assist_requests(),
                                          self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            if resp.event_type == END_OF_UTTERANCE:
                self.conversation_stream.stop_recording()
            if resp.speech_results:
                for r in resp.speech_results:            
                    usercommand=str(r)
                if "stability: 1.0" in usercommand.lower():
                    usrcmd=str(' '.join(r.transcript for r in resp.speech_results)).lower()
                    print(colored('[ViPi_0.2] + [DATA] '+usrcmd,'green'))
#                    if configuration['Wakewords']['Ok_Google']=='Enabled':
#                        os.remove("okgoogle.detect")
                    if GPIOcontrol:
                        ctr_led('think')
                    custom_command=self.data_processing(usrcmd)
                    if custom_command is not None:
                        skill,pure_data =  self.data_processing(usrcmd)
                        pre_skill,action,types = skill.split('_')
                        more_data=''   
                        if 'app' == pre_skill:
                            self.conversation_stream.stop_playback()
                            self.ctr_app(skill,pure_data)
                            return continue_conversation
                        if 'med' == pre_skill:
                            if GPIOcontrol:
                                ctr_led('think')
                            self.conversation_stream.stop_playback()
                            self.ctr_med(skill,pure_data)
                            return continue_conversation
                        if ('sma' == pre_skill) and (configuration['Home_Assistant']['control']=='Enabled'):
                            if GPIOcontrol:
                                ctr_led('think')
                            self.conversation_stream.stop_playback()
                            self.ctr_sma(skill,action,types,pure_data)
                            return continue_conversation                            
                        if configuration['Conversation']['Conversation_Control']=='Enabled':
                            for i in range(1,numques+1):
                                try:
                                    if str(configuration['Conversation']['question'][i][0]).lower() in str(usrcmd).lower():
                                        selectedans=random.sample(configuration['Conversation']['answer'][i],1)
                                        say(selectedans[0])
                                        return self.is_new_conversation
                                except Keyerror:
                                    say('Please check if the number of questions matches the number of answers')
                            if configuration['Raspberrypi_GPIO_Control']['GPIO_Control']=='Enabled':
                                if (custom_action_keyword['Keywords']['Pi_GPIO_control'][0]).lower() in str(usrcmd).lower():
                                    Action(str(usrcmd).lower())
                                    return self.is_new_conversation
                    else:
                        answer = kb(usrcmd)
                        if answer is not None:
                            self.conversation_stream.stop_playback()
                            say(answer)
                            return continue_conversation
                        else:
                            if GPIOcontrol:
                                ctr_led('speaking')
                            continue
            elif len(resp.audio_out.audio_data) > 0 and usrcmd !='thông dịch':
                if not self.conversation_stream.playing:
                    self.conversation_stream.stop_recording()
                    self.conversation_stream.start_playback()
                self.conversation_stream.write(resp.audio_out.audio_data)
            if resp.screen_out.data:
                html_response = resp.screen_out.data            
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                self.conversation_state = conversation_state
            if resp.dialog_state_out.supplemental_display_text:
                text_response = resp.dialog_state_out.supplemental_display_text                
            if resp.dialog_state_out.volume_percentage != 0:
                volume_percentage = resp.dialog_state_out.volume_percentage
                self.conversation_stream.volume_percentage = volume_percentage
            if resp.dialog_state_out.microphone_mode == DIALOG_FOLLOW_ON:
                continue_conversation = True
                if GPIOcontrol:
                    ctr_led('listening')
                logging.info('Expecting follow-on query from user.')
            elif resp.dialog_state_out.microphone_mode == CLOSE_MICROPHONE:
                if GPIOcontrol:
                    ctr_led('off')
                if vlcplayer.is_vlc_playing():
                    with open('{}/.mediavolume.json'.format(USER_PATH), 'r') as vol:
                        oldvolume= json.load(vol)
                    vlcplayer.set_vlc_volume(int(oldvolume))
                continue_conversation = configuration['continue_conversation'] 
            if resp.device_action.device_request_json:
                device_request = json.loads(
                    resp.device_action.device_request_json
                )
                fs = self.device_handler(device_request)
                if fs:
                    device_actions_futures.extend(fs)
            if self.display and resp.screen_out.data:
                system_browser = browser_helpers.system_browser
                system_browser.display(resp.screen_out.data)
        if len(device_actions_futures):
            concurrent.futures.wait(device_actions_futures)
        print(colored('[ViPi_0.2] + [Finish action: Gass] ','yellow'))
        self.conversation_stream.stop_playback()
        if GPIOcontrol:
            ctr_led('off')
        if vlcplayer.is_vlc_playing():
            with open('{}/.mediavolume.json'.format(USER_PATH), 'r') as vol:
                oldvolume= json.load(vol)
            vlcplayer.set_vlc_volume(int(oldvolume))
        return continue_conversation
    def gen_assist_requests(self):
        config = embedded_assistant_pb2.AssistConfig(
            audio_in_config=embedded_assistant_pb2.AudioInConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
            ),
            audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
                volume_percentage=self.conversation_stream.volume_percentage,
            ),
            dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                language_code=self.language_code,
                conversation_state=self.conversation_state,
                is_new_conversation=False,
            ),
            device_config=embedded_assistant_pb2.DeviceConfig(
                device_id=self.device_id,
                device_model_id=self.device_model_id,
            )
        )
        if self.display:
            config.screen_out_config.screen_mode = PLAYING
        self.is_new_conversation = False
        yield embedded_assistant_pb2.AssistRequest(config=config)
        for data in self.conversation_stream:
            yield embedded_assistant_pb2.AssistRequest(audio_in=data)

def main():
    if GPIOcontrol:
        ctr_led('wakeup')
    if gender=='Male' and configuration['Startup_voice'] == 'Enabled':
        subprocess.Popen(["aplay", "{}/sample-audio-files/Startup-Male.wav".format(ROOT_PATH)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if gender=='Female' and configuration['Startup_voice'] == 'Enabled':
        subprocess.Popen(["aplay", "{}/sample-audio-files/Startup-Female.wav".format(ROOT_PATH)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    language_code,display,device_id, device_model_id,project_id    = 'en-US', True, 'Loa-ViPi', configuration['Google_Assistant']['device_model_id'], configuration['Google_Assistant']['project_id']
    device_config=os.path.join(os.path.expanduser('~/.config'),'googlesamples-assistant','device_config_library.json')
    if not device_id or not device_model_id:
        try:
            with open(device_config) as f:
                device = json.load(f)
                device_id = device['id']
                device_model_id = device['model_id']
                logging.info("Using device model %s and device id %s",
                             device_model_id,
                             device_id)
        except Exception as e:
            logging.warning('Device config not found: %s' % e)
            logging.info('Registering device')
            if not device_model_id:
                logging.error('Option --device-model-id required '
                              'when registering a device instance.')
                sys.exit(-1)
            if not project_id:
                logging.error('Option --project-id required '
                              'when registering a device instance.')
                sys.exit(-1)
            device_base_url = (
                'https://%s/v1alpha2/projects/%s/devices' % (api_endpoint,
                                                             project_id)
            )
            device_id = str(uuid.uuid1())
            payload = {
                'id': device_id,
                'model_id': device_model_id,
                'client_type': 'SDK_SERVICE'
            }
            session = google.auth.transport.requests.AuthorizedSession(
                credentials
            )
            r = session.post(device_base_url, data=json.dumps(payload))
            if r.status_code != 200:
                logging.error('Failed to register device: %s', r.text)
                sys.exit(-1)
            logging.info('Device registered: %s', device_id)
            pathlib.Path(os.path.dirname(device_config)).mkdir(exist_ok=True)
            with open(device_config, 'w') as f:
                json.dump(payload, f)

    device_handler = device_helpers.DeviceRequestHandler(device_id)
    with GoogleAssistant(language_code, device_model_id, device_id,
                         conversation_stream, display,
                         grpc_channel, grpc_deadline,device_handler) as assistant:
        def detected():
            continue_conversation=assistant.assist()
            if continue_conversation:
                print('Continuing conversation')
                time.sleep(1)
                assistant.assist()
        signal.signal(signal.SIGINT, signal_handler)
        _sensitivities = [configuration['Wakewords']['sensitivities']]*wakeword_length
        _library_path = pvporcupine.LIBRARY_PATH
        _model_path = pvporcupine.MODEL_PATH
        _keyword_paths = picovoice_models
        _input_device_index = None

        def picovoice_run():
            keywords = list()
            for x in _keyword_paths:
                keywords.append(os.path.basename(x).replace('.ppn', '').split('_')[0])
            porcupine = None
            pa = None
            audio_stream = None
            try:
                porcupine = pvporcupine.create(
                    library_path=_library_path,
                    model_path=_model_path,
                    keyword_paths=_keyword_paths,
                    sensitivities=_sensitivities,access_key='d+SMP+hQksg/UKalL2q+PetoJbmlGAVupaXkwonKPvRezShlKAh+WA==')
                pa = pyaudio.PyAudio()
                audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length,
                    input_device_index=_input_device_index)
                while True:
                    pcm = audio_stream.read(porcupine.frame_length,exception_on_overflow = False)
                    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                    result = porcupine.process(pcm)
                    if result >= 0:
                        detected()
            except KeyboardInterrupt:
                print('Stopping ...')
            finally:
                if porcupine is not None:
                    porcupine.delete()
                if audio_stream is not None:
                    audio_stream.close()
                if pa is not None:
                    pa.terminate()
        wait_for_user_trigger = True
        while 1:
#            print (os.path.exists(hotword))
#            if os.path.exists(hotword) == True:
#                detected()        
            if wait_for_user_trigger:
                if custom_wakeword:
                    if configuration['Wakewords']['Wakeword_Engine']=='Picovoice':
                        picovoice_run()
                    else:
                        button_state=GPIO.input(pushbuttontrigger)
                if button_state==True:
                    continue
                if continue_conversation == True:
                    continue
                else:
                    pass
            continue_conversation = assistant.assist()
            wait_for_user_trigger = not continue_conversation

def re_ask():
    tic = time.perf_counter()
    record = sr.Recognizer()
    required=-1
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "capture" in name:
            required= index
    with noalsaerr() as n,sr.Microphone(device_index=required) as source:
        sr.SAMPLE_RATE = 16000
        record.adjust_for_ambient_noise(source)
        if GPIOcontrol:
            ctr_led('wakeup')        
        subprocess.Popen(["aplay", "{}/sample-audio-files/Fb.wav".format(ROOT_PATH)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            if GPIOcontrol:
                ctr_led('listening')    
            audio = record.listen(source, timeout=3, phrase_time_limit=3)
        except Exception as e:
#            print(e)
            pass
    try:
        data = record.recognize_google(audio,language = "vi-VN")
    except:
        data =  record.recognize_wit(audio, key=WIT_AI_KEY)
#    data =  record.recognize_wit(audio, key=WIT_AI_KEY)
#    toc = time.perf_counter()
#    print("STT: " + data)
#    print(f"STT take {toc - tic:0.4f} seconds")  
    return data

if __name__ == '__main__':
    import time
    main()