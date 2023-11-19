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
create table items(
    item_id      int,
    item_name   text,
    store_id     int, 
    primary key (item_id),
    foreign key (store_id) references stores
);

