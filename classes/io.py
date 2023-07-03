import json

class JSONHandler:
	"""
	TODO: Como usar:
	json_handler = JSONHandler()

	# Read data from a JSON file.
	data = json_handler.read_json('json_files/options.json')
	print(data)  # prints the content of the JSON file

	# Write data to a JSON file.
	data_to_write = {"some_key": "some_value"}
	json_handler.write_json('json_files/some_file.json', data_to_write)
	"""
	@staticmethod
	def read_json(file_path):
		"""Read a JSON file and return the data."""
		with open(file_path, 'r') as f:
			data = json.load(f)
		return data

	@staticmethod
	def write_json(file_path, data):
		"""Write data to a JSON file."""
		with open(file_path, 'w') as f:
			json.dump(data, f, indent=4)
