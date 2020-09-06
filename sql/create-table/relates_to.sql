create table relates_to(
	post_id references posts(id),
	topic_id references topics(id),
	primary key (post_id, topic_id)
);