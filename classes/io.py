import json

class JSONHandler:
	"""
	TODO: Como usar:
	json_handler = JSONHandler()

	# Ler os dados de um arquivo JSON.
	data = json_handler.read_json('json_files/options.json')
	print(data)  # imprime os dados do arquivo JSON

	# Escrevendo os dados num arquivo JSon.
	data_to_write = {"some_key": "some_value"}
	json_handler.write_json('json_files/some_file.json', data_to_write)
	"""
	@staticmethod
	def read_json(file_path):
		"""
		TODO:
		- Ler um arquivo JSon e retorna os dados dele
		- Adicionei encoding='utf-8' às funções open() em ambos os métodos. 
		  Isso garante que o arquivo seja lido e gravado como UTF-8.
		"""
		with open(file_path, 'r', encoding='utf-8') as f:
			data = json.load(f)
		return data

	@staticmethod
	def write_json(file_path, data):
		"""
		TODO:
		- Escreve os dados em um arquivo JSON
		- Adicionei ensure_ascii=False ao método json.dump(). 
		- Isso garante que os caracteres não ASCII sejam escritos no arquivo JSON corretamente, 
		  em vez de serem escapados com sequências.
		- Adicionei encoding='utf-8' às funções open() em ambos os métodos. 
		  Isso garante que o arquivo seja lido e gravado como UTF-8.
		"""
		with open(file_path, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=4, ensure_ascii=False)
