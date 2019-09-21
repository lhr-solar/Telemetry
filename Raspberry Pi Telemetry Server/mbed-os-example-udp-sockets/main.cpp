#include "mbed.h"
#include "EthernetInterface.h"
#include "Watchdog.h"
 
Watchdog wd;
// Network interface
EthernetInterface net;
 
// Time protocol implementation : Address: time.nist.gov UDPPort: 37  
 
typedef struct {
    uint32_t secs;         // Transmit Time-stamp seconds.
}ntp_packet;
 
int main() {
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
        int random = rand() % 42;
        char out_buffer[512];
        memset(out_buffer, 0, 512);
        sprintf(out_buffer, "%d", random);
        if(0 > sock.sendto("192.168.4.2", 6969, out_buffer, sizeof(out_buffer))) {
            printf("Error sending data\n");
        }
        wd.Service();
        wait(5);
    }
    
    sock.close();
    net.disconnect();
    return 0;
}