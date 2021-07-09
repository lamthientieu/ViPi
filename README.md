## Dự án bot [ViPi] là dự án mod lại từ các dự án sau:
https://github.com/googlesamples/assistant-sdk-python/tree/master/google-assistant-sdk
https://github.com/shivasiddharth/GassistPi

Với sự đóng góp các thành viên mù code và tester đam mê phá nhà, nghèo vì độ loa sẽ update trong contributer sau :D

1 số bạn có nhã ý donate cho nhóm.mình xin ghi nhận tấm lòng.cũng là 1 phần các bạn đã kích lệ cho anh em tìm tòi và nghiên cứu thêm các thứ mới.
Nhất là phần cứng all in all anh em đang ấp ủ.

Momo: 0935300314 lâm.
Xin ghi rõ nội dung ủng hộ nhóm vipi.
 Tất cả thông tin donate đều cập nhập lên git.
## DONATE: 
Danh sách các bạn đã ủng hộ.cập nhập đến 03.07.2021.

Dù ít hay nhiều chúng tôi đều trân trọng tấm lòng của các bạn như nhau.

1 - Khuê: 50.000đ

2 - Tiến: 500.000đ

3 - T.Quang: 100.000đ

4 - M.Quang: 200.000đ

5 - T.Nguyên: 2.000.000đ

6 - D.Hai : 50.000đ

7 - T.An: 100.000đ

8 - T.Đạt: 100.000đ

9 - V.Dũng: 100.000đ

Tc: 3.200.000đ

Vì anh em chúng tôi làm nhóm nên tất cả đều công khai minh bạch.😍😍😍😍😍

Donate chúng tôi ko hề bắt buộc.

Kinh phí này nhóm sẽ dùng cho việc phát triển phần cứng all in one.

xin chân thành cảm ơn.
## PHÁT TRIỂN CODE :
Người mò mẫm đầu tiên [longhd2](https://github.com/longhd2)

Coder 3h Youtube [canghp128](https://github.com/canghp128)

Coder ẩn dật [HungDoManh](https://github.com/HungDoManh)

Copy & paste [thangnd85](https://github.com/thangnd85)

Phá Hoại Bày Vẽ [lamthientieu](https://github.com/lamthientieu)

Chuyên gia âm thanh, độ chế tay nghề cao [Đại Ca SƠN - PHÚ QUỐC]

Sharktank [tuanto90](https://github.com/tuanto90)

Tester nghiệp dư [tienhuansk](https://github.com/tienhuansk)


Đây là dự án miễn phí, phục vụ cá nhân khi rảnh rỗi, không phải dev chuyên nghiệp. 

Anh em muốn tham gia vào đội coder thì cứ inbox [Nhóm test code](https://t.me/vipi_code)

## 1.Chuẩn bị:
Thẻ nhớ, file image tải bên dưới:
Imgage gốc:

http://www.cs.tohoku-gakuin.ac.jp/pub/Linux/RaspBerryPi/

Hoặc bản có sẵn môi trường và wifi hotspot

https://vipiteam.page.link/img

Flash vào thẻ nhớ bằng Echter hoặc Raspberry Pi Imager

## 1.1 Kết nối wifi và ssh:

1, Với image gốc: Tạo file ssh (không có đuôi gì cả và không nội dung) 

Tạo tiếp file wpa_suplicant.conf với nội dung sau:
```
country=vn
update_config=1
ctrl_interface=/var/run/wpa_supplicant

network={
 scan_ssid=1
 ssid="tên_wifi"
 psk="pass_wifi"
}
```
Rồi chép cả 2 vào partition boot trong thẻ nhớ. Gắn thẻ vào Pi rồi bật nguồn.

2. Trường hợp flash image có sẵn môi trường, sau khi flash xong, gắn vào Pi và bật nguồn, sẽ xuất hiện wifi tên là ViPi

Kết nối với wifi đó để tiến hành nối vào mạng.

3. Sau khi nối mạng, có thể dùng các phần mềm trên điện thoại như Fing để quét IP, 

hoặc dùng IP scanner free trên PC Hay vào modem/router để xem IP của pi. 


File json google Actions:

Tạo json theo hướng dẫn tại đây, tải về đổi tên tùy ý, chút sẽ sử dụng.

https://www.youtube.com/watch?v=ROQ5K4om2Fo

Nhớ thêm email của mình vào mục Test user:

Nếu cài đặt từ img gốc, tiến hành từ bước 2:

Nếu cài từ img sẵn có môi trường, chuyển qua bước 7.

### 2.Update OS & cài đặt git:

Dùng ssh để đăng nhập vào pi với username và pass mặc định

Sử dụng puTTY hoặc Terminal để SSH vào Pi với địa chỉ đã scan bên trên, hoặc dùng hostname raspberrypi.local

Dùng WinSCP để quản lí file trong Pi

Copy json ở bước 1 vào /home/pi (là cái folder mặc định khi vào winscp)

### 3. Cài đặt Mic & Loa nếu sử dụng Mic HAT:
OS trước tháng 8.2020
```sh
cd /home/${USER}/
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh --compat-kernel
sudo reboot
```
OS sau tháng 8.2020
```sh
cd /home/${USER}/
git clone https://github.com/HinTak/seeed-voicecard
cd seeed-voicecard
sudo ./install.sh
sudo reboot now
```
Sau khi khởi động lại, đăng nhập lại vào console

Kiểm tra xem có âm thanh ở loa hay không:
```sh
speaker-test
```
Lệnh Thống kê ID của Mic và Loa
```sh
arecord -l
aplay -l
```

##4. Cài portaudio:
 
Tải về từ git:
```sh
git clone -b alsapatch https://github.com/gglockner/portaudio
cd portaudio
./configure && make
sudo make install
sudo ldconfig
```

Nếu vẫn còn xuất hiện lỗi cài bổ sung các thư viện bổ sung của pulseaudio
```sh
sudo apt-get install pulseaudio -y && sudo apt-get remove pulseaudio -y
```


### 4.1. Disable onboard sound nếu không dùng:
```sh
sudo nano /etc/modprobe.d/snd-blacklist.conf
```
Thêm dòng này vào:
```
blacklist snd_bcm2835
```
Ctr + X, Y Enter

## 5. Clone source về  Pi và cài đặt


```sh
cd /home/${USER}/
git clone https://github.com/lamthientieu/ViPi.git
sudo chmod +x ./ViPi/scripts/installer.sh && sudo ./ViPi/scripts/installer.sh
```
Nhập đường dẫn json:  /home/pi/ten_file.json (đổi tên cho đúng nhé)

Sau khi cài đặt xong có thể sẽ bị rớt mạng wifi, khởi động lại pi hoặc kiểm tra wifi trên điện thoại (hay máy tính), 

sẽ có mạng wifi mới tên là ViPi thì kết nối vào đó, rồi lựa chọn mạng wifi nhà mình, nhập mật khẩu để kết nối. 

Ngay sau khi kết nối thành công thì có thể dùng các công cụ để tìm IP để ssh, winscp để chỉnh sửa file tùy ý.

Team sẽ cố gắng tạo ra phần cài đặt bằng trình duyết cho gọn nhẹ. 

### 5.1: Update new source:
Cách 1: 
```
cd /home/${USER}/
cd ViPi
git pull
```
Cách 2:
```
cd /home/${USER}/
rm -rf ViPi
git clone https://github.com/lamthientieu/ViPi.git
```

## 6. Cấu hình led và các cài đặt khác trong file ViPi/src/config.yaml
```sh
  #  Set type mic to:
  # 1. 'GEN'   ---> USB-MIC-JACK
  # 2. 'GEN'   ---> USB-MIC-HDMI
  # 3. 'AIY'   ---> AIY-HAT
  # 4. 'R2M'   ---> Respeaker-2-Mic
  # 5. 'R4M'   ---> Respeaker-4-Mic
  # 6. 'RUM'   ---> Respeaker-Usb-Mic
  # 7. 'NEO'   ---> NeoPixel
  # 8. 'GOO'   ---> Google
  # 8. 'ALE'   ---> Alexa
  Bật tắt Home_Assistant:
  .......
```

## 7.Chạy lần đầu:
Chạy lần đầu với raspi:
```sh
source ~/env/bin/activate
google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype \
          --scope https://www.googleapis.com/auth/gcm \
          --save --headless --client-secrets /home/pi/ten_file.json
```
Tiếp tục:
```sh
env/bin/python -u ./ViPi/src/start.py --project-id 'XXX' --device-model-id 'XXX'
```
Thay bằng project-id và device-model-id của bạn trong file config.


## 8.Thiết lập chạy tự động:
a. Chạy tự động với supervisor:
```sh
sudo nano /etc/supervisor/conf.d/ViPi.conf
```
Cửa sổ nano hiện lên, paste dòng sau
```sh
[program:ViPi]
directory=/home/pi
command=/bin/bash -c 'env/bin/python -u ./ViPi/src/start.py'
numprocs=1
autostart=true
autorestart=true
user=pi
```
Chạy lệnh sau để khởi động chạy tự động:
```sh
sudo supervisorctl update
```
Bật web ínterface để xem log cho nhanh
```sh
sudo nano /etc/supervisor/supervisord.conf
```
Sau đó paste dòng này vào:
```sh
[inet_http_server]
port=*:9001
username=user
password=pass
```
Ctrn + X, Y, enter để save. Xong reboot lại Pi, có thể mở web lên nhập http://ip_của_pi:9001 nhập username và pass ở trên để xem log:

```sh
sudo reboot
```

### 8.1.Tắt chạy tự động trong phiên làm việc:

```sh
sudo supervisorctl stop ViPi
```
### 8.2.Xóa chạy tự động:
```sh
sudo rm -rf /etc/supervisor/conf.d/ViPi.conf
```
### 9. (Tùy chọn, chưa phát triển) Tạo STT tại đây:

-  Đăng ký Acc FPT AI tại: https://fpt.ai/

-  Đăng ký Acc Viettel AI tại: https://viettelgroup.ai/en

-  Đăng ký Acc Zalo AI tại: https://zalo.ai/user-profile



###. Note!
fix: NotImplementedError: mixer module not available (ImportError: libSDL2_mixer-2.0.so.0: cannot open shared object file: No such file or directory)
```sh
sudo dpkg --configure -a
#sudo apt-get install libsdl-ttf2.0-0
#sudo apt-get install libsdl2-mixer-2.0-0
sudo apt-get install python3-sdl2 -y
sudo apt install libportaudio2;
```
Đưa lệnh vào env với raspi:
```sh
source env/bin/activate
```
Đưa lệnh vào env với bananapi:
```sh
source ViPi/env/bin/activate
```
Cài thêm app:
```sh
pip install pygame
```
Hạ phiên bản VLC:
```sh
source env/bin/activate
pip install python-vlc==3.0.11115
```

### Khai báo khi sử dụng Mic Usb:
Lệnh Thống kê ID của Mic USB và Loa
```sh
arecord -l
aplay -l
```
Chạy lệnh sau
```sh
sudo nano /home/pi/.asoundrc
```
Cửa sổ nano hiện lên, paste dòng sau, thay thế ID mic, loa phù hợp

```sh
pcm.dsnooper {
    type dsnoop
    ipc_key 816357492
    ipc_key_add_uid 0
    ipc_perm 0666
    slave {
        pcm "hw:1,0"
        channels 1
    }
}

pcm.!default {
        type asym
        playback.pcm {
                type plug
                slave.pcm "hw:0,0"
        }
        capture.pcm {
                type plug
                slave.pcm "dsnooper"
        }
}

```
Coppy cấu hình âm thanh vào etc:
```sh
sudo cp /home/pi/.asoundrc /etc/asound.conf
```
Đưa Account đang dùng (Ví dụ pi) vào group root:
```sh
sudo usermod -aG root pi
```

Fix lỗi không nhận được âm thanh:
Step 1: rm ~/.asoundrc && sudo rm /etc/asound.conf
Step 2: Reinstall driver
Step 3: Reboot

#### Một số khẩu lệnh:

```
Tăng/giảm âm thanh: tăng thêm/giảm bớt âm lượng 0-100 
Tăng giảm âm thanh: đặt/thay đổi âm lượng lớn nhất/ tối thiểu
Tăng giảm âm thanh: đặt/thay đổi âm lượng 0-100
Tắt nhạc: tắt nhạc
Chuyển bài chỉ áp dụng khi phát tự động: bài tiếp theo/ bài hát trước
Phát một bài hát: Phát bài, phát nhạc+()
Phát nhiều bài bài hát khi dùng start.py: Phát tự động + (), phát danh sách+()
Phát nhiều bài bài hát khi dùng start.py: Phát + ()
phát radio:   radio + (tên đài) ví dụ Radio bà rịa vũng tàu
Lịch âm: Lịch âm hoặc âm lịch + (hôm nay, qua , mai ,mốt)
Thay đổi âm lượng giọng nói: âm lượng tăng/ âm lượng giảm ( tự động +/-5% đối với pi zero, +/-10% đối với pi3 trở lên)
Nghe báo nói: Báo nói + (thời sự, tin mới, thể thao, cười)
Điều khiển Home_Assistant: Bật tắt thiết bị, kiểm tra trạng thái, kích hoạt kịch bản (script) hoặc tự động hóa (automation)

```
https://installvirtual.com/install-python-3-7-on-raspberry-pi/

## Sửa lỗi không lưu cài đặt âm thanh khi khởi động với mic 2HAT

Xóa bỏ service cũ:
```
sudo rm /lib/systemd/system/alsa-restore.service
```
Tạo service mới:

```
sudo nano /lib/systemd/system/alsa-restore.service
```
Dán nội dụng sau vào:

```

[Unit]
Description=Save/Restore Sound Card State
Documentation=man:alsactl(1)
ConditionPathExists=!/etc/alsa/state-daemon.conf
ConditionPathExistsGlob=/dev/snd/control*
After=alsa-state.service

[Service]
Type=oneshot
RemainAfterExit=true
ExecStart=
ExecStart=-/usr/sbin/alsactl -E HOME=/run/alsa -f /etc/voicecard/wm8960_asound.state restore

ExecStop=
ExecStop=-/usr/sbin/alsactl -E HOME=/run/alsa -f /etc/voicecard/wm8960_asound.state store
```

Ctr + X,Y, enter
Sau đó 
```
sudo systemctl daemon-reload
```
Khởi động lại  

### Chuyển json vào root 

Password: điền pass.không biết pass thì tạo pass mới.

```sh
sudo passwd root
sudo su
cd ~
cd .config
mkdir google-oauthlib-tool
sudo cp /home/pi/.config/google-oauthlib-tool/credentials.json /root/.config/google-oauthlib-tool/credentials.json
```
## config Nếu dùng led W2812
```sh
sudo usermod -aG spi pi
sudo nano /boot/config.txt
```
#Add thêm 2 dòng sau
```sh
core_freq=250
spidev.bufsiz=32768
```
Reboot lại thiết bị


### Fix pluseaudio
```sh   
cd /home/${USER}/       
git clone https://github.com/shivasiddharth/PulseAudio-System-Wide       
cd ./PulseAudio-System-Wide/      
sudo cp ./pulseaudio.service /etc/systemd/system/pulseaudio.service    
systemctl --system enable pulseaudio.service       
systemctl --system start pulseaudio.service       
sudo cp ./client.conf /etc/pulse/client.conf        
sudo sed -i '/^pulse-access:/ s/$/root,pi/' /etc/group    
```
