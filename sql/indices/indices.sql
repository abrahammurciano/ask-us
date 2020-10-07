create index index_questions_points on questions(points);
create index index_answers_points on answers(points);
create index index_comments_points on comments(points);

create index index_questions_timestamp on questions(timestamp);
create index index_answers_timestamp on answers(timestamp);
create index index_comments_timestamp on comments(timestamp);

create index index_questions_author_id on questions(author_id);
create index index_answers_author_id on answers(author_id);
create index index_comments_author_id on comments(author_id);