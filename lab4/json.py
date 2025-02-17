import json

file_path = r"C:\Users\Admin\AppData\Roaming\git\labs\lab4\exercises\sample-data.json"
with open (file_path, "r") as file:
    data = json.load (file)


imdata = data["imdata"]


print (f"{'DN':<50}{'DESCRIPTION':<20}{'SPEED':<10}{'MTU'}")
for imdates in imdata:
    print (f'{imdates["l1PhysIf"]["attributes"]["dn"]:<50}{imdates["l1PhysIf"]["attributes"]["descr"]:<20}{imdates["l1PhysIf"]["attributes"]["speed"]:<10}{imdates["l1PhysIf"]["attributes"]["mtu"]}')