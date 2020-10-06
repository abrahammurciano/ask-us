select * from (
       select q.title, q.body question, a.body answer, a.points
       from questions q
       inner join answers a
       on q.post_id = a.question_id
       where a.post_id = (
             select * from (
                    select a2.post_id from answers a2
                    where a2.question_id = q.post_id
                    order by a2.points desc
             ) where rownum = 1
       )
       and q.timestamp >= sysdate - 7
       order by q.points desc
) where rownum <= 15
