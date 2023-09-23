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

class TestTimestamp(unittest.TestCase):

	# Test get TimestampFormat, Timezone and NumberOfDecimalPoints
	def test_get_timestamp_format_timezone_and_number_of_decimal_points(self):
		json_data = {}
		try:
			input_file = THIS_FOLDER + '/test_data.json'
			# Import json data from input_file
			with open(input_file, 'r') as f:
				json_data = json.load(f)
				# Close file
				f.close()
		except Exception as e:
			t_actual = get_UTC_Now("%Y-%m-%dT%H:%M:%S")
			log_msg = "---> T_UTC: " + t_actual + " - There is something wrong in file: " + os.path.basename(input_file) + " - Check if json format is ok, if file is empty or if the file exists."
			logging.error(log_msg)
			self.assertTrue(False)
		
		# Create empty list for timestamp_examples data
		timestamp_examples_data = []
		# Check if data is not empty
		if json_data:
			# Get the timestamp_examples data
			timestamp_examples_data = json_data["timestamp_format_tz_decimalPoints"]
			# Get the number of elements inside the timestamp_examples tag
			num_elements = len(timestamp_examples_data)
			if num_elements != 0:
				# Iterate over the elements inside the timestamp_examples tag
				for i in range(num_elements):
					# Get the timestamp
					timestamp = timestamp_examples_data[i]["timestamp"]
					# Get the expected timezone
					expected_timezone = timestamp_examples_data[i]["timezone"]
					# Get the default timezone
					default_timezone = timestamp_examples_data[i]["default_tz"]
					# Get the expected timestamp format
					expected_timestamp_format = timestamp_examples_data[i]["timestamp_format"]
					# Get the expected number of decimal points
					expected_number_of_decimal_points = timestamp_examples_data[i]["number_of_decimal_points"]
					# Get the expected timestamp format, timezone and number of decimal points
					timestamp_format, timezone, number_of_decimal_points = get_timestamp_format_timezone_and_numberOfDecimalPoints(timestamp, default_timezone)
					# Check if the timestamp format is the expected
					self.assertEqual(timestamp_format, expected_timestamp_format)
					# Check if the timezone is the expected
					self.assertEqual(timezone, expected_timezone)
					# Check if the number of decimal points is the expected
					self.assertEqual(number_of_decimal_points, expected_number_of_decimal_points)


	# Test the conversion from timezone to timezone
	def test_convert_tz_timestamp(self):
		json_data = {}
		try:
			input_file = THIS_FOLDER + '/test_data.json'
			# Import json data from input_file
			with open(input_file, 'r') as f:
				json_data = json.load(f)
				# Close file
				f.close()

			#data = json.load(open(input_file, 'r'))
		except Exception as e:
			t_actual = get_UTC_Now("%Y-%m-%dT%H:%M:%S")
			log_msg = "---> T_UTC: " + t_actual + " - There is something wrong in file: " + os.path.basename(input_file) + " - Check if json format is ok, if file is empty or if the file exists."
			logging.error(log_msg)
			self.assertTrue(False)
		
		# Create empty list for same_format_different_tz data
		same_format_different_tz_data = []
		# Check if data is not empty
		if json_data:
			# Get the same_format_different_tz data
			same_format_different_tz_data = json_data["same_format_different_tz"]
			# Get the number of elements inside the same_format_different_tz tag
			num_elements = len(same_format_different_tz_data)
			if num_elements != 0:
				for i in range(num_elements):
					# Get the input timestamp
					input_timestamp = same_format_different_tz_data[i]['input_timestamp']
					# Get the expected timestamp
					expected_timestamp = same_format_different_tz_data[i]['output_timestamp']
					# Get the timestamp format
					timestamp_format = same_format_different_tz_data[i]['timestamp_format']
					# Get the input timezone
					input_tz = same_format_different_tz_data[i]['input_timezone']
					# Get the output timezone
					output_tz = same_format_different_tz_data[i]['output_timezone']
					# Convert the timestamp from input timezone to output timezone
					timestamp_converted = convert_from_timezone_to_timezone(input_timestamp, timestamp_format, input_tz, output_tz)
					# Compare the expected timestamp with the converted timestamp
					self.assertTrue (timestamp_converted == expected_timestamp)
			else:
				# Log that there where no information in the tag inside the json file
				t_actual = get_UTC_Now("%Y-%m-%dT%H:%M:%S")
				log_msg = "---> T_UTC: " + t_actual + " - No data on the tag 'same_format_different_tz' inside document: " + os.path.basename(input_file)
				logging.error(log_msg)
				self.assertTrue(False)
		else:
			# Log that there where no information in the tag inside the json file
			t_actual = get_UTC_Now("%Y-%m-%dT%H:%M:%S")
			log_msg = "---> T_UTC: " + t_actual + " - No data inside document: " + os.path.basename(input_file)
			logging.error(log_msg)
			self.assertTrue(False)

		self.assertTrue(True)

if __name__ == '__main__':
	print("\n\n\n")
	print("Iniciando unit test...")
	# Create unit test
	unittest.main()