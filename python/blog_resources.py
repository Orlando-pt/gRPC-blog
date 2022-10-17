"""Common resources used in the gRPC route guide example."""

import datetime
from bson import ObjectId
from typing import List, Tuple

from pymongo import MongoClient
import pymongo
from google.protobuf.timestamp_pb2 import Timestamp

import blog_pb2


def get_database():
    # Provide the mongodb url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://root:root@localhost/"

    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)

    return client["blog"]


def create_blog(client: MongoClient, author: str, name: str) -> blog_pb2.Blog:
    collection = client["blogs"]

    blog = {
        "author": author,
        "name": name
    }

    inserted = collection.insert_one(blog)
    return blog_pb2.Blog(
        id=str(inserted.inserted_id),
        author=blog["author"],
        name=blog["name"]
    )


def find_blog(client: MongoClient, id: str) -> Tuple[blog_pb2.Blog, None]:
    collection = client["blogs"]

    result = collection.find_one({"_id": ObjectId(id)})

    if result:
        return blog_pb2.Blog(
            id=str(result['_id']),
            author=result['author'],
            name=result['name']
        )
    else:
        return None


def create_blog_post(client: MongoClient, blog_id: str, post_title: str, post_content: str) -> blog_pb2.BlogPost:
    collection = client[f"blog_{blog_id}_posts"]
    blog_post = {
        "title": post_title,
        "content": post_content
    }

    inserted = collection.insert_one(blog_post)
    return blog_pb2.BlogPost(
        id=str(inserted.inserted_id),
        title=blog_post["title"],
        content=blog_post["content"],
    )


def find_blog_posts(client: MongoClient, id: str) -> List[blog_pb2.BlogPost]:
    collection = client[f"blog_{id}_posts"]

    result = collection.find()

    posts = []

    for post in result:
        posts.append(blog_pb2.BlogPost(
            id=str(post['_id']),
            title=post['title'],
            content=post['content']
        ))

    return posts


def add_comment_to_blog_post(client: MongoClient, post_id: str, author: str, content: str) -> blog_pb2.Comment:
    collection = client[f"blog_post_{post_id}_comments"]
    creation_date = datetime.datetime.utcnow()
    comment = {
        "author": author,
        "content": content,
        "created_at": creation_date
    }

    inserted = collection.insert_one(comment)
    return blog_pb2.Comment(
        blog_post_id=post_id,
        author=comment["author"],
        content=comment["content"],
        created_at=Timestamp(seconds=int(creation_date.timestamp()))
    )


def get_comments_cursor(client: MongoClient, post_id: str) -> pymongo.CursorType:
    collection = client[f"blog_post_{post_id}_comments"]

    return collection.find({"created_at": {
        "$gt": datetime.datetime.utcnow()}})
