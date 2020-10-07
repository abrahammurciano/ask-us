select *
from questions
where lower(questions.title) like lower('%word%')
	or lower(questions.body) like lower('%word%')
order by points desc;