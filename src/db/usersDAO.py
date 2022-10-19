from .agent import Agent
from datetime import datetime
from logs.setup import logger
import threading

lock = threading.Lock()


class UsersDAO:
    def get_user_data_by_magento_token(magento_token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"SELECT id, username, magento_token, moodle_token, last_use_date FROM users WHERE magento_token = '{magento_token}'"
            try:
                return agent.read(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: get_user_data_by_magento_token", exc_info=1)
        finally:
            lock.release()

    def get_user_data_by_username(username):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"SELECT id, username, magento_token, moodle_token, last_use_date FROM users WHERE username = '{username}'"
            try:
                return agent.read(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: get_user_data_by_username", exc_info=1)
        finally:
            lock.release()

    def update_user_data(username, magento_token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"UPDATE users SET magento_token = '{magento_token}', last_use_date = '{datetime.now()}' WHERE username = '{username}'"
            try:
                return agent.update(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: update_user_data", exc_info=1)
        finally:
            lock.release()

    def update_username_by_id(username, id):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"UPDATE users SET username = '{username}' WHERE id = '{id}'"
            try:
                return agent.update(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: update_user_email_by_id", exc_info=1)
        finally:
            lock.release()

    def update_moodle_token_by_id(moodle_token, id):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"UPDATE users SET moodle_token = '{moodle_token}' WHERE id = '{id}'"
            try:
                return agent.update(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: update_moodle_token_by_id", exc_info=1)
        finally:
            lock.release()

    def update_token_date(magento_token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"UPDATE users SET last_use_date = '{datetime.now()}' WHERE magento_token = '{magento_token}'"
            try:
                return agent.update(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: update_token_date", exc_info=1)
        finally:
            lock.release()

    def create_user(id, username, magento_token, moodle_token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"INSERT INTO users (id, username, magento_token, moodle_token, last_use_date) VALUES ('{id}','{username}', '{magento_token}', '{moodle_token}', '{datetime.now()}')"
            try:
                return agent.create(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: create_user", exc_info=1)
        finally:
            lock.release()

    def create_and_update_user(id, username, magento_token, moodle_token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"INSERT INTO users (id, username, magento_token, moodle_token, last_use_date) VALUES ('{id}','{username}', '{magento_token}', '{moodle_token}', '{datetime.now()}') ON CONFLICT(id) DO UPDATE SET magento_token='{magento_token}', moodle_token='{moodle_token}', last_use_date='{datetime.now()}'"
            try:
                return agent.create(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: create_and_update_user", exc_info=1)
        finally:
            lock.release()

    def remove_token_by_token(magento_token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"UPDATE users SET magento_token = '' WHERE magento_token = '{magento_token}'"
            try:
                return agent.update(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: remove_token_by_token", exc_info=1)
        finally:
            lock.release()
