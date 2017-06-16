# TODO
* ~~Design Dao test framework~~
* ~~Move utils classes to a Utils folder~~
* ~~ApiValidator methods for Attendee fields~~
* Create service layer for Event/Attendees
* ~~create base exception class~~
* test user filter
* integrate user filter and retest api
* availability validation
* year mechanism
* switch all of api method to use service layer
* query to load events by attendee

# Request Objects
## Events
### URL
`/events`
* GET - Returns all events (see response object)
* POST - Creates a new event (see request/response objects)
* PUT - Not used
* DELETE - Not used

`/events/{id}`
* GET - Returns the event details (see response object)
* POST - not used
* PUT - Updates this event
* DELETE - Deletes this event

### Request
```
{
  name: String,
  creator: String
}
```

### Response
```
{
  id: String,
  name: String,
  creator: String,
  created_date: date
}
```

## Attendee
### URL
`/events/{id}/attendees`
* GET - Returns all attendees for this event (see response object)
* POST - Creates a new attendee for this event (see request/response objects)
* PUT - Not used
* DELETE - Not used

`/events/{id}/attendees/{id}`
* GET - Returns the attendee details (see response object)
* POST - not used
* PUT - Updates this attendee
* DELETE - Deletes this attendee (just removes them from the event)

### Request
```
{
  name: String,
  email: String (optional)
}
```

### Response
```
{
  id: int,
  name: String,
  email: String
}
```

## Availability
### URL
`/events/{id}/attendees/{id}/availability`
* GET - Returns compiled availability for this attendee (see response object)
* POST - Creates a new availability for this event (see request/response objects)
* PUT - Not used
* DELETE - Not used

`/events/{id}/attendees/{id}/availability/{id}`
* GET - Returns the availability details (see response object)
* POST - not used
* PUT - Updates this availability
* DELETE - Deletes this availability

### Request
```
{
  attendee_name: String,
  year: String
}
```

### Response
```
{
  id: String,
  event_id: String,
  attendee_id: String,
  year: String,
  january: String,
  february: String,
  march: String,
  april: String,
  may: String,
  june: String,
  july: String,
  august: String,
  september: String,
  october: String,
  november: String,
  december: String
}
```
