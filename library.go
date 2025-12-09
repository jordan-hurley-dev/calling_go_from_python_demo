package main

import (
	"C"
	"encoding/json"
	"reflect"
)

type Contact struct {
	Name  *string `json:"name"`
	Email *string `json:"email"`
	Phone *string `json:"phone"`
}

//export ValidateContact
func ValidateContact(jsonStr *C.char) C.uint {
	goStr := C.GoString(jsonStr)
	if goStr == "" {
		return 0
	}

	var contact *Contact
	err := json.Unmarshal([]byte(goStr), &contact)
	if err != nil {
		return 0
	}

	if contact == nil || reflect.ValueOf(contact).IsNil() {
		return 0
	}

	val := reflect.ValueOf(contact).Elem()
	for i := 0; i < val.NumField(); i++ {
		field := val.Field(i)
		if field.Kind() != reflect.Ptr || field.IsNil() {
			return 0
		}
		if field.Elem().Kind() == reflect.String && field.Elem().Len() == 0 {
			return 0
		}
	}

	return 1
}

func main() {}
