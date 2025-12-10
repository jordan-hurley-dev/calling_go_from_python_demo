package main

import (
	"C"
	"encoding/json"
)
import "reflect"

type Contact struct {
	Id      *string  `json:"id"`
	Name    *string  `json:"name"`
	Version *int     `json:"version"`
	Active  *bool    `json:"active"`
	Count   *int     `json:"count"`
	Profile *Profile `json:"profile"`
}

type Profile struct {
	Username    *string      `json:"username"`
	Email       *string      `json:"email"`
	CreatedAt   *string      `json:"created_at"`
	Roles       []string     `json:"roles"`
	Addresses   []Address    `json:"addresses"`
	Preferences *Preferences `json:"preferences"`
}

type Address struct {
	Type        *string      `json:"type"`
	Line1       *string      `json:"line1"`
	City        *string      `json:"city"`
	State       *string      `json:"state"`
	Postal      *string      `json:"postal"`
	Coordinates *Coordinates `json:"coordinates"`
}

type Coordinates struct {
	Lat *float64 `json:"lat"`
	Lng *float64 `json:"lng"`
}

type Preferences struct {
	Language      *string        `json:"language"`
	Timezone      *string        `json:"timezone"`
	Notifications *Notifications `json:"notifications"`
	Theme         *Theme         `json:"theme"`
}

type Notifications struct {
	Email *bool `json:"email"`
	SMS   *bool `json:"sms"`
	Push  *Push `json:"push"`
}

type Push struct {
	Enabled *bool   `json:"enabled"`
	Sound   *string `json:"sound"`
	Vibrate *bool   `json:"vibrate"`
}

type Theme struct {
	Name         *string `json:"name"`
	PrimaryColor *string `json:"primary_color"`
	AccentColor  *string `json:"accent_color"`
}

//export ValidateContact
func ValidateContact(jsonStr *C.char) C.uint {
	goStr := C.GoString(jsonStr)
	if goStr == "" {
		return 0
	}

	var contact Contact
	err := json.Unmarshal([]byte(goStr), &contact)
	if err != nil {
		return 0
	}

	if !validateNoNilPointers(contact) {
		return 0
	}

	return 1
}

func validateNoNilPointers(v any) bool {
	return validateNoNilPointersValue(reflect.ValueOf(v))
}

func validateNoNilPointersValue(val reflect.Value) bool {
	switch val.Kind() {
	case reflect.Pointer:
		if val.IsNil() {
			return false
		}
		return validateNoNilPointersValue(val.Elem())
	case reflect.Struct:
		for i := 0; i < val.NumField(); i++ {
			field := val.Field(i)
			if !validateNoNilPointersValue(field) {
				return false
			}
		}
		return true
	case reflect.Slice, reflect.Array:
		for i := 0; i < val.Len(); i++ {
			if !validateNoNilPointersValue(val.Index(i)) {
				return false
			}
		}
		return true
	default:
		return true
	}
}

func main() {}
