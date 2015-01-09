CREATE TABLE IF NOT EXISTS staff_members (
  id integer primary key NOT NULL, 
  first_name char(200), 
  last_name char(200), 
  institution_name char(200), 
  region_name char(200)
);

CREATE TABLE IF NOT EXISTS nominations (
  id integer primary key NOT NULL,
  nominee_id integer,
  nominator_name text, 
  awesomeness text,
  FOREIGN KEY(nominee_id) REFERENCES staff_members(id)
); 