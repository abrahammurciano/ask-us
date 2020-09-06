from lorem.text import TextLorem

# remove duplicate entries from the list of topics
with open("topics.txt", "w") as topics:
	lines_seen = set() # holds lines already seen
	for line in open("topics_w_dups.txt", "r"):
		if line not in lines_seen: # not a duplicate
			topics.write(line)
			lines_seen.add(line)

# make an insert statement for each topic
with open("topics.txt", "r") as topics:
	sql = open("../../sql/insert/insert_topics.sql", "w")
	lorem = TextLorem(srange=(4,16), prange=(2,16)) # 4-16 words/sentence, 2-16 sentences/paragraph
	for topic in topics:
		while True:
			description = lorem.paragraph()
			if len(description) <= 255: # make sure the description fits in the database
				break
		label = topic[:-1].replace("'", "''") # remove trailing \n and escape single quotes
		sql.write(
"""
insert into topics
	(label, description)
values
	('""" + label + "', '" + description + """');
"""
		)
	sql.close()