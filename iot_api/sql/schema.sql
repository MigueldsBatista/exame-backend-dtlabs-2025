create database exame_backend;

use exame_backend;


create table user(
    id int not null primary key auto_increment,
    username varchar(255) not null,
    password varchar(255) not null
);

create table server(
	id char(26) not null primary key, -- A criação do ULID do servidor deve ser feita pelo backend
    server_name varchar(255) not null
);

create table reading(
id int not null primary key auto_increment,
server_ulid char(26) not null,
timestamp_ms timestamp not null,
temperature decimal(4, 1),
humidity decimal(4, 1),
voltage decimal(4, 1),
`current` decimal(4, 1),
foreign key(server_ulid) references server(id)
);

alter table reading
	add constraint has_any_reading check (
		(humidity is not null and humidity > 0 and reading.humidity <= 100) OR
        (temperature is not null) OR
		(voltage is not null and voltage >=0) or
        (current is not null and current >=0)
);


