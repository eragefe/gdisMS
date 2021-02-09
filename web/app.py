from flask import Flask, render_template, request
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
    os.system('mv wifi.tmp /root/wifi')
    os.system('sed -i "$ i bash /root/startwifi" /etc/rc.local')
    os.system('bash /root/wifi')
    return ('', 204)

@app.route("/volume", methods = ['GET', 'POST'])
def volume():
    a = request.form["a"]
    create_file(a)
    os.system('cp vol.tmp /root/vol')
    os.system('bash /root/volweb')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return ('', 204)

def create_file(a):

    temp_conf_file = open('vol.tmp', 'w')
    temp_conf_file.write('' + a + '')
    temp_conf_file.close

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/sound')
def sound():
    return render_template('sound.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/power')
def power():
    return render_template('power.html')

@app.route('/net')
def net():
    os.system('bash /root/net')
    return ('', 204)

@app.route('/nos')
def nos():
    os.system('i2cset -y 1 17 5 1')
    return render_template('nos.html')

@app.route('/sound1')
def sound1():
    os.system('i2cset -y 1 17 5 0')
    os.system('i2cset -y 1 17 8 4')
    return render_template('sound1.html')

@app.route('/sound2')
def sound2():
    os.system('i2cset -y 1 17 8 0')
    return render_template('sound2.html')

@app.route('/volup', methods = ['GET', 'POST'])
def volup():
    os.system('bash /root/volup')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

@app.route('/voldown', methods = ['GET', 'POST'])
def voldown():
    os.system('bash /root/voldown')
    with open("/root/vol", "r") as f:
         vol = f.read()
    return render_template('app.html', vol=vol)

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

@app.route('/streamer', methods = ['GET', 'POST'])
def streamer():
    os.system('bash /root/streamer')
    return ('', 204)

@app.route('/optical1', methods = ['GET', 'POST'])
def optical1():
    os.system('bash /root/optical1')
    return ('', 204)

@app.route('/optical2', methods = ['GET', 'POST'])
def optical2():
    os.system('bash /root/optical2')
    return ('', 204)

@app.route('/coaxial1', methods = ['GET', 'POST'])
def coaxial1():
    os.system('bash /root/coaxial1')
    return ('', 204)

@app.route('/coaxial2', methods = ['GET', 'POST'])
def coaxial2():
    os.system('')
    return ('', 204)

@app.route('/s1', methods = ['GET', 'POST'])
def s1():
    os.system('bash /root/test')
    return ('', 204)

@app.route('/prev', methods = ['GET', 'POST'])
def prev():
    os.system('mpc prev')
    return ('', 204)

@app.route('/play', methods = ['GET', 'POST'])
def play():
    os.system('mpc toggle')
    return ('', 204)

@app.route('/stop', methods = ['GET', 'POST'])
def stop():
    os.system('mpc stop')
    return ('', 204)

@app.route('/next', methods = ['GET', 'POST'])
def next():
    os.system('mpc next')
    return ('', 204)

######## FUNCTIONS ##########

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

    temp_conf_file = open('wifi.tmp', 'w')

    temp_conf_file.write('#!/bin/bash\n')
    temp_conf_file.write('\n')
    temp_conf_file.write('nmcli r wifi on\n')
    temp_conf_file.write('nmcli d wifi connect ' + ssid + '  password  ' + wifi_key + '\n')
    temp_conf_file.close

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
