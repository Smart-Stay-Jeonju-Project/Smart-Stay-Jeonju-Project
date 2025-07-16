use ateam_project1;

create table accommodations(
	aNo int primary key auto_increment,
	name varchar(50) not null,
	category varchar(50) not null,
    address varchar(200) not null,
	aRating int default 0,
	image varchar(100) not null,
	feature varchar(20),
	score int default 0,
	aiReport longtext
);

DESCRIBE `accommodations`;

create table review(
	rNo int primary key auto_increment,
	review_text longtext not null,
	write_date datetime,
	rRating int not null default 0,
    foreign key (aNo) references accommodations(aNo)
);

create table keyword(
	kNo int primary key auto_increment,
	count int not null default 0,
	keyword_text longtext not null,
	foreign key (aNo) references accommodations(aNo)
);