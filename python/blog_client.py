"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function
import datetime

import logging
import random
import time
from typing import List, Tuple
from essential_generators import DocumentGenerator

import grpc
import blog_pb2
import blog_pb2_grpc
import blog_resources

gen = DocumentGenerator()


def create_blogs(stub: blog_pb2_grpc.BlogServiceStub) -> List[str]:
    blog_ids: List[str] = []
    for _ in range(3):
        blog_creation = blog_pb2.BlogCreation(
            author=gen.name(), name=gen.sentence())

        blog_response = stub.CreateBlog(blog_creation)
        print("\nBlog with id %s, name %s and author %s, was created." %
              (blog_response.id, blog_response.name, blog_response.author))
        blog_ids.append(blog_response.id)

    return blog_ids


def get_blog_info(stub: blog_pb2_grpc.BlogServiceStub, blog_ids: List[str]):
    for id in blog_ids:
        blog_id = blog_pb2.BlogId(id=id)
        print("\nAsking for Blog with id %s" % (id))
        blog_response = stub.GetBlogInfo(blog_id)
        print("\nBlog with id %s, name %s and author %s, was obtained." %
              (blog_response.id, blog_response.name, blog_response.author))


def create_blog_posts(stub: blog_pb2_grpc.BlogServiceStub, blog_ids: List[str]) -> List[str]:
    posts_ids: List[str] = []
    for id in blog_ids:
        blog_post_creation = blog_pb2.BlogPostCreation(
            blog_id=id, post_title=gen.sentence(), post_content=gen.paragraph(min_sentences=3))

        blog_post_response = stub.CreateBlogPost(blog_post_creation)
        print("\nBlog Post with id %s, title %s and content %s, was created." % (
            blog_post_response.id, blog_post_response.title, blog_post_response.content))
        posts_ids.append(blog_post_response.id)
    return posts_ids


def get_blog_posts(stub: blog_pb2_grpc.BlogServiceStub, blog_ids: List[str]) -> List[Tuple[str, str]]:
    posts_id_content: List[Tuple[str, str]] = []
    for id in blog_ids:
        blog_id = blog_pb2.BlogId(id=id)
        print("\nAsking for Blog Posts of Blog with id %s" % (id))
        blog_post_responses = stub.GetBlogPosts(blog_id)
        for post in blog_post_responses:
            print("\nPost %s \n\nTitle: %s \n\nContent: %s" %
                  (post.id, post.title, post.content))
            posts_id_content.append((post.id, post.content))
    return posts_id_content


def record_quotes_from_posts(stub: blog_pb2_grpc.BlogServiceStub, posts_id_content: List[Tuple[str, str]]):
    quote_iterator = generate_quotes(posts_id_content)
    quote_summary = stub.RecordQuotes(quote_iterator)
    print("Quote Summary of quotes sent:\n")
    print(quote_summary)


def generate_quotes(posts_id_content: List[Tuple[str, str]]):
    for id, content in posts_id_content:
        words = list(map(str, content.split()))
        n_words_of_quote = random.randint(2, 5)
        start_of_quote = random.randint(0, len(words) - n_words_of_quote)
        quote_content = words[start_of_quote:start_of_quote + n_words_of_quote]
        quote = blog_pb2.Quote(content=' '.join(
            quote_content), blog_post_id=id)
        print("\nSending Quote %s of post %s" %
              (quote.content, quote.blog_post_id))
        yield quote
        time.sleep(random.randint(1, 3))


def send_blog_post_comments_to_chat(stub: blog_pb2_grpc.BlogServiceStub, post_id: str):
    responses = stub.BlogPostChat(generate_comments(post_id))
    for response in responses:
        print("\n\nReceived comment of blog %s:\nDate: %s\nAuthor: %s\nContent: %s" % (
            response.blog_post_id, datetime.datetime.fromtimestamp(response.created_at.seconds), response.author, response.content))


def generate_comments(post_id: str):
    author = gen.name()
    for _ in range(random.randint(2, 10)):
        yield blog_pb2.Comment(
            blog_post_id=post_id,
            author=author,
            content=gen.sentence(),
        )
        time.sleep(random.randint(1, 3))


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = blog_pb2_grpc.BlogServiceStub(channel)
        print("\n\n-------------- CreateBlog --------------")
        blog_ids = create_blogs(stub)
        print("\n\n-------------- GetBlogInfo --------------")
        get_blog_info(stub, blog_ids)
        print("\n\n-------------- CreateBlogPost --------------")
        posts_ids = create_blog_posts(stub, blog_ids)
        print("\n\n-------------- GetBlogPosts --------------")
        posts_id_content = get_blog_posts(stub, blog_ids)
        print("\n\n-------------- RecordQuotes --------------")
        record_quotes_from_posts(stub, posts_id_content)
        print("\n\n-------------- BlogPostChat --------------")
        send_blog_post_comments_to_chat(stub, random.choice(posts_ids))


if __name__ == '__main__':
    logging.basicConfig()
    run()
