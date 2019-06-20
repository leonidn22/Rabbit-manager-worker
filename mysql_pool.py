#!/usr/bin/env python3

import asyncio
import aiomysql
import sys
import traceback

# @asyncio.coroutine
async def mysql_insert(loop, stmt_insert):
    db = {'host': '127.0.0.1',
          'port': 3306,
          'user': 'leo',
          'password': 'leopass',
          'db': 'leo',
          'autocommit': True}
    try:
        pool = await aiomysql.create_pool(minsize=5, maxsize=20, loop=loop, **db)
        async with pool.acquire() as conn:
        # with (await pool) as conn:
            cursor = await conn.cursor()
            await cursor.execute(stmt_insert)
        return 'Done'
    except Exception as e:
        # print('\n', sys.exc_info()[1])
        # print("\n\tCheck log for more details\n")
        return traceback.format_exc()
        # logging.error(traceback.format_exc())

        # sys.exit(-1)
    finally:
        pool.close()
        await pool.wait_closed()
            # cursor.close()
            # conn.close()

# the below code is for testing
stmt_insert = "insert into leotable(c) select '13'"
loop = asyncio.get_event_loop()
loop.run_until_complete(mysql_insert(loop, stmt_insert))

