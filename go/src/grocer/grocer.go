package main 

import (
	"log"
	"net"
	"os"
	"os/signal"
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

func responseFunc(c net.Conn) {
	for {
		buf := make([]byte, 512)
		nr, err := c.Read(buf)
		if err != nil {
			return
		}
		
		data := buf[0:nr]
		println("server got: ", string(data))
		_, err = c.Write(data)
		if err != nil {
			log.Fatal("writing client error: ", err)
		}
	}
}

func echoServer(c net.Conn) {
	for {
		buf := make([]byte, 512)
		nr, err := c.Read(buf)
		if err != nil {
			return
		}
		
		data := buf[0:nr]
		println("server got: ", string(data))
		_, err = c.Write(data)
		if err != nil {
			log.Fatal("writing client error: ", err)
		}
	}
}


func main() {
	log.Println("starting echo server...")
	ln, err := net.Listen("unix", "/tmp/grocer.sock")
	if err != nil {
		log.Fatal("listen error: ", err)
	}
	
	sigc := make(chan os.Signal, 1)
	signal.Notify(sigc, os.Interrupt, syscall.SIGTERM)
	go func(ln net.Listener, c chan os.Signal) {
		sig := <-c
		log.Printf("caught signal %s: shutting down", sig)
		ln.Close()
		os.Exit(0)
	}(ln, sigc)
	
	for {
		fd, err := ln.Accept()
		if err != nil {
			log.Fatal("accept error: ", err)
		}
		
		go echoServer(fd)
	}
}

