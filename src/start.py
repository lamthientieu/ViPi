import platform, os, yaml
ROOT_PATH = os.path.realpath(os.path.join(__file__, '..', '..'))
with open('{}/src/config.yaml'.format(ROOT_PATH),'r', encoding='utf8') as conf:
    configuration = yaml.safe_load(conf)

a=platform.platform()
print("\ncheck system: ",a)
#print('\n')
if configuration['Wakewords']['Ok_Google']=='Disabled' and 'armv7l' not in platform.platform():
    print ('GPIO CONTROL ENABLED & INTERPRER DISABLED')
    print ('\nimport main_v6')
    import main6
    main6.Myassistant().main()
if configuration['Wakewords']['Ok_Google']=='Disabled' and 'armv7l' in platform.platform():
    print ('GPIO CONTROL ENABLED & INTERPRER DISABLED')
    print ('\nimport main_v7')
    import main7
    main7.Myassistant().main()
if 'armv7l' in platform.platform() and configuration['Wakewords']['Ok_Google']=='Enabled':
    import main
    print ('\nimport main_new')
    main.Myassistant().main()
else:
    print ('\nimport main_v6')
    import main6
    main6.Myassistant().main()