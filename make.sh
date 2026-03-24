#!/bin/bash
#
ca65 --cpu 65816 -o $1.o $1.asm
ld65 -C memmap.cfg $1.o -o $1.smc

