create table follows(
	user_id references users(id),
	topic_id references topics(id),
	primary key (user_id, topic_id)
);