package main

import (
	"net/http"

	"github.com/raifpy/Go/errHandler"
)

func main() {
	err := http.ListenAndServe(":1011", http.FileServer(http.Dir("files")))
	errHandler.HandlerExit(err)
}
