import tango
import json
from tango import Database, DbDevInfo

# --------
# variables
# --------
number_of_fug_ps = 10
tango_class_name = 'FugControl'
fugs_ip_list = ['10.18.88.106',
                '10.18.88.105',
                '10.18.88.108',
                '10.18.88.107',
                '10.18.88.110',
                '10.18.88.109',
                '10.18.88.188',
                '10.18.88.187',
                '10.18.88.41',
                '10.18.88.43',
                ]
instances = [f'{fugs_ip}' for fugs_ip in fugs_ip_list]
domain = 'fsd'
family = 'lv'
member = [f'fug_{ip}' for ip in instances]
# host = '159.93.121.94'
port = 2101

# Creating a database object.
db = Database()
# Creating a device info object.
dev_info = DbDevInfo()
# Setting the class of the device.
dev_info._class = tango_class_name
#
for i in range(number_of_fug_ps):
    dev_info.server = f'{tango_class_name}/{instances[i]}'
    dev_info.name = f'{domain}/{family}/{member[i]}'

    db.add_device(dev_info)
    db.put_device_property(dev_info.name, {'host': instances[i]})
    db.put_device_property(dev_info.name, {'port': port})
