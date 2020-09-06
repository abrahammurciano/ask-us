create table votes(
	user_id references users(id),
	post_id references posts(id),
	primary key (user_id, post_id)
);