select *
from questions
where lower(questions.title) like lower('%search phrase%')
	or lower(questions.body) like lower('%search phrase%')
order by points desc;