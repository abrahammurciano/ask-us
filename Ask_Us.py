# encoding=utf-8
from PyInquirer import prompt
import sqlite3

def enter_username():
    username_prompt = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter your username'
        }
    ]
    return prompt(username_prompt)['username']

#fill in
def valid_username(username):
    # query database
    return True

def enter_password():
    password_prompt = [
        {
            'type': 'password',
            'name': 'password',
            'message': 'Enter your password'
        }
    ]
    return prompt(password_prompt)['password']

#fill in
def correct_password(username, password):
    # query database
    return True

#fill in
def filter_input(input):
    # make sure keywords safe for sql
    return input

#fill in
def get_your_topics(username):
    # query database, return list of topics
    return []

#fill in
def get_questions_keyword():
    search = [
        {
            'type': 'input',
            'name': 'search',
            'message': 'What would you like to search for?',
            'filter': filter_input
        }
    ]
    word = prompt(search)
    # query database...

#fill in
def get_questions_topic(username):
    topics = get_your_topics(username)
    topic_prompt = [
        {
            'type': 'list',
            'name': 'topics',
            'message': 'What topic would you like to retrieve questions from?',
            'choices': topics
        }
    ]
    topic = prompt(topic_prompt)
    # query database...

#fill in
def get_unanswered_questions(username):
    topics = get_your_topics(username)
    topic_prompt = [
        {
            'type': 'list',
            'name': 'topics',
            'message': 'What topic would you like to retrieve questions from?',
            'choices': topics
        }
    ]
    topic = prompt(topic_prompt)
    # query database...

#fill in
def get_answers_to_you(username):
    # query database
    print()

#fill in
def get_your_posts(username):
    # query database
    print()

#fill in
def get_topics():
    # query database...
    return []

#fill in
def follow_topics(username):
    topics = get_topics()
    def generate_choices(all_topics, my_topics):
        choices = []
        for topic in all_topics:
            if topic in my_topics:
                choices.append({'name':topic,'checked':True})
            else:
                choices.append(topic)
    choices = generate_choices(topics, get_your_topics(username))
    browse_topics = [
        {
            'type': 'checkbox',
            'name': 'topics',
            'message': 'Select which topics to follow:',
            'choices': choices,
        }
    ]
    answers = prompt(browse_topics)
    # follow and unfollow in database

def main_menu(username):
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
                '6- Browse and follow new topics',
                '0- Sign out'
            ]
        }
    ]
    command = prompt(menu)

    if command['command'][0] == '1':
        get_questions_keyword()
    elif command['command'][0] == '2':
        get_questions_topic(username)
    elif command['command'][0] == '3':
        get_unanswered_questions(username)
    elif command['command'][0] == '4':
        get_answers_to_you(username)
    elif command['command'][0] == '5':
        get_your_posts(username)
    elif command['command'][0] == '6':
        follow_topics(username)
    else: # command['command'][0] == '0' exit...
        return

    main_menu(username)


if __name__ == "__main__":
    username = enter_username()
    while not valid_username(username):
        print("invalid username")
        username = enter_username()

    password = enter_password()
    while not correct_password(username, password):
        print("incorrect password")
        password = enter_password()

    main_menu(username)
