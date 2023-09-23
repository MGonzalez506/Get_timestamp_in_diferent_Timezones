#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import threading
import traceback
import time
import signal
import fcntl
import string
import re

from timestamp_timezones import *

if __name__ == "__main__":
	# Imprimir título
	os.write(
		sys.stdout.fileno(), 
		"\n######### Obtener timestamp con zonas horarias #########\n\n"
		.encode('utf-8')
		)
	
