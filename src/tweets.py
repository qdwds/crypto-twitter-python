from ntscraper import Nitter
from models.tweets import Tweets #, UserInfo
from core.logger import log
from .ding import message_dingding_api
from datetime import datetime
from utils.date import format_date

scraper = None


def create_nitter():
    global scraper
    scraper = Nitter()

"""
查询用户推文
"""
# TODO 基本完成，测试即可
async def batch_query_users_tweets(usernames):
    # 获取最新推文数据
    scraper = Nitter()

    log.info("开始查询")
    for username in usernames:
        # 获取用户推文
        try:
            new_tweets = scraper.get_tweets(username, mode="user", number=3, max_retries=1)
            # 查询对应数据库
            db_tweets = await Tweets.filter(tweet_username=username).all()
            # 筛出link
            db_links = [tweet.link for tweet in db_tweets]
            # 筛选出 新推文
            diff_tweet = [tweet for tweet in new_tweets["tweets"] if tweet["link"] not in db_links]

            if len(diff_tweet) > 0:
              
                # 保存推文 和 更新推文数量
                for tweet in diff_tweet:
                    data = {
                        "title": "",
                        "text": tweet["text"],
                        "date": format_date(tweet["date"])
                    }
                    # 判断是否为转推
                    if tweet["is-retweet"]:
                        data["title"] =  username + "转发" + tweet["user"]["username"] + "用户推文!"
                        log.info(f"{username} --- 转发推文")
                    else:
                        data["title"] = username + "有新推文!"
                        log.info(f"{username} --- 有新推文")
                    
                    # 保存推文
                    await save_user_tweets(username, tweet)
                     # 推送消息到钉钉
                    message_dingding_api(data)

        except Exception as e:
            log.error(f"查询发生错误:{e}")
    scraper = None



"""
保存用户推文到数据库
"""
async def batch_save_users_tweets(usernames):
    log.info("开始添加新用户到数据库")
    scraper = Nitter()
    for username in usernames:
        new_user_tweets = scraper.get_tweets(username, mode="user", number=100,max_retries=1)
        
        # 批量存储推文到数据库
        for tweet in new_user_tweets["tweets"]:
           await save_user_tweets(username,tweet)

    log.info("添加新用户结束")

""""
推文存储数据库
"""
async def save_user_tweets(username, tweet):
    try:
        tw, created = await Tweets.get_or_create(
            link=tweet["link"],
            tweet_username= username,
            text= tweet["text"],
            user= tweet["user"],
            date= tweet["date"],
            is_retweet= tweet["is-retweet"],
            external_link= tweet["external-link"],
            quoted_post= tweet["quoted-post"],
            stats= tweet["stats"],
            # pictures= tweet["pictures"],
            # videos= tweet["videos"],
            # gifs= tweet["gifs"]
        )
       
        if created:
            log.info(f"{username} 推文数据存储!")
    except Exception as e:
        log.error(f"推文存储错误:{e}")



