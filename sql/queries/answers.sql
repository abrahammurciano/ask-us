select body, points, accepted, timestamp
from answers
where question_id = 1
order by points desc;