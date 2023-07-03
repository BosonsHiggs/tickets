import random
import time

class UniqueIdGenerator:
    @staticmethod
    def generate_unique_custom_id():
        timestamp = time.time()  # Current time in seconds
        rand_num = random.randint(0, 100000)  # A random number

        # Convert both values to hexadecimal and combine
        custom_id = hex(int(timestamp))[2:] + hex(rand_num)[2:]

        return custom_id[:100]  # Truncate to 100 characters if necessary
