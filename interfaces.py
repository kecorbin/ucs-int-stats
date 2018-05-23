from ucsmsdk.ucshandle import UcsHandle
import yaml
from tabulate import tabulate

if __name__ == "__main__":
    data = []

    with open('config.yaml', 'r') as config:
        config = yaml.safe_load(config)
    hostname, username, password = config['host'], config['name'], config['passwd']
    handle = UcsHandle(hostname, username, password)
    print("Connecting to UCSM at {} as {} ......".format(hostname, username)),
    if handle.login():
        print("Success")
    interfaces = handle.query_classid('etherPIo')

    for interface in interfaces:
        dn = interface.dn
        rx_stats = handle.query_dn(interface.dn + '/rx-stats')
        rx_packets = rx_stats.total_packets
        rx_bytes = rx_stats.total_bytes
        tx_stats = handle.query_dn(interface.dn + '/tx-stats')
        tx_packets = tx_stats.total_packets
        tx_bytes = tx_stats.total_bytes
        err_stats = handle.query_dn(interface.dn + '/err-stats')
        tx_discards = err_stats.out_discard
        values = [rx_packets, rx_bytes,
                  tx_packets, tx_bytes,
                  tx_discards]
        if not all(v == '0' for v in values):
            data.append([dn,
                         rx_packets,
                         rx_bytes,
                         tx_packets,
                         tx_bytes,
                         tx_discards])
    print(tabulate(data, headers=["DN",
                                  "RX Packets",
                                  "RX Bytes",
                                  "TX Packets",
                                  "TX Bytes",
                                  "Out Drops"]))
