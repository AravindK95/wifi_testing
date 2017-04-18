import os
import csv
import subprocess
from os import listdir
from os.path import isfile, join

# Variables 
host ="192.168.1.2:8888"
headers = ['retransmission', 'duplicate_ack', 'lost_segment', 'fast_retransmission', 'ack_rtt', 'frame_count', 'window_size', 'frame.len']
key_headers = [1, 5, 6, 8]
cwd = os.getcwd()

# Get list of all files
def get_all_pcap_files():
    return [f for f in listdir(cwd) if isfile(join(cwd, f)) and f.endswith('.pcap')]

# Get list of clients, given pcap filename
def get_clients(filename):
    print subprocess.Popen(['tshark', '-r', filename, '-q', '-z', 'conv,tcp'], cwd=cwd, stdout=subprocess.PIPE).stdout.read()
    p = subprocess.Popen(['tshark', '-r', filename, '-q', '-z', 'conv,tcp'], cwd=cwd, stdout=subprocess.PIPE)
    output = p.stdout.readlines()
    p.stdout.close()
    clients = []
    for line in output:
        out = line.split()
        if len(out) >= 3 and out[0] == host:
            clients.append(out[2].split(":")[0])
        if len(out) >= 3 and out[2] == host:
            clients.append(out[0].split(":")[0])
    return clients

# For each client, out put data
def scrape_file_by_client(filename, client):
    csv_row = []
    csv_row.append(client)
    filter = " and ip.src=={}".format(client)
    commands = ['tshark', '-r', filename, '-q', '-z', 'io,stat,200,\
                COUNT(tcp.analysis.retransmission) tcp.analysis.retransmission{0},\
                COUNT(tcp.analysis.duplicate_ack) tcp.analysis.duplicate_ack{0},\
                COUNT(tcp.analysis.lost_segment) tcp.analysis.lost_segment{0},\
                COUNT(tcp.analysis.fast_retransmission) tcp.analysis.fast_retransmission{0},\
                AVG(tcp.analysis.ack_rtt) tcp.analysis.ack_rtt{0},\
                COUNT(frame) frame{0},\
                AVG(tcp.window_size) tcp.window_size{0},\
                SUM(frame.len) frame.len{0}'.format(filter)]

    # print subprocess.Popen(commands, cwd=cwd, stdout=subprocess.PIPE).stdout.read()
    p = subprocess.Popen(commands, cwd=cwd, stdout=subprocess.PIPE)

    output = p.stdout.readlines()
    p.stdout.close()
    #print("\nStats for {}".format(client))
    for line in output:
        processed = map(str.strip, line.split("|"))
        # If last line
        if(len(processed) >= 2 and processed[1].find("<>") >= 0):
            for i, header in enumerate(headers):
                #print(header + ":" + processed[i+2])
                csv_row.append(processed[i+2])
    return csv_row

# Write out to csv
def initialize_csv():
    with open('data.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        # Write Headers
        writer.writerow(["Client\Headers"] + headers)

summary = {}
def append_to_csv(csv_data):
    print csv_data
    with open('data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        # Write Parsed Data
        for row in csv_data:
            writer.writerow(row)

        if len(row) >= 2:
            # collect Average Data
            total = [0] * len(row)
            for row in csv_data:
                for i, data in enumerate(row):
                    if (i != 0):
                        total[i] += float(data)
            average = [i/len(csv_data) for i in total]
            writer.writerow(total)
            writer.writerow(average)
            summary[len(csv_data)] = [total, average]

def append_summary_to_csv():
    with open('data.csv', 'a') as csvfile:
        names = summary.keys()
        writer = csv.writer(csvfile)
        writer.writerow(names)

        # Print significant data
        for header in key_headers:
            avgs = [0]*len(summary)
            tots = [0]*len(summary)
            for i, data in enumerate(summary):
                tots[i] = summary[data][0][header]
                avgs[i] = summary[data][1][header]
            writer.writerow(avgs)
            writer.writerow(tots)

if __name__ == "__main__":
    initialize_csv()
    filenames = get_all_pcap_files()
    for filename in filenames:
        print filename
        append_to_csv([[filename]])
        clients = get_clients(filename)
        csv_data = []
        for client in clients:
            csv_data.append(scrape_file_by_client(filename, client))
        append_to_csv(csv_data)
        append_to_csv([''])
    append_summary_to_csv()

