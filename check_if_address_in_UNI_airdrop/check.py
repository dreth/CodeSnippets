with open('./data/uniswap-distribution.csv') as f:
    data = [(x.split(',')[0],x.split(',')[1]) for x in [x.replace('\n','') for x in f.readlines()]]
    data_addresses = [x[0] for x in data]
    del data_addresses[0]
    del data[0]

with open('addresses.txt') as f:
    addresses = [x.replace('\n','') for x in f.readlines()]

for address in addresses:
    if address in data_addresses:
        amount = [x for x in data if x[0] == address][0][1]
        print(f'the address: {address} has {amount} UNI to claim')

input('\npress any key to exit...')