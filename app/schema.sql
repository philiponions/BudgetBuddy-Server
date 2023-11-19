-- Let's drop the users in case they exist from previous runs
drop table if exists users;
drop table if exists stores;
drop table if exists items;

create table users (
    username         text,
    password        text,
    primary key (username)
);
create table stores (
    store_id  int,
    name       text,
    username      text,
    primary key (store_id),
    foreign key (username) references users
);
CREATE TABLE items(
    item_id      INTEGER PRIMARY KEY,
    item_name    TEXT,
    store_id     INTEGER, 
    FOREIGN KEY (store_id) REFERENCES stores ON DELETE CASCADE
);

