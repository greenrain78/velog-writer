from typing import List

from aiohttp_retry import RetryClient


def get_header(access_token: str, refresh_token: str) -> dict:
    return {
        "authority": "v3.velog.io",
        "origin": "https://velog.io",
        "content-type": "application/json",
        "cookie": f"access_token={access_token}; refresh_token={refresh_token}",
    }


async def request_graphql(session: RetryClient, query: str, variables: dict, operation_name: str):
    payload = {"query": query, "variables": variables, "operationName": operation_name}
    async with session.post("https://v2cdn.velog.io/graphql", json=payload) as response:
        return await response.json()


async def get_post_by_username(session: RetryClient, username: str):
    query = """query 
        Posts($cursor: ID, $username: String, $temp_only: Boolean, $tag: String, $limit: Int) {
           posts(cursor: $cursor, username: $username, temp_only: $temp_only, tag: $tag, limit: $limit) {
               id
                title
                body
                short_description
                released_at
                updated_at
                tags
                is_private
           }
        }"""
    variables = {"username": username}
    res = await request_graphql(session=session, query=query, variables=variables, operation_name="Posts")
    return res.get("data")


async def write_post(session: RetryClient, title: str, body: str, tags: List):
    query = """mutation 
        WritePost($title: String, $body: String, $tags: [String], $is_markdown: Boolean, $is_temp: Boolean, 
        $is_private: Boolean, $url_slug: String, $thumbnail: String, $meta: JSON, $series_id: ID) {
            writePost(title: $title, body: $body, tags: $tags, is_markdown: $is_markdown, is_temp: $is_temp, 
            is_private: $is_private, url_slug: $url_slug, thumbnail: $thumbnail, meta: $meta, series_id: $series_id) {
            id
            user {
                id
                username
                __typename
            }
            url_slug
            __typename
            }
        }"""
    variables = {
        "title": title,
        "body": body,
        "tags": tags,
        "is_markdown": True,
        "is_temp": False,
        "is_private": False,
        "url_slug": title,
        "thumbnail": None,
        "meta": {
            "short_description": body
        },
        "series_id": None
    }
    result = await request_graphql(session=session, query=query, variables=variables, operation_name="WritePost")
    return result


async def edit_post(session: RetryClient, post_id: str, title: str, body: str, tags: List):
    query = """mutation 
    EditPost($id: ID!, $title: String, $body: String, $tags: [String], $is_markdown: Boolean, $is_temp: Boolean, 
    $is_private: Boolean, $url_slug: String, $thumbnail: String, $meta: JSON, $series_id: ID) {
        editPost(id: $id, title: $title, body: $body, tags: $tags, is_markdown: $is_markdown, is_temp: $is_temp, 
        is_private: $is_private, url_slug: $url_slug, thumbnail: $thumbnail, meta: $meta, series_id: $series_id) {
        id
        title
        released_at
        updated_at
        tags
        body
        short_description
        is_private
        url_slug
      }
    }
    """
    variables = {
        "id": post_id,
        "title": title,
        "body": body,
        "tags": tags,
        "is_markdown": True,
        "is_temp": False,
        "is_private": False,
        "url_slug": title,
        "thumbnail": None,
        "meta": {
            "short_description": body
        },
        "series_id": None
    }
    result = await request_graphql(session=session, query=query, variables=variables, operation_name="EditPost")
    return result
