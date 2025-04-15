#!/bin/bash
socat - TCP:localhost:9999 <<THE_END
PUSH
1
2
3

ZAP

PEEK

THE_END


