# encoding=utf-8
from PyInquirer import prompt
import sqlite3
from pprint import pprint
from hashlib import sha256
import base64
from typing import Tuple
import re
from tabulate import tabulate
import os

connection = sqlite3.connect('app/ask_us.db')
user = None		# tuple (id: int, username: str)


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
			print('incorrect password')
			continue

		break
	return get_user_data(username)


def signup(username: str) -> Tuple[int, str]:
	while True:
		password = enter_password()
		if (password == enter_password('Repeat password')):
			break
		print('Passwords do not match')
	hashed_pass = hash_password(password)
	email = enter_email()
	cursor = connection.cursor()
	cursor.execute('insert into users (username, email, password) values (?, ?, ?)', (username, email, hashed_pass))
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
	cursor.execute('select id from users where username = ?', (username,))
	user_id = cursor.fetchone()
	return user_id[0] if user_id else None


def enter_password(message = 'Enter password'):
	password_prompt = [
		{
			'type': 'password',
			'name': 'password',
			'message': message,
			'validate': lambda password: len(password) >= 8 or 'Password must be at least 8 characters'
		}
	]
	return prompt(password_prompt)['password']


def enter_email(message = 'Enter email'):
	email_prompt = [
		{
			'type': 'input',
			'name': 'email',
			'message': message,
			'validate': lambda email: True if re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email) else 'Invalid email'
		}
	]
	return prompt(email_prompt)['email']


def hash_password(password: str) -> str:
	return base64.b64encode(sha256(password.encode()).digest()).decode('ascii')[:43]


def correct_password(username, password):
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM users WHERE username = ? and password = ?', (username, hash_password(password)))
	user_ = cursor.fetchone()
	if user_:
		return True
	else:
		return False


def get_user_data(username):
	cursor = connection.cursor()
	cursor.execute('select id, username from users where username = ?', (username,))
	return cursor.fetchone()


# Takes a list of tuples (each tuple is a question) and asks user to choose one
def present_questions(questions):
	qs = [
		{
			'type': 'list',
			'name': 'question',
			'message': 'Questions found, select one to continue:',
			'choices': map(lambda q: str(q[0]) + ' - ' + q[1], questions),
			'filter': lambda choice: int(choice.split(' - ')[0])
		}
	]
	display_question(prompt(qs)['question'])


def html_strip(html: str) -> str:
	return re.sub('<[^<]+?>', '', html)


# Takes a quesion id and prints it, with its answers, and all comments
def display_question(q_id: int):
	cursor = connection.cursor()
	cursor.execute("""
		select q.title, q.body, q.points, u.username, q.timestamp
		from questions q inner join users u on q.author_id = u.id
		where q.post_id = ?
	""", (q_id,))
	question = cursor.fetchone()

	clear()
	print('QUESTION')
	print_question(q_id, question[0], question[1], question[2], question[3], question[4])
	print('--------------------')
	display_comments(q_id)
	print('====================')
	display_answers(q_id)
	question_menu(q_id)


def clear():
    os.system('cls' if os.name=='nt' else 'clear')


# prints a single question
def print_question(id: int, title: str, body: str, points: int, username: str, timestamp: str):
	print(tabulate([[title]], tablefmt='grid'))
	print(html_strip(body))
	print('~ ID ' + str(id), username, str(points) + ' pts', timestamp, sep=' | ')


# displays comments (recursively) for a given post, returning the number of comments
def display_comments(post_id: int, indent: int = 1, indent_block: str = ' ' * 4, n_comments = 0) -> int:
	cursor = connection.cursor()
	cursor.execute("""
		select c.post_id, c.body, c.points, u.username, c.timestamp
		from comments c inner join users u on c.author_id = u.id
		where parent_post_id = ?
		order by c.points desc
	""", (post_id,))
	comments = cursor.fetchall()
	if not comments:
		if n_comments == 0:
			print('Wow, such empty!')
		return n_comments
	for comment in comments:
		n_comments += 1
		print_comment(comment[0], comment[1], comment[2], comment[3], comment[4], indent_block * indent)
		n_comments = display_comments(comment[0], indent + 1, n_comments = n_comments)
	return n_comments


# prints a single comment
def print_comment(id: int, body: str, points: int, username: str, timestamp: str, indent_str: str):
	print(indent_str + body)
	print(indent_str + '~ ID ' + str(id), username, str(points) + ' pts', timestamp, sep=' | ')


# display all answers to a given question
def display_answers(q_id: int):
	cursor = connection.cursor()
	cursor.execute("""
		select a.post_id, a.body, a.points, u.username, a.timestamp, a.accepted
		from answers a inner join users u on a.author_id = u.id
		where question_id = ?
		order by a.points desc;
	""", (q_id,))
	for answer in cursor.fetchall():
		print('\nANSWER')
		print_answer(answer[0], answer[1], answer[2], answer[3], answer[4], answer[5] != 0)
		print('--------------------')
		display_comments(answer[0])
		print('====================')


def print_answer(id: int, body: str, points: int, username: str, timestamp: str, accepted: bool):
	print(body)
	print('~ ID ' + str(id), username, ('Accepted, ' if accepted else '') + str(points) + ' pts', timestamp, sep = ' | ')


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
		print('you do not follow any topics')
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
		print('you do not follow any topics')
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
	cursor.execute('select id from topics where label = ?', (topic,))
	topic_ = cursor.fetchone()
	return topic_


#fill in
def ask_question():
	topic_ids = search_topics()
	questions = [
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
	if not topic_ids:
		print('Question must be related to at least one topic')
		return
	post_id = create_post()
	cursor = connection.cursor()
	cursor.execute("""
	insert into questions(post_id, title, body, author_id)
	values(?,?,?,?)
	""", (post_id, answers['title'], answers['body'], user[0]))
	relates_to_insert = []
	for id in topic_ids:
		relates_to_insert.append((post_id,id))
	cursor.executemany('insert into relates_to(question_id, topic_id) values(?,?)', relates_to_insert)
	connection.commit()


# inserts row into posts table, and returns the ID inserted
def create_post() -> int:
	cursor = connection.cursor()
	cursor.execute('insert into posts default values')
	connection.commit()
	cursor.execute('select id from posts where rowid = ?', (cursor.lastrowid,))
	return cursor.fetchone()[0]


def question_menu(q_id):
	menu = [
		{
			'type': 'list',
			'name': 'command',
			'message': 'What would you like to do?',
			'choices': [
				'1 - Vote for the question, an answer, or a comment',
				'2 - Answer the question',
				'3 - Write a comment on the question, an answer, or a comment',
				'0 - Main menu'
			],
			'filter': lambda choice: int(choice.split(' - ')[0])
		}
	]
	command = prompt(menu)

	if command['command'] == 1:
		cast_vote()
	elif command['command'] == 2:
		add_answer(q_id)
	elif command['command'] == 3:
		add_comment()
	elif command['command'] == 0:
		return
	display_question(q_id)

def cast_vote():
	menu = [
		{
			'type': 'input',
			'name': 'post_id',
			'message': 'Enter the ID of the post you want to vote for',
			'validate': lambda id: id.isdigit() or 'ID must be a number',
			'filter': lambda id: int(id)
		}
	]
	id = prompt(menu)['post_id']
	cursor = connection.cursor()
	try:
		cursor.execute('insert into votes (user_id, post_id) values (?, ?)', (user[0], id))
	except sqlite3.IntegrityError as e:
		print("Error: You have already voted on this post")
	else:
		cursor.execute("""
			update users set points = points + 1
			where id = (select author_id from all_posts where id = ?)
		""", (id,))
		cursor.execute('update questions set points = points + 1 where post_id = ?', (id,))
		cursor.execute('update answers set points = points + 1 where post_id = ?', (id,))
		cursor.execute('update comments set points = points + 1 where post_id = ?', (id,))
		connection.commit()


def add_answer(q_id: int):
	menu = [
		{
			'type': 'input',
			'name': 'answer',
			'message': 'Type your answer'
		}
	]
	answer = prompt(menu)['answer']
	cursor = connection.cursor()
	cursor.execute('insert into answers (post_id, question_id, body, author_id) values (?, ?, ?, ?)', (create_post(), q_id, answer, user[0]))
	connection.commit()


def add_comment():
	menu = [
		{
			'type': 'input',
			'name': 'parent_post_id',
			'message': 'Enter the ID of the post you want to comment under',
			'validate': lambda id: id.isdigit() or 'ID must be a number',
			'filter': lambda id: int(id)
		},
		{
			'type': 'input',
			'name': 'body',
			'message': 'Type your comment'
		}
	]
	answers = prompt(menu)
	cursor = connection.cursor()
	cursor.execute('insert into comments (post_id, parent_post_id, body, author_id) values (?, ?, ?, ?)', (create_post(), answers['parent_post_id'], answers['body'], user[0]))
	connection.commit()

def search_topics(topic_ids = []):
	# get user input for what topics he would like
	topic_search = [
		{
			'type': 'input',
			'name': 'topic',
			'message': 'What would you like to search for?'
		}
	]
	topic = prompt(topic_search)['topic']
	# query database for topics related to his search
	cursor = connection.cursor()
	cursor.execute("""
			select id, label
			from topics
			where lower(label) like lower('%'||?||'%') or lower(description) like lower('%'||?||'%')
			""", (topic, topic))
	topics = cursor.fetchall()
	# create list of choices for checkbox
	choices = []
	for topic in topics:
		choices.append({'name':topic[1]})
	topics_checkbox = [
		{
			'type': 'checkbox',
			'name': 'topics',
			'message': 'Choose topics:',
			'choices': choices
		}
	]
	answers = prompt(topics_checkbox)['topics']
	for topic in topics:
		if topic[1] in answers:
			topic_ids.append(topic[0])
	continue_search = [
		{
			'type': 'confirm',
			'message': 'Continue to search?',
			'name': 'search',
			'default': False,
		}
	]
	if prompt(continue_search)['search']:
		search_topics(topic_ids)
	return topic_ids

def follow_topics():
	topics = search_topics()
	cursor = connection.cursor()
	for topic in topics:
		cursor.execute('insert into follows (user_id, topic_id) values (?, ?)', (user[0], topic))
	connection.commit()

def main_menu():
	menu = [
		{
			'type': 'list',
			'name': 'command',
			'message': 'What would you like to see?',
			'choices': [
				'1 - Obtain all questions whose title or body contain keywords',
				'2 - Retrieve the most popular questions which relate to a topic you follow',
				'3 - Retrieve the newest unanswered questions which relate to a topic you follow',
				'4 - Obtain all answers to questions as well as all comments to posts which were posted by you, sorted from newest to oldest',
				'5 - Retrieve all questions, answers, and comments you authored, sorted by newest first',
				'6 - Ask a question',
				'7 - Browse topics',
				'0 - Sign out'
			],
			'filter': lambda choice: int(choice.split(' - ')[0])
		}
	]
	command = prompt(menu)

	if command['command'] == 1:
		get_questions_keyword()
	elif command['command'] == 2:
		get_questions_topic()
	elif command['command'] == 3:
		get_unanswered_questions()
	elif command['command'] == 4:
		get_answers_to_you()
	elif command['command'] == 5:
		get_your_posts()
	elif command['command'] == 6:
		ask_question()
	elif command['command'] == 7:
		follow_topics()
	else: # command['command'] == 0 exit...
		return

	main_menu()


if __name__ == '__main__':
	user = login()

	main_menu()

	connection.close()
