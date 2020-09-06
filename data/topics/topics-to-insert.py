from lorem.text import TextLorem

sql = open("../../sql/insert/insert_topics.sql", "w")

lorem = TextLorem(srange=(1,10))

with open("topics.txt") as topics:
	for topic in topics:
		while True:
			description = lorem.paragraph()
			if len(description) < 255:
				break
		sql.write("insert into topics (label, description) values ('" + topic[:-1].replace("'", "''") + "', '" + description + "');\n")

sql.close()