package main

/*
	Dmitrii Shaporenko, 2020
	To build run:
	go build -ldflags="-s -w" tool.go

*/

import (
	"fmt"
	"os"
	"strconv"
)

func fall() {
	println("Tool expects one int or float argument.")
	os.Exit(1)
}

func main() {

	if len(os.Args) != 2 {
		fall()
	}
	if num, err := strconv.ParseFloat(os.Args[1], 64); err == nil {
		fmt.Println(1.0 / num)
		os.Exit(0)
	} else if num, err := strconv.ParseUint(os.Args[1], 10, 64); err == nil {
		fmt.Println(1.0 / float64(num))
		os.Exit(0)
	} else {
		fall()
	}
}
