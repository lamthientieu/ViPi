## Hướng dẫn test code nhánh Beta:

## Tải IMG cho raspi tại đây, IMG mặc định cho Raspberry Pi Zero:
```sh
https://drive.google.com/file/d/1ieaSzrc-2UyGz9aGLrRTsiGR50K83pEh/view?usp=sharing
```
Giải nén và dùng Phần mềm win32 disk imager để ghi ra thẻ:
![image](https://user-images.githubusercontent.com/57694952/177024364-5aa1771e-fccd-4340-8a68-9a0ffa8490a2.png)

Gắn thẻ vào raspi đợi 1-2 phút, kết nối với mạng WiFi được raspi phát ra với tên "ViPi"
![image](https://user-images.githubusercontent.com/57694952/177024308-4e08fbea-c3b3-49f8-8f2a-de8f6910acef.png)

Sau đó kết nối với mạng WIFI đang sử dụng
![image](https://user-images.githubusercontent.com/57694952/177024665-f17a300c-862f-4b39-96dc-550163f5449b.png)

Dùng PM WinSCP, và putty để ssh vào pi với user/pass mặc định: pi/raspberry
![image](https://user-images.githubusercontent.com/57694952/177024726-fd9d07a8-c7a9-4cab-bcc7-031a1bd87394.png)

![image](https://user-images.githubusercontent.com/57694952/177024745-1ff85019-6efe-42f9-a27c-b8c4f125ef71.png)

Chạy thêm lệnh sau:
```
pip3 install pvporcupine==1.9.5
```


Để sử dụng cho Raspberry Pi Zero 2 W/ Pi 3/ 3B+ trở lên cài thêm các lệnh sau
```
pip3 uninstall google-assistant-library
pip3 install google-assistant-library==1.1.0
```

Đăng ký tài khoản json theo hướng dẫn" chờ cập nhật sau chưa tìm ra link"


Tải code ở link: https://github.com/lamthientieu/ViPi/tree/beta
Giải nén và chép vào thư mục /home/pi

