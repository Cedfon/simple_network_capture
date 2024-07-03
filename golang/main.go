package main

// #include "./c_code/capture.c"
import "C"
import (
	"os"
	"os/signal"
	"syscall"
	"fmt"
	"flag"
)

func capture(ifname string, promiscuousMode bool) {
	signalChannel := make(chan os.Signal, 1)
	signal.Notify(signalChannel, os.Interrupt, syscall.SIGTERM)

	isPromiscMode := 0
	if promiscuousMode {
		isPromiscMode = 1
	}


	fd := C.init_capture(C.CString(ifname), C.int(isPromiscMode))

	go C.go_capture_packets(fd, C.closure(C.go_packets_capture_cb))

	for {
		select {
		case content := <-channel:
			buf := []byte(content)
			hexdumpInBox(buf, 16, len(buf), 16)
		case <-signalChannel:
			println("Done")
			C.deactive_promisc(fd)
			os.Exit(0)
			return
		}
	}
}

func main() {
	interfaceName := flag.String("interface", "", "Interface to capture packets from")
    promiscuousMode := flag.Bool("p", false, "Enable promiscuous mode")
    flag.Parse()

    if *interfaceName == "" {
        fmt.Println("Interface name cannot be empty")
		fmt.Println("Usage: -interface <interface> [-p]")
        os.Exit(1)
    }

    capture(*interfaceName, *promiscuousMode)
}