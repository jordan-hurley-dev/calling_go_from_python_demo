import ctypes
import time
import json
from dataclasses import dataclass

# Python implementation
@dataclass
class Contact:
    name: str
    email: str
    phone: str

def py_validate_contact(string: str) -> bool:
    if not string:
        return False
    try:
        contact = Contact(**json.loads(string))
        if not contact.name or not contact.email or not contact.phone:
            return False
        return True
    except:
        return False


# Go implementation setup
lib = ctypes.cdll.LoadLibrary('./library.so')
_go_validate_contact = lib.ValidateContact
_go_validate_contact.argtypes = [ctypes.c_char_p]
_go_validate_contact.restype = ctypes.c_bool

def go_validate_contact(string: str) -> bool:
    return _go_validate_contact(string.encode('utf-8'))


# Testing and benchmarking
valid_contact = '{"name": "John Doe", "email": "john.doe@example.com", "phone": "123-456-7890"}'
invalid_contact = '{"name": "Jane Doe", "email": "jane.doe@invalid"}'

print("Testing Python validation:")
start_time = time.perf_counter()
valid_contact_result = py_validate_contact(valid_contact)
end_time = time.perf_counter()
print(f"Valid contact test: {valid_contact_result} - Time taken: {end_time - start_time:.6f} seconds")

start_time = time.perf_counter()
invalid_contact_result = py_validate_contact(invalid_contact)
end_time = time.perf_counter()
print(f"Invalid contact test: {invalid_contact_result} - Time taken: {end_time - start_time:.6f} seconds")

print("\nTesting Go validation:")
start_time = time.perf_counter()
valid_contact_result = go_validate_contact(valid_contact)
end_time = time.perf_counter()
print(f"Valid contact test: {valid_contact_result} - Time taken: {end_time - start_time:.6f} seconds")

start_time = time.perf_counter()
invalid_contact_result = go_validate_contact(invalid_contact)
end_time = time.perf_counter()
print(f"Invalid contact test: {invalid_contact_result} - Time taken: {end_time - start_time:.6f} seconds")
