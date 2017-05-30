# TODO
* ~~Design Dao test framework~~
* ~~Move utils classes to a Utils folder~~
* ApiValidator methods for Attendee fields
** refactor validator to rely on exceptions
* Create service layer for Event/Attendees
* create base exception class

# Request Object
```
{
  user_id: '',
  token: '',
  payload: {
    // an event, availability, or user object
  }
}
```
