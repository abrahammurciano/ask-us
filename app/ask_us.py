# encoding=utf-8
from PyInquirer import prompt
import sqlite3
from pprint import pprint
from hashlib import sha256
import base64
from typing import Tuple
import re

connection = sqlite3.connect('app/ask_us.db')
user = None

# prompts for username and password and returns a tuple (id: int, username: str)
def login() -> Tuple[int, str]:
	while True:
		username = enter_username()
		if get_user_id(username) is None:
			signup_prompt = [
				{
					'type': 'confirm',
					'message': 'User does not exist. Create account?',
					'name': 'signup',
					'default': True,
				}
			]
			if prompt(signup_prompt)['signup']:
				return signup(username)
			continue

		password = enter_password()
		if not correct_password(username, password):
			print("incorrect password")
			continue

		break
	return get_user_data(username)

def signup(username: str) -> Tuple[int, str]:
	while True:
		password = enter_password()
		if (password == enter_password('Repeat password')):
			break
		print("Passwords do not match")
	hashed_pass = hash_password(password)
	email = enter_email()
	cursor = connection.cursor()
	cursor.execute("insert into users (username, email, password) values (?, ?, ?)", (username, email, hashed_pass))
	connection.commit()
	user_id = get_user_id(username)
	return (user_id, username) if user_id is not None else None

def enter_username(message = 'Enter username'):
	username_prompt = [
		{
			'type': 'input',
			'name': 'username',
			'message': message
		}
	]
	return prompt(username_prompt)['username']

# Returns id of username provided, or None if user does not exist
def get_user_id(username: str) -> int:
	cursor = connection.cursor()
	cursor.execute("select id from users where username = ?", (username,))
	user_id = cursor.fetchone()
	return user_id[0] if user_id else None

def enter_password(message = 'Enter password'):
	password_prompt = [
		{
			'type': 'password',
			'name': 'password',
			'message': message,
			'validate': lambda password: len(password) >= 8 or "Password must be at least 8 characters"
		}
	]
	return prompt(password_prompt)['password']

def enter_email(message = 'Enter email'):
	email_prompt = [
		{
			'type': 'input',
			'name': 'email',
			'message': message,
			'validate': lambda email: True if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) else "Invalid email"
		}
	]
	return prompt(email_prompt)['email']

def hash_password(password: str) -> str:
	return base64.b64encode(sha256(password.encode()).digest()).decode('ascii')[:43]

def correct_password(username, password):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username = ? and password = ?", (username, hash_password(password)))
	user_ = cursor.fetchone()
	if user_:
		return True
	else:
		return False

def get_user_data(username):
	cursor = connection.cursor()
	cursor.execute("select id, username from users where username = ?", (username,))
	return cursor.fetchone()

def present_questions(questions):
	titles = []
	for question in questions:
		titles.append(question[1])
	qs = [
		{
			'type': 'list',
			'name': 'question',
			'message': 'Questions found, select one to continue:',
			'choices': titles
		}
	]
	question = prompt(qs)
	for i, q in enumerate(questions):
		if q[1] in question:
			break
	display_question(questions[i])

def display_question(question):
	print("QUESTION:")
	pprint(question)
	cursor = connection.cursor()
	cursor.execute("""
		select body, points, timestamp
		from comments
		where parent_post_id = ?
		order by points desc
	""", (question[0],))
	print("COMMENTS:")
	pprint(cursor.fetchall())
	cursor2 = connection.cursor()
	cursor.execute("""
		select body, points, accepted, timestamp
		from answers
		where question_id = ?
		order by points desc
	""", (question[0],))
	print("ANSWERS:")
	pprint(cursor2.fetchall())

def get_questions_keyword():
	search = [
		{
			'type': 'input',
			'name': 'search',
			'message': 'What would you like to search for?',
		}
	]
	word = prompt(search)
	cursor = connection.cursor()
	cursor.execute("""
		select *
		from questions
		where lower(questions.title) like lower('%'||?||'%') or lower(questions.body) like lower('%'||?||'%')
		order by points desc
		""", (word['search'], word['search']))
	questions = cursor.fetchall()
	present_questions(questions)


def get_questions_topic():
	cursor = connection.cursor()
	cursor.execute("""
		select *
		from questions q
		where exists (
				select topic_id from follows
				where user_id = ?
				intersect
				select topic_id from relates_to
				where question_id = q.post_id
			)
		order by points desc
		limit 10
		""", (user[0],))
	questions = cursor.fetchall()
	if not questions:
		print("you do not follow any topics")
		return
	present_questions(questions)

#fill in
def get_unanswered_questions():
	cursor = connection.cursor()
	cursor.execute("""
			select * from (
				select *
				from questions q
				where exists (
					select topic_id from follows
					where user_id = ?
					intersect
					select topic_id from relates_to
					where question_id = q.post_id
				) and not exists (
					select post_id from answers
					where question_id = q.post_id
				)
			)
			order by timestamp desc
			limit 10
			""", (user[0],))
	questions = cursor.fetchall()
	if not questions:
		print("you do not follow any topics")
		return
	present_questions(questions)

#fill in
def get_answers_to_you():
	cursor = connection.cursor()
	cursor.execute("""
		select * from (
				select
					q.title subject,
					substr(a.body, 1, 100) preview,
					a.timestamp
				from
					answers a
					inner join questions q
					on a.question_id = q.post_id
				where
					q.author_id = ?
			union
				select
					q.title,
					substr(c.body, 1, 100) preview,
					c.timestamp
				from
					comments c
					inner join questions q
					on c.parent_post_id = q.post_id
				where
					q.author_id = ?
			union
				select
					substr(a.body, 1, 20) subject,
					substr(c.body, 1, 100) preview,
					c.timestamp
				from
					comments c
					inner join answers a
					on c.parent_post_id=a.post_id
				where
					a.author_id = ?
			union
				select
					substr(p.body, 1, 20) subject,
					substr(c.body, 1, 100) preview,
					c.timestamp
				from
					comments c
					inner join comments p
					on c.parent_post_id=p.post_id
				where
					p.author_id = ?
		) order by timestamp desc
		""", (user[0], user[0], user[0], user[0]))
	pprint(cursor.fetchall())


def get_your_posts():
	cursor = connection.cursor()
	cursor.execute("""
		select * from (
			select title, points, timestamp
			from questions
			where author_id = ?
			union
			select substr(body, 1, 4000), points, timestamp
			from answers
			where author_id = ?
			union
			select substr(body, 1, 4000), points, timestamp
			from comments
			where author_id = ?
		) order by timestamp desc;
		""", (user[0], user[0], user[0]))
	pprint(cursor.fetchall())

def existing_topic(topic):
	cursor = connection.cursor()
	cursor.execute("select id from topics where label = ?", (topic,))
	topic_ = cursor.fetchone()
	return topic_

#fill in
def ask_question():
	# see if we can do checkbox of topics
	questions = [
		{
			'type': 'input',
			'name': 'topic',
			'message': 'What topic does your question relate to?'
		},
		{
			'type': 'input',
			'name': 'title',
			'message': 'Enter a title:'
		},
		{
			'type': 'input',
			'name': 'body',
			'message': 'What is your question?'
		}
	]
	answers = prompt(questions)
	topic_id = existing_topic(answers['topic'])
	if not topic_id:
		print("cannot use topic that doesnt exist")
		return
	cursor = connection.cursor()
	cursor.execute("insert into posts default values")
	cursor.execute("select id from posts where rowid = ?", (cursor.lastrowid,))
	post_id = cursor.fetchone()[0]
	cursor.execute("""
	insert into questions(post_id, title, body, author_id)
	values(?,?,?,?)
	""", (post_id, answers['title'], answers['body'], user[0]))
	cursor.execute("insert into relates_to(question_id, topic_id) values(?,?)", (post_id, topic_id[0]))


def main_menu():
	menu = [
		{
			'type': 'list',
			'name': 'command',
			'message': 'What would you like to see?',
			'choices': [
				'1- Obtain all questions whose title or body contain keywords',
				'2- Retrieve the most popular questions which relate to a topic you follow',
				'3- Retrieve the newest unanswered questions which relate to a topic you follow',
				'4- Obtain all answers to questions as well as all comments to posts which were posted by you, sorted from newest to oldest',
				'5- Retrieve all questions, answers, and comments you authored, sorted by newest first',
				'6- Ask a question',
				'0- Sign out'
			]
		}
	]
	command = prompt(menu)

	if command['command'][0] == '1':
		get_questions_keyword()
	elif command['command'][0] == '2':
		get_questions_topic()
	elif command['command'][0] == '3':
		get_unanswered_questions()
	elif command['command'][0] == '4':
		get_answers_to_you()
	elif command['command'][0] == '5':
		get_your_posts()
	elif command['command'][0] == '6':
		ask_question()
	else: # command['command'][0] == '0' exit...
		return

	main_menu()

if __name__ == "__main__":
	user = login()

	main_menu()

	connection.close()
