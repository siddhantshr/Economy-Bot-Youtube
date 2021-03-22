import aiohttp, asyncio

# https://www.reddit.com/r/memes/random/.json

async def get_meme():
    async with aiohttp.ClientSession() as conn:
        async with conn.get('https://www.reddit.com/r/memes/random/.json') as r:
            json = await r.json()
            parent = json[0]['data']['children'][0]['data']

            url = 'https://www.reddit.com{}'.format(parent['permalink'])
            img = parent["url"]
            title = parent["title"]
            desc = parent["selftext"]
            up_votes = parent["ups"]
            down_votes = parent["downs"]
            comments = parent["num_comments"]
            author = parent["author"]

            return {
                "post_url" : url,
                "img_url" : img,
                "title" : title,
                "description" : desc,
                "up_votes" : up_votes,
                "down_votes" : down_votes,
                "comments" : comments,
                "author" : author
            }


asyncio.run(get_meme())