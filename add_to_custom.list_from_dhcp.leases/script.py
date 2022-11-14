import json

# read from dhcp.leases and return
# a dict with the device name as key and dhcp lease as value
def read_leases():
    # return dict
    leases_dict = {}

    # read dhcp leases
    with open('dhcp.leases','r') as leases:
        contents = leases.read().splitlines()
        
        # only keep devices with names
        # assemble a dict with the dhcp lease and device name
        for line in contents:
            line_split = line.split(' ')
            if line_split[3] == '*':
                continue
            else:
                leases_dict[line_split[3]] = line_split[2]
    
    # return named device leases
    return leases_dict

# read custom.list
# so that we do not overwrite anything that was already set
# return it as a dict as well
def read_custom():
    # custom.list dict
    custom_dict = []

    # read custom.list
    with open('custom.list','r') as custom:
        contents = custom.read().splitlines()

        # assemble a dict with the ip and custom dns name
        for line in contents:
            line_split = line.split(' ')
            custom_dict.append((line_split[0],line_split[1]))
    
    # return custom.list dict
    return custom_dict

# generate items to append to custom.list on every run
def pair_devices_with_domain():
    # devices pairing
    with open('device_domain.json','r') as devices_json:
        dd = json.load(devices_json)
        devices_domains = list(zip(dd['devices'],dd['domains']))
        devices, domains = zip(*devices_domains) # this is kinda cool ngl...

    # get dhcp leases
    leases_dict = read_leases()

    # get custom.list
    custom_dict = read_custom()

    # generate dict with the pairings for custom.list
    # only add devices that are not already in custom.list
    # if the domain is already present, overwrite it with the new ip
    for i in range(len(custom_dict)):
        if custom_dict[i][1] in domains:
            idx = domains.index(custom_dict[i][1])
            custom_dict[i] = (leases_dict[devices[idx]],custom_dict[i][1])
    
    for device,domain in devices_domains:
        try:
            if domain not in list(zip(*custom_dict))[1]:
                custom_dict.append((leases_dict[device],domain))
        except:
            custom_dict.append((leases_dict[device],domain))


    # return the items to append to custom.list
    return custom_dict

# generate text to add to custom.list
def generate_custom_list_contents():
    # get new contents
    new_contents = pair_devices_with_domain()

    # generate text to add to custom.list
    text_to_add = ''
    for address,domain in new_contents:
        text_to_add += f"{address} {domain}\n"

    return text_to_add

# write to custom.list
def main():
    # generate contents
    contents = generate_custom_list_contents()

    # write to custom.list
    with open('custom.list','w') as custom:
        custom.write(contents)

if __name__ == '__main__':
    main()
