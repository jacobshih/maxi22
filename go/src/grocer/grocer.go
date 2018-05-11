package main

import (
	"log"
	"net"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"syscall"
)

type IPCSocket struct {
	sockFile string
	listener net.Listener
}

type ResponseFunc func(c net.Conn)

func (ipcSock *IPCSocket) init(s string) {
	ipcSock.sockFile = s
	ipcSock.listener = nil
}

func (ipcSock *IPCSocket) start() {
	ln, err := net.Listen("unix", ipcSock.sockFile)
	if err != nil {
		log.Fatal("listen error: ", err)
	} else {
		ipcSock.listener = ln
	}
	sigc := make(chan os.Signal, 1)
	signal.Notify(sigc, os.Interrupt, syscall.SIGTERM)
	go func(ln net.Listener, c chan os.Signal) {
		sig := <-c
		log.Printf("caught signal %s: shutting down", sig)
		ln.Close()
		os.Exit(0)
	}(ipcSock.listener, sigc)
}

func (ipcSock *IPCSocket) stop() {
}

func (ipcSock *IPCSocket) run(response ResponseFunc) {
	for {
		fd, err := ipcSock.listener.Accept()
		if err != nil {
			log.Fatal("accept error: ", err)
		}

		go response(fd)
	}
}

func getData(dataPath string) []byte {
	const dataDummy = `{
		"group01": {
			"1": {
				"name": "name01",
				"email": "name01@abc.com"
			},
			"2": {
				"name": "name02",
				"email": "name02@abc.com"
			},
			"event": [
				{
					"name": "event01",
					"description": "description01"
				}
			]
		}
	}
	`

	nodes := strings.Split(dataPath, "/")

	// FIXME - process the request here and remove temporary snippets.
	// +++ temporary
	debug := false
	if debug {
		for i := range nodes {
			println("   ", i, nodes[i])
		}
	} else {
		println(dataPath)
	}

	data := []byte(dataDummy)
	// --- temporary

	return data
}

func responseFunc(c net.Conn) {
	for {
		buf := make([]byte, 512)
		nr, err := c.Read(buf)
		if err != nil {
			return
		}

		// filepath.Clean() helps normalize the path.
		// e.g., replace multiple separators with a single one.
		dataPath := filepath.Clean(string(buf[:nr]))
		data := []byte(getData(dataPath))
		_, err = c.Write(data)
		if err != nil {
			log.Fatal("writing client error: ", err)
		}
	}
}

func main() {
	log.Println("starting grocer...")

	// FIXME - initialize backend here.

	ipcsock := IPCSocket{}
	ipcsock.init("/tmp/grocer.sock")
	ipcsock.start()
	ipcsock.run(responseFunc)
	ipcsock.stop()
}
