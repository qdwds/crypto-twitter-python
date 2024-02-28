import asyncio
from tortoise import Tortoise
from core.logger import log
from src.tweets import batch_query_users_tweets,batch_save_users_tweets
from core.config import config
"""
添加新用户
True: 首次添加表数据
False: 正常开始监控
"""
is_add_user = False

users=[
    "@NEXTYPE1",
    "@CherryswapNet",
    "@KalataOfficial",
    "@Rollup_Finance"
]


# 执行 异步任务
async def periodic_task():
    global users

    while True:
        try:
            await batch_query_users_tweets(users)
        except Exception as e:
            log.error(f"执行异步任务错误: {e}")

        await asyncio.sleep(2 * 60)



async def main():
    global is_add_user
    global users

    log.info("正在启动项目..")
 
    # 初始化 Tortoise
    try:
        await Tortoise.init(
            db_url=f'mysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_DATABASE}',
            modules={'models': ['models.tweets']}
        )
    except Exception as e:
        print(f"连接数据库报错：{e}")
    
    # 生成数据库表
    try:
        # 生成数据库表
        await Tortoise.generate_schemas(safe=True)
        log.info("数据库表正常")
    except Exception as e:
        log.error(f"创建表报错: {e}")
        return
    
    # 添加新用户
    if is_add_user:
        # 添加新用户
        await batch_save_users_tweets(users)
    else:
        # 启动异步任务
        task = asyncio.create_task(periodic_task())
        await task

    # # 关闭 Tortoise 连接
    # await Tortoise.close_connections()



if __name__ == "__main__":
    asyncio.run(main())
    
 

