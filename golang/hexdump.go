package main

import (
    "fmt"
	"strings"
)

const (
    CROSS        = "╋"
    TOP_LEFT     = "┏"
    TOP_RIGHT    = "┓"
    BOTTOM_LEFT  = "┗"
    BOTTOM_RIGHT = "┛"
    LEFT_T       = "┣"
    RIGHT_T      = "┫"
    TOP_T        = "┳"
    BOTTOM_T     = "┻"
    VERTICAL     = "┃"
    HORIZONTAL   = "━"
)

func printLine(buffer []byte, offset int, lineLen int) {
    fmt.Printf("%06x |", offset)

    numBytes := len(buffer)

    for i := 0; i < lineLen; i++ {
        if i > 0 && i%4 == 0 {
            fmt.Print(" ")
        }
        if i < numBytes {
            fmt.Printf(" %02x", buffer[i])
        } else {
            fmt.Print("   ")
        }
    }

    fmt.Print(" | ")

    for i := 0; i < numBytes; i++ {
        if buffer[i] > 31 && buffer[i] < 127 {
            fmt.Printf("%c", buffer[i])
        } else {
            fmt.Print(".")
        }
    }

    fmt.Println()
}

func printDump(content []byte, offset int, toRead int, lineLen int) {
    for i := 0; i < toRead; i += lineLen {
        end := i + lineLen
        if end > toRead {
            end = toRead
        }
        printLine(content[i:end], offset+i, lineLen)
    }
}

func hexdumpInBox(content []byte, offset int, toRead int, lineLen int) {
    fmt.Printf("%s%s%s%s%s%s%s\n", TOP_LEFT, strings.Repeat(HORIZONTAL, 8), TOP_T, strings.Repeat(HORIZONTAL, lineLen*3+4), TOP_T, strings.Repeat(HORIZONTAL, 18), TOP_RIGHT)
    numLines := (toRead / lineLen) + 1

    for i := 0; i < numLines; i++ {
        fmt.Printf("%s %06x %s", VERTICAL, offset+i*lineLen, VERTICAL)

        for j := 0; j < lineLen; j++ {
            if j > 0 && j%4 == 0 {
                fmt.Print(" ")
            }
            if i*lineLen+j < toRead {
                fmt.Printf(" %02x", content[i*lineLen+j])
            } else {
                fmt.Print(" 00")
            }
        }

        fmt.Printf(" %s ", VERTICAL)

        for j := 0; j < lineLen; j++ {
            if i*lineLen+j < toRead {
                if content[i*lineLen+j] > 31 && content[i*lineLen+j] < 127 {
                    fmt.Printf("%c", content[i*lineLen+j])
                } else {
                    fmt.Print(".")
                }
            } else {
                fmt.Print(" ")
            }
        }

        fmt.Printf(" %s\n", VERTICAL)
    }

    fmt.Printf("%s%s%s%s%s%s%s\n", BOTTOM_LEFT, strings.Repeat(HORIZONTAL, 8), BOTTOM_T, strings.Repeat(HORIZONTAL, lineLen*3+4), BOTTOM_T, strings.Repeat(HORIZONTAL, 18), BOTTOM_RIGHT)
}