# TODO
* ~~Design Dao test framework~~
* ~~Move utils classes to a Utils folder~~
* ~~ApiValidator methods for Attendee fields~~
* ~~create base exception class~~
* ~~load_attendees Dao method~~
* ~~builtins variable names. change other tests to use new fetchall pattern~~
* ~~test attendee dao methods~~
* ~~test user filter~~
* ~~test attendee validator~~
* ~~query to load events by attendee~~
* ~~DAO methods should use fetch one unless it is a many-type query~~
* ~~factory that provides DOAs and Services based on environment~~
* ~~abstract DAO to initialize psycopg2~~
* ~~wire provider to services~~
* ~~unified API for service methods. All should accept raw request.~~
* ~~finish testing event service~~
* ~~services should return a fully populated request object~~
* ~~finish AttendeeService~~
* ~~test AttendeeService~~
* ~~add rest of attendee methods to API~~
* ~~decide if all attendees will be unique.~~
* ~~yes, easier to pair users with their event availability.~~
  * ~~cookies will contain event id and attendee id pair~~
* ~~design availability mechanism~~
  * ~~new service? yes~~
  * ~~integrate with attendee service? no~~
* ~~availability validator w/ year mechanism~~
* ~~tabs to spaces~~
* ensure uniform structure in tests, services, and validators
* find way to test provider in production mode
* investigate __import__ vs importlib in DAOs
* Script to test DB load/save queries

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
* DELETE - deletes this attendee and removes it them from the event

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
