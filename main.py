import asyncio

from aiohttp_retry import RetryClient, RetryOptions

from src.apis import request_graphql, get_post_by_username, write_post, get_header, edit_post


async def run():
    retry_options = RetryOptions(attempts=3)
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzEyOWI5ZTQtNTk2NS00OWExLWExNjQtZWE5ZTFlNTc4NGJhIiwiaWF0IjoxNzAxMTc5NDEyLCJleHAiOjE3MDExODMwMTIsImlzcyI6InZlbG9nLmlvIiwic3ViIjoiYWNjZXNzX3Rva2VuIn0.T96MfAhyeVkKuqTOLZYTU6QnPAjq91ws80VSUCIU3Ko"
    refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzEyOWI5ZTQtNTk2NS00OWExLWExNjQtZWE5ZTFlNTc4NGJhIiwidG9rZW5faWQiOiIyZWNkYTcwNC00OTdiLTRmN2ItOGU1My0yYTQyZjE0MDgzZTkiLCJpYXQiOjE3MDExNzk0MTIsImV4cCI6MTcwMzc3MTQxMiwiaXNzIjoidmVsb2cuaW8iLCJzdWIiOiJyZWZyZXNoX3Rva2VuIn0.gZTMEa-M2v44gQ3AYhXCGNReJSqR9blDl4R62dQxncQ"
    headers = get_header(access_token=access_token, refresh_token=refresh_token)
    async with RetryClient(retry_options=retry_options, headers=headers) as session:
        username = "greenrain"
        data = await get_post_by_username(session=session, username=username)
        for i in data.get('posts'):
            print(i)
        # post = data.get('data').get('posts')[0]
        # print(post)
        # print()
        # post_id = post['id']
        # title = "제목test"
        # body = "동일 제목으로 해도 되나?"
        # tags = ["태그test"]
        # data = await write_post(session=session, title=title, body=body, tags=tags)


        # data = await edit_post(session=session, post_id=post_id, title=title, body=body, tags=tags)
        # print(data)
    print('end')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
