# install 
1. korean font
sudo apt-get install ibus ibus-hangul ttf-unfonts-core

2. keyboard layout 
sudo raspi-config 
105 layout

3. locale
asia > seoul

4. mouse cursor slow problem
sudo nano /boot/cmdline.txt
add 'usbhid.mousepoll=0'

5. pi 3.5inch display install 

    - http://bbangpan.tistory.com/82


    - /home/pi/Downloads 

    - cd LCD-show 

    - hdmi : sudo ./LCD-hdmi

    - display : sudo ./LCD35-show

# wlan 

sudo nano /etc/udev/rules.d/10-network.rules

SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="aa:bb:cc:dd:ee:ff", NAME="wlan0"   # 2.4 AP

SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ee:dd:cc:bb:aa", NAME="wlan1"   # 2.4 STATION

SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ee:dd:cc:bb:aa", NAME="wlan2"   # 5 AP

SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ee:dd:cc:bb:aa", NAME="wlan3"   # 5 STATION

SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ee:dd:cc:bb:aa", NAME="wlan4"   # wlan built in the pi 

# Set static IP

allow-hotplug wlan0

iface wlan0 inet static

wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
    
address 192.168.0.174

netmask 255.255.255.0

gateway 192.168.0.1

# AP mode
1. sudo apt-get install dnsmasq hostapd

2. sudo nano /etc/dhcpcd.conf

   - denyinterfaces wlan0

3. sudo nano /etc/network/interfaces

   - allow-hotplug wlan0  
  
   - iface wlan0 inet static  

   - address 192.24.1.1
    
   - netmask 255.255.255.0
    
   - network 192.24.1.0
    
   - broadcast 192.24.1.255
    
   - #wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

4. sudo service dhcpcd restart

5. sudo ifdown wlan0; sudo ifup wlan0

6. sudo nano /etc/hostapd/hostapd.conf

   - #This is the name of the WiFi interface we configured above
   
   - interface=wlan0

   - #Use the nl80211 driver with the brcmfmac driver
   
   - driver=rtl871xdrv #driver=nl80211
   
   - #This is the name of the network
   
   - ssid=Pi3-AP

   - #Use the 2.4GHz band
   
   - hw_mode=g

   - #Use channel 6
   
   - channel=6

   - #Enable 802.11n
   
   - ieee80211n=1

   - #Enable WMM
   
   - wmm_enabled=1

   - #Enable 40MHz channels with 20ns guard interval
   
   - ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]

   - #Accept all MAC addresses
   
   - macaddr_acl=0

   - #Use WPA authentication

   - auth_algs=1

   - #Require clients to know the network name

   - ignore_broadcast_ssid=0

   - #Use WPA2

   - wpa=2

   - #Use a pre-shared key

   - wpa_key_mgmt=WPA-PSK

   - #The network passphrase

   - wpa_passphrase=raspberry

   - #Use AES, instead of TKIP

   - rsn_pairwise=CCMP
   
7. sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf

8. Ctrl+C

9. sudo nano /etc/default/hostapd

   - DAEMON_CONF="/etc/hostapd/hostapd.conf"
   
10. sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig  

11. sudo nano /etc/dnsmasq.conf    

    - interface=wlan0      #Use interface wlan0 
   
    - listen-address=192.24.1.1 #Explicitly specify the address to listen on  

    - bind-interfaces      #Bind to the interface to make sure we aren't sending things elsewhere 

    - server=8.8.8.8       #Forward DNS requests to Google DNS  

    - domain-needed        #Don't forward short names  

    - bogus-priv           #Never forward addresses in the non-routed address spaces.  

    - dhcp-range=192.24.1.50,192.24.1.150,12h #Assign IP addresses between 192.24.1.50 and 192.24.1.150 with a 12 hour lease time

12. sudo nano /etc/sysctl.conf

    - remove the #from the beginning of the line containing net.ipv4.ip_forward=1

13. sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

14. sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE  

15. sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT  

16. sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT

17. sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

18. sudo nano /etc/rc.local

     - iptables-restore < /etc/iptables.ipv4.nat  
     
19. sudo service hostapd start  

20. sudo service dnsmasq start 

21. sudo reboot

# ip forwarding

sudo iptables -A PREROUTING -t nat -p tcp -d [receive IP] --dport [receive port] -j DNAT --to [next IP:next port]

sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

sudo iptables -t nat -F 

# realtek RTL8812AU

1. install necessary software

    - sudo apt-get update

    - sudo apt-get install bc git

    - sudo apt-get install libncurses5-dev


2. download rpi kernel source. takes some minutes

    - sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source

    - sudo chmod 755 /usr/bin/rpi-source

    - rpi-source -q --tag-update

    - rpi-source


3. download the rtl8812au kernel driver and complie it. takes some minutes

    - git clone https://github.com/gnab/rtl8812au.git

    - cd rtl8812au

    - sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/g' Makefile

    - sed -i 's/CONFIG_PLATFORM_ARM_RPI = n/CONFIG_PLATFORM_ARM_RPI = y/g' Makefile

    - make
    
    - sudo make install
    
    - sudo modprobe 8812au
    
    - reboot
    
5. pactch hostapd

    - Download 2.6.x version from here : http://w1.fi/hostapd/

    - rtl pactch file : https://github.com/pritambaral/hostapd-rtl871xdrv/archive/master.zip
    
    - unzip hostapd-2.6.zip and hostapd-rtl871xdrv-master.zip
    
    - sudo cp hostapd-rtl871xdrv-master/* hostapd-2.6/
    
    - sudo cp hostapd-rtl871xdrv-master/.c* hostapd-2.6/
    
    - cd hostapd-2.6
    
    - patch -Np1 -i rtlxdrv.patch
    
    - cp .config ./hostapd/

    - cd hostapd
    
    - make
    
    - sudo make install
    
    - sudo cp /usr/sbin/hostapd  /usr/sbin/hostapd-old
    
    - sudo cp /usr/sbin/hostapd_cli /usr/sbin/hostapd_cli-old

    - sudo cp /usr/local/bin/hostapd /usr/sbin/hostapd

    - sudo cp /usr/local/bin/hostapd_cli /usr/sbin/hostapd_cl
    
    - reboot
    
    
6. DKMS

    - sudo apt-get install build-essential dkms
    
    - sudo dkms add -m 8812au -v 4.2.2
    
    - sudo dkms build -m 8812au -v 4.2.2
    
    - sudo dkms install -m 8812au -v 4.2.2    
    
    
    
    
    
    
    
    
    

4. copy the driver and use it

    - sudo insmod 8812au.ko

    - sudo cp 8812au.ko /lib/modules/$(uname -r)/kernel/drivers/net/wireless

    - sudo depmod


5. disable the integrated wifi chip

    - sudo nano /etc/modprobe.d/raspi-blacklist.conf

    - (add) blacklist brcmfmac

    - (add) blacklist brcmutil


6. reboot

https://www.max2play.com/en/forums/topic/howto-raspberry-pi-3-realtek-802-11ac-rtl8812au/

https://layereight.de/raspberry-pi/2016/08/25/raspbian-rtl8812au.html
