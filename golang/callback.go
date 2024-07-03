package main

import "C"

var channel = make(chan string, 100)
var done = make(chan bool)

//export go_packets_capture_cb
func go_packets_capture_cb(buf *C.char, size C.int) {
	content := C.GoStringN(buf, size)
	channel <- content
}