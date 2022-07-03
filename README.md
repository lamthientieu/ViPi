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

Để đăng ký tài vào địa chỉ IP:5002 thực hiện như hình
![image](https://user-images.githubusercontent.com/57694952/177025093-0bd11d9a-9b3c-4fdc-b26f-8ce7a375a804.png)

sau đó
Tải code ở link: https://github.com/lamthientieu/ViPi/tree/beta
Giải nén và chép vào thư mục /home/pi



Vào địa chỉ IP:5002 chọn config để chỉnh sữa cài đặt, đăng ký tài khoản Zalo ai, mượn số điện thoại zalo bạn bè đăng ký 2-3 key zalo để dử dụng
![image](https://user-images.githubusercontent.com/57694952/177025349-e69adda8-6909-41b9-b0d6-a935c723bb10.png)
Lưu ý chọn đúng cấu hình đang sử dụng:

1/ cấu hình homeassistant: tăng độ chuẩn xác bằng cách chỉnh ratio: 100 là đúng tên thiết bị 100% mới điều khiển được

![image](https://user-images.githubusercontent.com/57694952/177025400-ce34e980-afe9-47b8-8cfe-f8a5fe6c8d29.png)

2/ Dán API zalo vào để sử dụng Zalo
![image](https://user-images.githubusercontent.com/57694952/177025492-37121a1c-622a-463a-bc28-67b1cc344e26.png)

3/ Thay đổi cấu hình cho phù hợp với phần cứng
để điều âm lượng hãy hãy kiểm tra card âm thanh đang sử dụng và điền đúng vào (Master/ Heaphone/ hoặc Speaker...)

![image](https://user-images.githubusercontent.com/57694952/177025539-ad868848-4539-4862-a421-33cedaedc00f.png)

Các Gpio được sử dụng trong code
![image](https://user-images.githubusercontent.com/57694952/177025720-53f14834-2068-4210-94b9-17351a679ba3.png)


Khởi động lại pi!


Để sử dụng dashboar vào địa chỉ IP:5002

Để xem log vào địa chỉ IP:9001 với user/pass: user/123
