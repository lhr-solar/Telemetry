#include "mbed.h"
#include "EthernetInterface.h"
#include "Watchdog.h"
 
Watchdog wd;
// Network interface
EthernetInterface net;
  
int main() {
    //Set up watchdog timer to restart system if connection is lost
    wd.Configure(15);
    // Bring up the ethernet interface
    printf("UDP Socket Initializing\n");
    while(0 != net.connect()) {
        printf("Error connecting, retrying...\n");
        wd.Service();
    }
 
    // Show the network address
    const char *ip = net.get_ip_address();
    printf("IP address is: %s\n", ip ? ip : "No IP");
        
    UDPSocket sock(&net);
    SocketAddress sockAddr;
 
    while(1){
        // For now just send a random number between 0 and 41 as the speed.
        int random = rand() % 42;
        char out_buffer[512];
        memset(out_buffer, 0, 512);
        sprintf(out_buffer, "%d", random);
        if(0 > sock.sendto("192.168.4.2", 6969, out_buffer, sizeof(out_buffer))) {
            printf("Error sending data\n");
        }
        wd.Service();
        // We wait 5 seconds between each udp packet. This is because
        // the database and grafana only updat once every 5 seconds
        wait(5);
    }
    
    sock.close();
    net.disconnect();
    return 0;
}