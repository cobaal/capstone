# INSTALL
1. korean font

       sudo apt-get install ibus ibus-hangul ttf-unfonts-core

2. keyboard layout 

       sudo raspi-config > 105 layout

3. locale

       asia > seoul

4. mouse cursor slow problem

       sudo nano /boot/cmdline.txt
       add 'usbhid.mousepoll=0'

5. pi 3.5inch display install 

       http://bbangpan.tistory.com/82
       /home/pi/Downloads 
       cd LCD-show 
       hdmi : sudo ./LCD-hdmi
       display : sudo ./LCD35-show

# FIX WLAN 

sudo nano /etc/udev/rules.d/10-network.rules

    SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="aa:bb:cc:dd:ee:ff", NAME="wlan0"   # 2.4 AP
    SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ee:dd:cc:bb:aa", NAME="wlan1"   # 2.4 STATION
    SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ee:dd:cc:bb:aa", NAME="wlan2"   # 5 AP
    SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ee:dd:cc:bb:aa", NAME="wlan3"   # 5 STATION
    SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="ff:ee:dd:cc:bb:aa", NAME="wlan4"   # wlan built in the pi 

# INSTALL DNSMASQ & HOSTAPD

    sudo apt-get install dnsmasq hostapd

# INSTALL realtek RTL8812AU

1. install necessary software

       sudo apt-get install bc git
       sudo apt-get install libncurses5-dev

2. download rpi kernel source. takes some minutes

       sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source
       sudo chmod 755 /usr/bin/rpi-source
       rpi-source -q --tag-update
       rpi-source

3. download the rtl8812au kernel driver and complie it. takes some minutes

       git clone https://github.com/gnab/rtl8812au.git
       cd rtl8812au
        
       sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/g' Makefile
       sed -i 's/CONFIG_PLATFORM_ARM_RPI = n/CONFIG_PLATFORM_ARM_RPI = y/g' Makefile
        
       make
       sudo make install
       sudo modprobe 8812au
       reboot

# PATCH HOSTAPD FOR RTL8812AU DRIVER (WAY 1)

1. Download 2.6.x version from here : http://w1.fi/hostapd/

2. rtl pactch file : https://github.com/pritambaral/hostapd-rtl871xdrv/archive/master.zip
    
3. unzip hostapd-2.6.zip and hostapd-rtl871xdrv-master.zip
    
       sudo cp hostapd-rtl871xdrv-master/* hostapd-2.6/
       sudo cp hostapd-rtl871xdrv-master/.c* hostapd-2.6/
       cd hostapd-2.6
        
       patch -Np1 -i rtlxdrv.patch
       cp .config ./hostapd/
       cd hostapd
       make
       sudo make install
        
       sudo cp /usr/sbin/hostapd  /usr/sbin/hostapd-old
       sudo cp /usr/sbin/hostapd_cli /usr/sbin/hostapd_cli-old
       sudo cp /usr/local/bin/hostapd /usr/sbin/hostapd
       sudo cp /usr/local/bin/hostapd_cli /usr/sbin/hostapd_cli
       reboot

# PATCH HOSTAPD FOR RTL8812AU DRIVER (WAY 2)

       sudo git clone https://github.com/lostincynicism/hostapd-rtl8188.git
       sudo apt-get install libnl-3-dev
       sudo apt-get install libssl-dev
       sudo apt-get install libnl-genl-3-dev
       
       cd RTL8188-hostapd/hostapd
       make
       make install
        
       sudo cp /usr/sbin/hostapd  /usr/sbin/hostapd-old
       sudo cp /usr/sbin/hostapd_cli /usr/sbin/hostapd_cli-old
       sudo cp /usr/local/bin/hostapd /usr/sbin/hostapd
       sudo cp /usr/local/bin/hostapd_cli /usr/sbin/hostapd_cli
       reboot

# AP mode

1. sudo nano /etc/dhcpcd.conf

       denyinterfaces wlan0
       denyinterfaces wlan2        

2. sudo nano /etc/network/interfaces

       allow-hotplug wlan0 
              iface wlan0 inet static  
              address 192.24.1.1
              netmask 255.255.255.0
              network 192.24.1.0
              broadcast 192.24.1.255

       allow-hotplug wlan2
              iface wlan0 inet static  
              address 192.24.2.1
              netmask 255.255.255.0
              network 192.24.2.0
              broadcast 192.24.2.255
               
3. sudo service dhcpcd restart

4. sudo ifdown wlan0; sudo ifup wlan0

   sudo ifdown wlan2; sudo ifup wlan2

6. sudo nano /etc/hostapd/hostapd_2Ghz.conf

       #This is the name of the WiFi interface we configured above
       interface=wlan0

       #Use the nl80211 driver with the brcmfmac driver
       #driver=rtl871xdrv 
       driver=nl80211
   
       #This is the name of the network
       ssid=Router1 2.4GHz

       #Use the 2.4GHz band
       hw_mode=g

       #Use channel 1
       channel=1

       #Enable 802.11n
       ieee80211n=1

       #Enable WMM
       wmm_enabled=1

       #Enable 40MHz channels with 20ns guard interval
       ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]

       #Accept all MAC addresses
       macaddr_acl=0

       #Use WPA authentication
       auth_algs=1

       #Require clients to know the network name
       ignore_broadcast_ssid=0

       #Use WPA2
       wpa=2

       #Use a pre-shared key
       wpa_key_mgmt=WPA-PSK

       #The network passphrase
       wpa_passphrase=raspberry

       #Use AES, instead of TKIP
       rsn_pairwise=CCMP
   
7. sudo /usr/sbin/hostapd /etc/hostapd/hostapd_2Ghz.conf

8. Ctrl+C

9. sudo nano /etc/hostapd/hostapd_5Ghz.conf

       #This is the name of the WiFi interface we configured above
       interface=wlan2

       #Use the nl80211 driver with the brcmfmac driver
       driver=rtl871xdrv 
       #driver=nl80211
   
       #This is the name of the network
   
       ssid=Router1 5GHz

       #Use the 5GHz band
       hw_mode=a

       #Use channel 40
       channel=40

       #Enable 802.11n
       ieee80211n=1

       #Enable WMM
       wmm_enabled=1

       #Enable 40MHz channels with 20ns guard interval
       ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]

       #Accept all MAC addresses
       macaddr_acl=0

       #Use WPA authentication
       auth_algs=1

       #Require clients to know the network name
       ignore_broadcast_ssid=0

       #Use WPA2
       wpa=2

       #Use a pre-shared key
       wpa_key_mgmt=WPA-PSK

       #The network passphrase
       wpa_passphrase=raspberry

       #Use AES, instead of TKIP
       rsn_pairwise=CCMP
   
10. sudo /usr/sbin/hostapd /etc/hostapd/hostapd_5Ghz.conf

11. Ctrl+C

12. sudo nano /etc/default/hostapd

        DAEMON_CONF="/etc/hostapd/hostapd_2Ghz.conf /etc/hostapd/hostapd_5Ghz.conf"
   
13. sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig  

14. sudo nano /etc/dnsmasq.conf    

- TWO AP

      interface=wlan0
      interface=wlan2
    
      dhcp-range=wlan0,192.24.1.50,192.24.1.149,12h
      dhcp-range=wlan2,192.24.2.50,192.24.2.149,12h

- ONE AP

      #Use interface wlan0 
      interface=wlan0      
   
      #Explicitly specify the address to listen on
      listen-address=192.24.1.1   

      #Bind to the interface to make sure we aren't sending things elsewhere
      bind-interfaces      

      #Forward DNS requests to Google DNS 
      server=8.8.8.8        

      #Don't forward short names
      domain-needed          

      #Never forward addresses in the non-routed address spaces. 
      bogus-priv            

      #Assign IP addresses between 192.24.1.50 and 192.24.1.150 with a 12 hour lease time
      dhcp-range=192.24.1.50,192.24.1.150,12h 

15. sudo nano /etc/sysctl.conf

    - remove the #from the beginning of the line containing net.ipv4.ip_forward=1

16. sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

# MASQUERADE

- ONE AP

      sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE  
      sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT  
      sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT

- TWO AP

      sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE  
      sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT  
      sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT

      sudo iptables -t nat -A POSTROUTING -o wlan3 -j MASQUERADE  
      sudo iptables -A FORWARD -i wlan3 -o wlan2 -m state --state RELATED,ESTABLISHED -j ACCEPT  
      sudo iptables -A FORWARD -i wlan2 -o wlan3 -j ACCEPT

18. sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

19. sudo nano /etc/rc.local

        iptables-restore < /etc/iptables.ipv4.nat  
     
20. sudo service hostapd start  

21. sudo service dnsmasq start 

22. sudo reboot

# ip forwarding (NOT USES)

    sudo iptables -A PREROUTING -t nat -p tcp -d [receive IP] --dport [receive port] -j DNAT --to [next IP:next port]
    sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
    sudo iptables -t nat -F 

https://www.max2play.com/en/forums/topic/howto-raspberry-pi-3-realtek-802-11ac-rtl8812au/

https://layereight.de/raspberry-pi/2016/08/25/raspbian-rtl8812au.html
