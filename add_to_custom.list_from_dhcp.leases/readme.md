# Tool to update pihole custom.list local domains with dhcp.leases

Simple script that reads dhcp.leases and fills/updates custom.list for custom local dns domains.

New domains can be added to `device_domain.json`, the `devices` key should use the device name as shown in the dhcp lease. The `domains` key should contain the corresponding domain to each item in `devices`, meaning that item 1 in `devices` will be pointed to the item 1 in `domains`.

The only point of this script is keeping updated custom.list in case a dhcp lease changes. It doesn't have to ever change if the lease is fixed. But if having a local device under a specific domain in local dns is mission critical, then this could prove useful.

I also think it's fun to play around with this kind of stuff, so I guess that makes any project worthwhile no matter how useless.
