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

Để đăng ký google assistant vào địa chỉ IP:5002 thực hiện như hình:

![image](https://user-images.githubusercontent.com/57694952/177025093-0bd11d9a-9b3c-4fdc-b26f-8ce7a375a804.png)

sau đó
Tải code ở link: https://github.com/lamthientieu/ViPi/tree/beta
Giải nén và chép vào thư mục /home/pi



Vào địa chỉ IP:5002 chọn config để chỉnh sữa cài đặt, đăng ký tài khoản Zalo ai, mượn số điện thoại zalo bạn bè đăng ký 2-3 key zalo để dử dụng
![image](https://user-images.githubusercontent.com/57694952/177025349-e69adda8-6909-41b9-b0d6-a935c723bb10.png)

## Lưu ý chọn đúng cấu hình đang sử dụng:

1/ Cấu hình homeassistant: tăng độ chuẩn xác bằng cách chỉnh ratio: 100 là đúng tên thiết bị 100% mới điều khiển được

![image](https://user-images.githubusercontent.com/57694952/177025400-ce34e980-afe9-47b8-8cfe-f8a5fe6c8d29.png)

2/ Dán API zalo vào để sử dụng Zalo
![image](https://user-images.githubusercontent.com/57694952/177025492-37121a1c-622a-463a-bc28-67b1cc344e26.png)

3/ Thay đổi cấu hình cho phù hợp với phần cứng
để điều âm lượng hãy hãy kiểm tra card âm thanh đang sử dụng và điền đúng vào (Master/ Heaphone/ hoặc Speaker...)

![image](https://user-images.githubusercontent.com/57694952/177025539-ad868848-4539-4862-a421-33cedaedc00f.png)

Các Gpio được sử dụng trong code, các bạn có thể thay đổi nhưng không phải GPIO nào cũng dùng được:

(Gpio_left:   Bấm 1 lần: Giảm âm lượng,  Bấm 2 lần: Mở bài hát trước
            
 Gpio_right:  Bấm 1 lần: tăng âm lượng, Bấm 2 lần: Next bài hát
             
 Gpio_center: Bấm 1 lần: gọi ViPi, Bấm 2 lần: stop/play)
                

![image](https://user-images.githubusercontent.com/57694952/177025720-53f14834-2068-4210-94b9-17351a679ba3.png)


Khởi động lại pi!


Để sử dụng dashboar vào địa chỉ IP:5002

Để xem log vào địa chỉ IP:9001 với user/pass: user/123



## Để nghe 1 bài hát: Hotword + các key trong "app_music_play"+ bài hát + (chọn nguồn nhạc muốn phát: Youtube, nhạc của tui, Zing, mặc định khi không chọn là nhạc của tui)

VD:         Ok google + hát nhạc + còn thương rau đắng mọc sau hè + trên youtube==> Bot sẽ tìm nhạc trên Youtube)
            Ok google + hát nhạc + còn thương rau đắng mọc sau hè ==> Bot mặc định tìm trên Nhạc của tui, nếu trên nhạc của tui không có bài hát đó thì sẽ chuyển sang tìm trên Youtube)

``` app_music_play:
        - 'phát bài hát'
        - 'phát bài nhạc'
        - 'hát nhạc'
        - 'phát nhạc'
        - 'chơi nhạc'
        - 'hát bài'
        - 'bài hát'
        - 'bài nhạc'
        - 'lên nhạc'
```
 
### Để nghe danh sách nhạc: dùng các key trong " app_music_auto:"
    
    
    
### Các keyword cho dự án, ngoài các keyword chính xác, các bạn có thể hỏi thêm làm gì, là ai, bot có thể làm toán mà không cần câu lệnh chính xác....:    

```
keyword:
    app_cooking_recipe:
        - 'cách nấu món'
    app_my_name:
        - 'bạn tên'
        - 'tên bạn'
        - 'tên mày'
    app_hour_schedule:
        - 'một giờ'
        - 'hai giờ'
        - 'ba giờ'
        - 'bốn giờ'
        - 'năm giờ'
        - 'sáu giờ'
        - 'bẩy giờ'
        - 'tám giờ'
        - 'chín giờ'
        - 'mười một giờ'
        - 'mười hai giờ'
    app_minutue_schedule:
        - 'năm phút'
        - 'mười phút'
        - 'mười năm phút'
        - 'hai mươi năm phút'
        - 'ba mươi phút'
        - 'ba mươi năm phút'
        - 'bốn mươi phút'
        - 'bốn mươi năm phút'
        - 'năm mươi phút'
        - 'năm mươi năm phút'
    app_lunar_calendar:
        - 'ngày âm'
        - 'lịch âm'
        - 'mồng mấy'
        - 'mùng mấy'
        - 'âm lịch hôm nay'
        - 'âm lịch ngày mai'
        - 'âm lịch ngày kia'
    app_read_story:
        # - 'truyện cười'
        - 'kể truyện'
        - 'đọc truyện'
        - 'tìm truyện'
        - 'câu chuyện'
        - 'kể chuyện'
    app_music_play:
        - 'phát bài hát'
        - 'phát bài nhạc'
        - 'hát nhạc'
        - 'phát nhạc'
        - 'chơi nhạc'
        - 'hát bài'
        - 'bài hát'
        - 'bài nhạc'
        - 'lên nhạc'
    app_music_random:
        - 'ca nhạc'
    med_radio_play:
        - 'nghe đài'
        - 'radio'
        - 'đài phát thanh'
    app_music_auto:
        - 'nghe playlist'
        - 'nghe danh sách'
        - 'phát danh sách'
        - 'phát playlist'
        - 'phát album'
        - 'nghe album'
        - 'danh sách'
        - 'list nhạc'
        # - 'abum'
    med_chromecast_play:
        - 'trên loa'
        - 'trên tivi'
    med_custom_weather:
        - 'dự báo thời tiết'
        - 'mưa hay nắng'
        - 'thời tiết'
    # med_news_radio:
        # - 'đọc báo'
        # - 'báo nói'
        # - 'tin mới'
        # - 'tin tức'
    med_read_note:
        - 'sinh nhật của'
        - 'ngày sinh của'
        - 'ngày sinh'
    med_translate_language:
        - 'thông dịch'
        - 'phiên dịch'
        - 'dịch thuật'
        - 'dịch tự động'        
    med_stop_music:
        - 'tắt nhạc'
        - 'dừng nhạc'
        - 'stop music'
        - 'dừng truyện'
    med_next_player:
        - 'tiếp theo'
        - 'kế tiếp'
    med_pause_player:
        - 'tạm dừng'
        - 'phát lại'
    med_continue_player:
        - 'tiếp tục'
    med_previous_player:
        - 'phát lại'
        - 'chơi lại'
    med_volume_ctr:
        - 'tăng âm'
        - 'giảm âm'
        - 'âm lượng' 
        - 'to lên'
        - 'nhỏ lại'
        - 'nhỏ xuống' 
    # med_setup_volume:
        # - 'thiết lập'
        # - 'cài đặt'
    # app_speedtest_net:
        # - 'tốc độ đường truyền'
        # - 'chất lượng đường truyền'
    sma_on_all:
        - 'bật tất cả'
        - 'bật hết'
        - 'bật toàn bộ'
        - 'bật các'
    sma_off_all:
        - 'tắt tất cả'
        - 'tắt hết'
        - 'tắt toàn bộ'
        - 'tắt các'
    sma_on_automation:
        - 'bật tự động'
    sma_off_automation:
        - 'tắt tự động'
        - 'vô hiệu tự động'
    sma_trigger_automation:
        - 'kích hoạt'
    sma_on_script:
        - 'bật kịch bản'
        - 'chạy kịch bản'
    sma_off_script:
        - 'tắt kịch bản'
        - 'dừng kịch bản'
    sma_toggle_script:
        - 'đổi kịch bản'
    sma_on_light:
        - 'mở đèn'
        - 'bật đèn'
    sma_off_light:
        - 'tắt đèn'
        - 'ngắt đèn'
    sma_on_switch:
        - 'bật công tắc'
        - 'mở công tắc'
        - 'bật điện'
    sma_off_switch:
        - 'tắt công tắc'
        - 'ngắt công tắc'
    sma_on_socket:
        - 'bật ổ cắm'
        - 'đóng điện ổ cắm'
        - 'mở điện ổ cắm'
        - 'mở nguồn ổ cắm'
    sma_off_socket:
        - 'tắt ổ cắm'
        - 'ngắt ổ cắm'
        - 'ngắt nguồn ổ cắm'
    sma_open_cover:
        - 'mở rèm'
        - 'kéo rèm lên'
        - 'kéo rèm ra'
    sma_close_cover:
        - 'đóng rèm'
        - 'kéo rèm lại'
    sma_on_fan:
        - 'bật quạt'
        - 'mở quạt'
    sma_off_fan:
        - 'tắt quạt'
    sma_schedule_:
        - 'hẹn giờ'
        - 'đặt giờ'
    sma_input_:
        - 'nhập vào'
        - 'điền vào'
        - 'chọn mục'
        - 'đầu vào'
        - 'mục nhập'
    sma_status_sensor:
        - 'kiểm tra'
        - 'trạng thái'
        - 'đóng hay mởi'
        - 'bật hay tắt'
        - 'kiểm tra'
        - 'hiển thị'
        - 'thông tin'
    sma_status_tracker:
        - 'vị trí'
        - 'ở đâu'
```
