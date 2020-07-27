# Copyrights rostepifanov.ru
#   Author: Epifanov Rostislav
#   Created: 21/07/2020

import os
import time
import click
import logging as log
import pandas as pd


from json import loads
from pathlib import Path
from requests import get


config = {}

class VkAPIError(Exception):
    pass

def load_user_info(user_idx):
    args = { 'user_ids': user_idx, 
             'fields': 'sex' }

    user = send_request('users.get', args) 

    user_sex = user[0]['sex']
    return 'male' if user_sex == 2 else 'female'

def load_group(domain):
    group_data = list()

    posts = load_posts(domain)

    for idx in range(config['POST_COUNT']):
        post_text, idxes = parse_post(posts, idx)

        comments = load_comments(idxes)

        for comment in comments['items']:
            for message in comment['thread']['items']:
                try:
                    message_text = message['text']

                    user_sex = load_user_info(message['from_id'])
                    link = config['VK_LINK'].format(domain, *idxes)

                    line = (link, post_text, message_text, user_sex)
                    group_data.append(line)
                except Exception as err:
                    config['LOGGER'].error(err)

    return group_data

def store_data(data):
    formatted_data = pd.DataFrame(data, columns=['source', 'text', 'message', 'sex'])

    formatted_data.to_csv(config['DATA_PATH'])

def load_posts(domain):
    args = { 'domain': domain, 
             'count': config['POST_COUNT'] }

    posts = send_request('wall.get', args) 

    return posts

def parse_post(posts, idx):
    text = posts['items'][idx]['text'][:config['POST_TEXT_SIZE']]
    owner_idx = posts['items'][idx]['owner_id']
    post_idx = posts['items'][idx]['id']

    return text, (owner_idx, post_idx)

def load_comments(idxes):
    args = { 'owner_id': idxes[0], 
             'post_id': idxes[1],
             'count': config['COMMENT_COUNT'],
             'thread_items_count': 10 }

    comments = send_request('wall.getComments', args)

    return comments

def send_request(method, args):
    args['v'] = config['VK_API_VERSION']
    args['access_token'] = os.getenv(config['VK_TOKEN_KEY'])

    if config['REQUEST_LATENCY']:
        time.sleep(config['REQUEST_LATENCY_PERIOD'])

    response = get(config['VK_API_GATEWAY'].format(method), args)

    parsed_response = loads(response.text)

    if 'response' in parsed_response.keys():
        return parsed_response['response']
    else:
        msg = parsed_response['error']['error_msg']
        raise VkAPIError(msg)

def init_global_config(**kwargs):
    for key, value in kwargs.items():
        config[key.upper()] = value

    config['VK_API_GATEWAY'] = 'https://api.vk.com/method/{}'
    config['VK_LINK'] = 'vk.com/{}?w=wall{}_{}'

    config['RESOURCES'] = config['RESOURCES'].split(',')

    if config['COMMENT_COUNT'] < 0:
        config['COMMENT_COUNT'] = 0
    elif config['COMMENT_COUNT'] > 100:
        config['COMMENT_COUNT'] = 100

def init_logging():
    config['LOGGER'] = log.getLogger(__name__)

    filepath = Path(__file__)
    logpath = filepath.stem + '.log'

    filehandler = log.FileHandler(logpath)
    filehandler.setLevel(log.INFO)

    formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler.setFormatter(formatter)

    config['LOGGER'].addHandler(filehandler)

@click.command()
@click.option('--vk_api_version', '-api', type=str, default='5.91')
@click.option('--vk_token_key', '-tk', type=str, default='VK_TOKEN_KEY')
@click.option('--resources', '-r', type=str, default='')
@click.option('--request_latency', '-rl', is_flag=True)
@click.option('--request_latency_period', '-rlp', type=float, default=0.1)
@click.option('--post_count', '-pc', type=int, default=100)
@click.option('--post_text_size', '-pts', type=int, default=280)
@click.option('--comment_count', '-cc', type=int, default=100)
@click.option('--data_path', '-dp', type=str, default='dump.csv')
def main(**kwargs):
    init_global_config(**kwargs)
    init_logging()

    data = list()

    for domain in config['RESOURCES']:
        try:
            config['LOGGER'].info(f'Start loading of {domain}')
            group_data = load_group(domain)
            data.extend(group_data)

            config['LOGGER'].info(f'Data has been loaded from {domain}')
        except Exception as err:
            config['LOGGER'].error(err)

    store_data(data)

if __name__ == '__main__':
    main()
