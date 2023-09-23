import os
import json
import logging

# Import unit test module
import unittest

# Import the functions to test
from timestamp_timezones import *

# Get the current directory
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(filename='Logs/unit_test.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

