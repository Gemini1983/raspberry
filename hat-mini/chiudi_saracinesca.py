#!/usr/bin/env python3
import sys, automationhat

id_valvola=sys.argv[1]
automationhat.output[int(id_valvola)-1].write(0)