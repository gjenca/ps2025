#!/bin/bash
socat - TCP:localhost:9999 <<THE_END
PUSH
1
2
3

ADD

PEEK

THE_END


