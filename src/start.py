import platform, os, yaml, json
ROOT_PATH = os.path.realpath(os.path.join(__file__, '..', '..'))
USER_PATH = os.path.realpath(os.path.join(__file__, '..', '..','..'))
with open('{}/src/config.yaml'.format(ROOT_PATH),'r', encoding='utf8') as conf:
    configuration = yaml.safe_load(conf)

a=platform.platform()
print("\ncheck system: ",a)
try:      
    with open('{}/.config/google-oauthlib-tool/credentials.json'.format(USER_PATH), 'r') as registers:
        register = json.load(registers)

    with open('{}/.config/google-oauthlib-tool/credentials.json'.format(USER_PATH), 'r') as registers:
        register = json.load(registers)
    if configuration['Wakewords']['Ok_Google']=='Disabled' and 'armv7l' not in platform.platform():
        print ('\nimport main6')
        import main6
        main6.Myassistant().main()
    if configuration['Wakewords']['Ok_Google']=='Disabled' and 'armv7l' in platform.platform():
        print ('\nimport main7')
        import main7
        main7.Myassistant().main()
    if 'armv7l' in platform.platform() and configuration['Wakewords']['Ok_Google']=='Enabled':
        import main
        print ('\nimport main')
        main.Myassistant().main()
    else:
        say_save('gặp lỗi không khởi động được, vui lòng kiểm tra cài đặt')
        pass
except:  
    print('Bạn chưa đăng ký tài khoản với google, thực hiện đăng ký tài khoản')
    from new_oauth import *
    if __name__ == '__main__':
       app.run(host='0.0.0.0',port=5002)
    pass
