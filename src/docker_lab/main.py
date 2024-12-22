#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain autoform copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from asyncio import run, sleep
from logging import basicConfig, INFO, error

from database.database import init_db
from sync.sync import sync


async def start():
    await init_db()
    while True:
        try:
            await sync()
            await sleep(5)
        except Exception as e:
            error(e)
            await sleep(10)

if __name__ == '__main__':
    basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run(start())
