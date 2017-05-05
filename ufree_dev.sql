CREATE TABLE availability (
    id integer SERIAL NOT NULL PRIMARY KEY,
    attendee_id integer NOT NULL,
    event_id integer NOT NULL,
    year date,
    january string,
    february string,
    march string,
    april string,
    may string,
    june string,
    july string,
    august string,
    september string,
    october string,
    november string,
    december string
);

CREATE TABLE attendee (
  id integer SERIAL NOT NULL PRIMARY KEY,
  name character NOT NULL,
  event_id character NOT NULL,
  joined_date date,
  email character
)

CREATE TABLE events (
    id character NOT NULL,
    name character varying(30) NOT NULL,
    creator_id integer NOT NULL,
    created_date date
);
