# capstone
1. sudo apt-get install dnsmasq hostapd

2. sudo nano /etc/dhcpcd.conf

   - denyinterfaces wlan0

3. sudo nano /etc/network/interfaces

   - allow-hotplug wlan0  
  
   - iface wlan0 inet static  

   - address 172.24.1.1
    
   - netmask 255.255.255.0
    
   - network 172.24.1.0
    
   - broadcast 172.24.1.255
    
   - #wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

4. sudo service dhcpcd restart

5. sudo ifdown wlan0; sudo ifup wlan0

6. sudo nano /etc/hostapd/hostapd.conf

   - #This is the name of the WiFi interface we configured above
   
   - interface=wlan0

   - #Use the nl80211 driver with the brcmfmac driver
   
   - driver=nl80211

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
   
    - listen-address=172.24.1.1 #Explicitly specify the address to listen on  

    - bind-interfaces      #Bind to the interface to make sure we aren't sending things elsewhere 

    - server=8.8.8.8       #Forward DNS requests to Google DNS  

    - domain-needed        #Don't forward short names  

    - bogus-priv           #Never forward addresses in the non-routed address spaces.  

    - dhcp-range=172.24.1.50,172.24.1.150,12h #Assign IP addresses between 172.24.1.50 and 172.24.1.150 with a 12 hour lease time

12. sudo nano /etc/sysctl.conf

    - remove the #from the beginning of the line containing net.ipv4.ip_forward=1

13. sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

14. sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE  

15. sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT  

16. sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

17. sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

18. sudo nano /etc/rc.local

     - iptables-restore < /etc/iptables.ipv4.nat  
     
19. sudo service hostapd start  

20. sudo service dnsmasq start 

21. sudo reboot
