create table users
(
	account_id serial not null
		constraint users_pkey
			primary key,
	first_name varchar(200),
	last_name varchar(200),
	email varchar(100),
	password_hash varchar(1000)
)
;

create table questions
(
	question_id serial not null
		constraint questions_pkey
			primary key,
	question_subject varchar(256) not null,
	question_body varchar(100) not null,
	date_posted timestamp default now(),
	posted_by integer
		constraint questions_users_account_id_fk
			references users
				on update set null on delete set null
)
;

create table answers
(
	answer_id serial not null
		constraint answers_pkey
			primary key,
	question_id integer not null
		constraint answers_questions_question_id_fk
			references questions
				on delete cascade,
	answeres_by integer
		constraint answers_users_account_id_fk
			references users,
	answer_date timestamp default now(),
	answer varchar(1000),
	accepted boolean default false
)