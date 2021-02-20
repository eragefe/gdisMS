from flask import Flask, flash, render_template, request
import subprocess
import os
import time

app = Flask(__name__)
app.debug = True


@app.route('/', methods = ['GET', 'POST'])
def index():
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route('/wifi')
def wifi():
    wifi_ap_array = scan_wifi_networks()

    return render_template('wifi.html', wifi_ap_array = wifi_ap_array)

@app.route('/manual_ssid_entry')
def manual_ssid_entry():
    return render_template('manual_ssid_entry.html')

@app.route('/save_credentials', methods = ['GET', 'POST'])
def save_credentials():
    ssid = request.form['ssid']
    wifi_key = request.form['wifi_key']
    create_wpa_supplicant(ssid, wifi_key)
    os.system('bash /tmp/wifi.tmp')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route("/volume2", methods = ['GET', 'POST'])
def volume2():
    a = request.form["c"]
    create_file(a)
    os.system('/usr/bin/amixer -M set Master $(cat /root/vol)% > /dev/null 2>&1')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route("/volume", methods = ['GET', 'POST'])
def volume():
    a = request.form["a"]
    create_file(a)
    os.system('/usr/bin/amixer -M set Master $(cat /root/vol)% > /dev/null 2>&1')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route('/input', methods = ['GET', 'POST'])
def input():
    input = request.form["input"]
    if input == "coax":
         os.system('bash /root/coaxial1')
    if input == "opt1":
         os.system('bash /root/optical1')
    if input == "opt2":
         os.system('bash /root/optical2')
    if input == "streamer":
         os.system('bash /root/streamer')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route('/test', methods = ['GET', 'POST'])
def test():
    test = request.form["test"]
    if test == "sound":
        os.system('bash /root/test')
    if test == "net":
        os.system('bash /root/net')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route('/power')
def power():
    return render_template('power.html')

@app.route('/reboot', methods = ['GET', 'POST'])
def reboot():
    time.sleep(1)
    os.system('reboot')
    return ('', 204)

@app.route('/poweroff', methods = ['GET', 'POST'])
def poweroff():
    time.sleep(1)
    os.system('poweroff')
    return ('', 204)

@app.route('/prev', methods = ['GET', 'POST'])
def prev():
    os.system('mpc prev')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route('/play', methods = ['GET', 'POST'])
def play():
    os.system('mpc toggle')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route('/stop', methods = ['GET', 'POST'])
def stop():
    os.system('mpc stop')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route('/next', methods = ['GET', 'POST'])
def next():
    os.system('mpc next')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

######## FUNCTIONS ##########

def create_file(a):

    temp_conf_file = open('/root/vol', 'w')
    temp_conf_file.write('' + a + '')
    temp_conf_file.close

def scan_wifi_networks():
    iwlist_raw = subprocess.Popen(['iwlist', 'scan'], stdout=subprocess.PIPE)
    ap_list, err = iwlist_raw.communicate()
    ap_array = []

    for line in ap_list.decode('utf-8').rsplit('\n'):
        if 'ESSID' in line:
            ap_ssid = line[27:-1]
            if ap_ssid != '':
                ap_array.append(ap_ssid)

    return ap_array

def create_wpa_supplicant(ssid, wifi_key):

    temp_conf_file = open('/tmp/wifi.tmp', 'w')

    temp_conf_file.write('#!/bin/bash\n')
    temp_conf_file.write('\n')
    temp_conf_file.write('nmcli r wifi on\n')
    temp_conf_file.write('nmcli d wifi connect ' + ssid + '  password  ' + wifi_key + '\n')
    temp_conf_file.close

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
