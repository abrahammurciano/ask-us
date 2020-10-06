select body, points, timestamp
from comments
where parent_post_id = 1
order by points desc;