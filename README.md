# Rpi web controller

## backend

### Create

event: `create`

Create a new room for a web display

output:
```json
{
    "state": "create-room",
    "name": "1A2B3C",
}
```
---
### Close

event: `close`

Close an existing room from the web display

output:
```json
{
    "state": "close-room",
    "name": "1A2B3C",
}
```

---

### Join

event: `join`

Join a room to control the web display

input:

```json
{
    "room":"1A2B3C"
}
```

output:
```json
{
    "state": "joined-room",
    "sid": "8cCD3Ujsev_p5O1cAAAD",
    "room": "1A2B3C"
}
```

```json
{
    "state": "room-non-existent",
    "sid": "8cCD3Ujsev_p5O1cAAAD",
    "room": ""
}
```

---

### Leave

event: `leave`

Leave a room to control the web display

input:

```json
{
    "room":"1A2B3C"
}
```

output:
```json
{
    "state": "create-room",
    "sid": "8cCD3Ujsev_p5O1cAAAD",
    "room": "1A2B3C"
}
```
---

### Message

event: `messages`

Send a message to all suscribed to the room

input:

```json
{
    "room":"1A2B3C",
    "message":"Hello world"
}
```

output:
```json
{
    "state": "message",
    "sid": "8cCD3Ujsev_p5O1cAAAD",
    "message": "Hello world"
}
```
---

## frontend




## rpi