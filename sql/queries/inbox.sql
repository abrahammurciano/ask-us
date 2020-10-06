(select 'A' post_type, q.title subject, to_char(substr(a.body, 1, 100)) preview, a.timestamp
from answers a inner join questions q on a.question_id=q.post_id
where q.author_id = 28)
union
(select 'CQ' post_type, q.title, to_char(substr(c.body, 1, 100)) preview, c.timestamp
from comments c inner join questions q on c.parent_post_id=q.post_id
where q.author_id = 28)
union
(select 'CA' post_type, to_char(substr(a.body, 1, 20)) subject, to_char(substr(c.body, 1, 100)) preview, c.timestamp
from comments c inner join answers a on c.parent_post_id=a.post_id
where a.author_id = 28)
union
(select 'CC' post_type, to_char(substr(p.body, 1, 20)) subject, to_char(substr(c.body, 1, 100)) preview, c.tumestamp
from comments c inner join comments p on c.parent_post_id=p.post_id
where p.author_id = 28)
