import ctypes
import time

from pydantic import BaseModel

from examples import valid_json, invalid_json

TEST_TRIALS = 10000

# Pydantic validation setup
class Contact(BaseModel):
    id: str
    name: str
    version: int
    active: bool
    count: int
    profile: "Profile"

class Profile(BaseModel):
    username: str
    email: str
    created_at: str
    roles: list[str]
    addresses: list["Addresses"]
    preferences: "Preferences"

class Addresses(BaseModel):
    type: str
    line1: str
    city: str
    state: str
    postal: str
    coordinates: "Coordinates"

class Coordinates(BaseModel):
    lat: float
    lng: float

class Preferences(BaseModel):
    language: str
    timezone: str
    notifications: "Notifications"
    theme: "Theme"

class Notifications(BaseModel):
    email: bool
    sms: bool
    push: "Push"

class Push(BaseModel):
    enabled: bool
    sound: str
    vibrate: bool

class Theme(BaseModel):
    name: str
    primary_color: str
    accent_color: str


def pyd_validate_contact(string: str) -> bool:
    if not string:
        return False
    try:
        Contact.model_validate_json(string)
        return True
    except:
        return False

# Go validation setup
lib = ctypes.cdll.LoadLibrary('./library.so')
_go_validate_contact = lib.ValidateContact
_go_validate_contact.argtypes = [ctypes.c_char_p]
_go_validate_contact.restype = ctypes.c_bool

def go_validate_contact(string: str) -> bool:
    return _go_validate_contact(string.encode('utf-8'))

# valid_contact = '{"name": "John Doe", "email": "john.doe@example.com", "phone": "123-456-7890"}'
# invalid_contact = '{"name": "Jane Doe", "email": "jane.doe@invalid"}'
valid_contact = str(valid_json)
invalid_contact = str(invalid_json)

def test_validation(name: str, validation_function: callable) -> str:
    print(f"Testing {name} validation:")
    print("----------------------------------------------------------")
    
    valid_test_passed: bool = True
    valid_test_total_time: float = 0.0
    for _ in range(TEST_TRIALS):
        is_valid, time_taken = perform_validation(validation_function, valid_contact)
        valid_test_total_time += time_taken
        if not is_valid:
            valid_test_passed = False
    print(f"Valid contact test: {'Passed' if valid_test_passed else 'Failed'} - Average time taken: {valid_test_total_time / TEST_TRIALS:.7f} seconds")
    
    invalid_test_passed: bool = True
    invalid_test_total_time: float = 0.0
    for _ in range(TEST_TRIALS):
        is_valid, time_taken = perform_validation(validation_function, invalid_contact)
        invalid_test_total_time += time_taken
        if is_valid:
            invalid_test_passed = False
    print(f"Invalid contact test: {'Passed' if invalid_test_passed else 'Failed'} - Average time taken: {invalid_test_total_time / TEST_TRIALS:.7f} seconds")
    print()

def perform_validation(validation_function: callable, json_string: str) -> tuple[bool, float]:
    start_time = time.perf_counter()
    is_valid = validation_function(json_string)
    end_time = time.perf_counter()
    return is_valid, end_time - start_time

if __name__ == "__main__":
    print("Starting validation tests...\n")
    test_validation("Pydantic", pyd_validate_contact)
    test_validation("Go", go_validate_contact)