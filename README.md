## Test code ViPi:
Cách cài đặt và cấu hình các bạn làm theo hướng dẫn bên nhánh main

##IMG cho Raspi0 armv6
https://drive.google.com/file/d/1ieaSzrc-2UyGz9aGLrRTsiGR50K83pEh/view?usp=sharing

Để chạy cho Raspi 02W, Raspi 3 trở lên chạy thêm các lệnh sau:

pip3 uninstall google-assistant-library
pip3 install google-assistant-library==1.1.0

````
Kiểm tra nếu không start được thành công thì có thể chạy lệnh sau:
```
sudo pkill -9 supervisord
```
Rồi start lại supervisor. User và password web là user/123
