select body, points, timestamp
from comments
where parent_post_id = 100
order by points desc;