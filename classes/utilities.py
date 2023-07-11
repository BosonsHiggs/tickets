import random
import time

class UniqueIdGenerator:
    @staticmethod
    def generate_unique_custom_id():
        timestamp = time.time()  # Tempo atual em segundos
        rand_num = random.randint(0, 100000)  # Um número aleatório

        #Converte ambos valores em hexadecimal e depois os combinam
        custom_id = hex(int(timestamp))[2:] + hex(rand_num)[2:]

        return custom_id[:100]  # Trunca em 100 caracteres se necessário
