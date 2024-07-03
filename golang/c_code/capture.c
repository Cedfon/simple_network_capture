#include <linux/if.h>
#include <linux/if_ether.h>
#include <sys/ioctl.h>
#include <netpacket/packet.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <netinet/in.h>
#include <stdbool.h>
#include <stdlib.h>
#include <signal.h>

struct ifreq if_req;

static void invoke(void (*f)(char buf, int len), char buf, int len)
{
	f(buf, len);
}

void go_packets_capture_cb(char buf, int len);

typedef void (*closure)(char buf, int len);

int active_promisc(int fd)
{
	// Check if the promiscuous mode is already active
	if (ioctl(fd, SIOCGIFFLAGS, &if_req) < 0)
	{
		perror("ioctl: get ifflags");
		return 0;
	}

	if (if_req.ifr_flags & IFF_PROMISC)
	{
		return 0;
	}

	// Set the promiscuous mode
	if_req.ifr_flags |= IFF_PROMISC;

	if (ioctl(fd, SIOCSIFFLAGS, &if_req) < 0)
	{
		perror("ioctl: set ifflags");
		return 0;
	}

	return 1;
}

int deactive_promisc(int fd)
{
	// Check if the promiscuous mode is already inactive
	if (ioctl(fd, SIOCGIFFLAGS, &if_req) < 0)
	{
		perror("ioctl: get ifflags");
		return 0;
	}

	if (!(if_req.ifr_flags & IFF_PROMISC))
	{
		return 0;
	}

	// Unset the promiscuous mode
	if_req.ifr_flags &= ~IFF_PROMISC;

	if (ioctl(fd, SIOCSIFFLAGS, &if_req) < 0)
	{
		perror("ioctl: set ifflags");
		return 0;
	}

	return 1;
}

int init_capture(char *ifname, int promisc)
{
	struct sockaddr_ll saddr;
	int sock;

	// Create a raw socket for packet capturing
	sock = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
	if (sock < 0)
	{
		perror("socket");
		return -1;
	}

	// Set the interface name in the ifreq structure
	strncpy(if_req.ifr_name, ifname, sizeof(if_req.ifr_name) - 1);

	// Get the interface index using the interface name
	if (ioctl(sock, SIOCGIFINDEX, &if_req) < 0)
	{
		perror("ioctl");
		close(sock);
		return -1;
	}

	// Set the socket address structure
	saddr.sll_family = PF_PACKET;
	saddr.sll_protocol = htons(ETH_P_ALL);
	saddr.sll_ifindex = if_req.ifr_ifindex;

	// Enable promiscuous mode if specified
	if (promisc == true)
	{
		active_promisc(sock);
	}

	// Bind the socket to the interface
	if (bind(sock, (struct sockaddr *)&saddr, sizeof(saddr)) < 0)
	{
		perror("bind");
		close(sock);
		return -1;
	}

	return sock;
}

int capture_packets(int fd)
{
	while (1)
	{
		// Read packets
		char buf[65535];
		int len = recvfrom(fd, buf, sizeof(buf), 0, NULL, NULL);

		// Do something with the data
	}
}

int go_capture_packets(int fd, void (*fn)(char *buf, int len))
{
	while (1)
	{
		// Read packets
		char buf[65535];
		int len = recvfrom(fd, buf, sizeof(buf), 0, NULL, NULL);
		if (len < 0)
		{
			perror("recvfrom");
			break;
		}
		
		printf("%s", buf);
		fn(buf, len);
	}
}
