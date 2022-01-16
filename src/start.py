import platform, os
from actions import configuration
try:
    if configuration['Gpios']['control']=='Enabled' and 'armv7l' not in platform.platform():
        print ('GPIO CONTROL ENABLED & INTERPRER DISABLED')
        import new_start
        new_start.main()
    if 'armv7l' in platform.platform() and configuration['Wakewords']['Ok_Google']=='Enabled':
        import new_main
        new_main.Myassistant().main()
    else:
        print ('GPIO CONTROL DISABLED & INTERPRER ENABLED')
        import old_start
        old_start.main()
except:
    from new_oauth import *
    if __name__ == '__main__':
       app.run(host='0.0.0.0',port=5002)
    pass
