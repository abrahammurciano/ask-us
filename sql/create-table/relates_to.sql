create table relates_to(
	question_id references questions(post_id),
	topic_id references topics(id),
	primary key (question_id, topic_id)
);