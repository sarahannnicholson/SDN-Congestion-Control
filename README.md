# Congestion-Control-in-SDN
# Motivation
The internet took off faster than anyone could have predicted. Nowadays, everything from cars, security systems, wearables, to kitchen appliances are connected through wifi or bluetooth, contributing to the Internet of Things. Users also have high expectations regarding good performance. This increased demand on traditional internet protocols and topologies has sprouted a new age of technology. Along with the immense growth of devices connecting to the network, the cloud has also creeped into the spotlight. Many companies provide Software As A Service (SAAS) to consumers to use their cloud technologies; for instance, Google Drive, DropBox, Amazon Web Services and many more. Some companies offer their computing resources to consumers or businesses for a price. This is know as cloud computing and has become extremely popular nowadays, especially in an era of big data. With large clusters of servers, high computational tasks can be offloaded onto a computer cluster which has a large amount of resources. Cloud computing is extremely useful for large computations on an immense amount of data that a single computer would be unable to perform. This brings us to the concept of datacentes.
 
Datacenters could consist of thousands of computers that need to provide quick service to customers; so performance is a large concern. One way to increase the performance within a datacenter network is to have good congestion control; because when a link gets very congested, the transmission delay is greatly increased and full bandwidth is not utilized. A good congestion control algorithm will cause the nodes in the network to forwards packets on a different route to distribute the load and get the most out of the link bandwidths. This will cause a high throughput, which is essential to datacenter network performance.

# Scope
For the project I decided to implement congestion control by rate limiting a link that uses a certain amount of bandwidth. This guarantees that other hosts will be able to use the same network and receive the quality of service they are expecting. 

# Setup
For simplicity, I exported my VirtualBox setup to Sarahs_VM_Setup.ova so that it could easily be imported into VirtualBox. I did this because it was difficult to keep track of all the libraries I downloaded in the length of this project. 
1. Download Sarahs_VM_Setup.ova https://drive.google.com/file/d/0BzgWPOej9NxdUExiNmtBQmRlNnc/view?usp=sharing
2. Import it into VirtualBox by going: File → Import Appliance → locate the file on your computer → Next → Import 
3. Start the box
4. The address may need to be configured on the box, this can be done by logging into the box via the VirtualBox terminal and assigning eth0 an IP address. In this case, mine was 192.168.56.102. 
5. I had Xming installed for the x11 window display (which uses DISPLAY=127.0.0.1:0.0) 
    * In my host terminal I executed export DISPLAY=127.0.0.1:0.0 
    * Then ssh -AYX mininet@192.168.56.102 
6. Once I was logged in, I made sure I had internet access by doing sudo dhclient eth1
7. And made sure that no mininet nodes were left over sudo mn -c

Since the .ova has this project already setup in the VB instance, downloading the repo is not required

