DROP TABLE if EXISTS user;

CREATE TABLE user(
  id integer primary key autoincrement ,
  title text,
  username text,
  email text,
  password text,
  real_name text
)
