valid_json = '''{
  "id": "root-0001",
  "name": "Example Nested Document",
  "version": 1,
  "active": true,
  "count": 42,
  "profile": {
    "username": "name",
    "email": "name@example.com",
    "created_at": "2023-05-18T12:34:56Z",
    "roles": [
      "admin",
      "editor",
      "user"
    ],
    "addresses": [
      {
        "type": "home",
        "line1": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "postal": "62701",
        "coordinates": {
          "lat": 39.7817,
          "lng": -89.6501
        }
      }
    ],
    "preferences": {
      "language": "en-US",
      "timezone": "America/Chicago",
      "notifications": {
        "email": true,
        "sms": false,
        "push": {
          "enabled": true,
          "sound": "chime",
          "vibrate": false
        }
      },
      "theme": {
        "name": "dark",
        "primary_color": "#0b3d91",
        "accent_color": "#ffcc00"
      }
    }
  }
}'''

invalid_json = '''{
  "id": "root-0001",
  "name": "Example Nested Document",
  "version": 1,
  "active": true,
  "count": 42,
  "null_field": null,
  "profile": {
    "username": "name",
    "email": "name@example.com",
    "created_at": "2023-05-18T12:34:56Z",
    "roles": [
      "admin",
      "editor",
      "user"
    ],
    "addresses": [
      {
        "type": "home",
        "line1": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "postal": "62701",
        "coordinates": {
          "lat": 39.7817,
          "lng": -89.6501
        }
      }
    ],
    "preferences": {
      "language": "en-US",
      "timezone": "America/Chicago",
      "notifications": {
        "email": true,
        "sms": false,
        "push": {
          "enabled": true,
          "sound": "chime",
          "vibrate": false
        }
      }
    }
  }
}'''