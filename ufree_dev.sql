CREATE TABLE availability (
    id SERIAL NOT NULL PRIMARY KEY,
    attendee_id integer NOT NULL,
    event_id varchar NOT NULL,
    year date,
    january varchar(31),
    february varchar(29),
    march varchar(31),
    april varchar(30),
    may varchar(31),
    june varchar(30),
    july varchar(31),
    august varchar(31),
    september varchar(30),
    october varchar(31),
    november varchar(30),
    december varchar(31)
);

CREATE TABLE attendee (
  id SERIAL NOT NULL PRIMARY KEY,
  name varchar(15) NOT NULL,
  email varchar(50)
);

CREATE TABLE event (
  id varchar NOT NULL,
  name varchar(20) NOT NULL,
  creator_id integer NOT NULL,
  created_date date
);

CREATE TABLE event_attendee (
  id SERIAL NOT NULL PRIMARY KEY,
  event_id INTEGER REFERENCES event (id),
  attendee_id INTEGER REFERENCES attendee (id),
);
