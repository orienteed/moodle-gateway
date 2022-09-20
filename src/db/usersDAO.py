from datetime import datetime
from fastapi import Query
from .agent import Agent
import uuid


class usersDAO:
    def get_user_data_by_magento_token(magento_token):
        agent = Agent()
        query = f"SELECT id, username, magento_token, moodle_token, last_use_date FROM users WHERE magento_token = '{magento_token}'"
        try:
            result = agent.read(query)
            return result
        except Exception as e:
            print('get_user_data_by_magento_token: ' + str(e))

    def get_user_data_by_username(username):
        agent = Agent()
        query = f"SELECT id, username, magento_token, moodle_token, last_use_date FROM users WHERE username = '{username}'"
        try:
            result = agent.read(query)
            return result
        except Exception as e:
            print('get_user_data_by_username: ' + str(e))

    def get_user_data_by_username_and_token(username, magento_token):
        agent = Agent()
        query = f"SELECT username, magento_token, moodle_token last_use_date FROM users WHERE username = '{username}' OR magento_token = '{magento_token}'"
        try:
            result = agent.read(query)
            return result
        except Exception as e:
            print('get_user_data_by_username_and_token: ' + str(e))

    def update_user_data(username, magento_token):
        agent = Agent()
        query = f"UPDATE users SET magento_token = '{magento_token}', last_use_date = '{datetime.now()}' WHERE username = '{username}'"
        try:
            result = agent.update(query)
            return result
        except Exception as e:
            print('update_user_data: ' + str(e))

    def update_token_date(magento_token):
        agent = Agent()
        query = f"UPDATE users SET last_use_date = '{datetime.now()}' WHERE magento_token = '{magento_token}'"
        try:
            result = agent.update(query)
            return result
        except Exception as e:
            print('update_token_date: ' + str(e))

    def create_user(id, username, magento_token, moodle_token):
        agent = Agent()
        query = f"INSERT INTO users (id, username, magento_token, moodle_token, last_use_date) VALUES ('{id}','{username}', '{magento_token}', '{moodle_token}', '{datetime.now()}')"
        try:
            result = agent.create(query)
            return result
        except Exception as e:
            print('create_user: ' + str(e))

    def create_and_update_user(id, username, magento_token, moodle_token):
        agent = Agent()
        query = f"INSERT INTO users (id, username, magento_token, moodle_token, last_use_date) VALUES ('{id}','{username}', '{magento_token}', '{moodle_token}', '{datetime.now()}') ON CONFLICT(id) DO UPDATE SET magento_token='{magento_token}', moodle_token='{moodle_token}', last_use_date='{datetime.now()}'"
        try:
            result = agent.create(query)
            return result
        except Exception as e:
            print('create_and_update_user: ' + str(e))

    def remove_token_by_token(magento_token):
        agent = Agent()
        query = f"UPDATE users SET magento_token = '' WHERE magento_token = '{magento_token}'"
        try:
            result = agent.update(query)
            return result
        except Exception as e:
            print('remove_token_by_token: ' + str(e))
