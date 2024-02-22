from flask import Flask
from flask_redis import FlaskRedis
from configs import Config
from datetime import datetime
import random

app = Flask(__name__)
app.config.from_object(Config)
redis_client = FlaskRedis(app)

class mainfunction:

    def code(num):
        to62list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        random_num = random.choices(to62list, k=num)

        return ''.join(random_num)

if __name__ == "__main__":
    print(mainfunction.code(10))

class redis_utils:
    def create(url,sec):
        set_url = mainfunction.code(15)

        # remain_time = (
        #     expire_time - datetime.now(expire_time.tzinfo))
        
        redis_client.set(set_url, url,  sec=sec)
        return set_url
        
    def get(url_id):
        return redis_client.get(url_id)
    
    def delete(url_id):
        redis_client.delete(url_id)
        return 'Success'