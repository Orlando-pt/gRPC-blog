"""The Python implementation of the gRPC blog server."""

from concurrent import futures
import logging
import time
from typing import List, Tuple

import grpc
import pymongo
import blog_pb2
import blog_pb2_grpc
import blog_resources


class BlogServiceServicer(blog_pb2_grpc.BlogServiceServicer):
    """Provides methods that implement functionality of blog server."""

    def __init__(self):
        self.db = blog_resources.get_database()

    def CreateBlog(self, request, context):
        author = request.author
        if author == "":
            msg = '`Author` cannot be empty'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.Blog()

        if len(author) > 255:
            msg = 'Length of `Author` cannot be more than 255 characters'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.Blog()

        name = request.name
        if name == "":
            msg = '`Name` cannot be empty'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.Blog()

        if len(name) > 255:
            msg = 'Length of `Name` cannot be more than 255 characters'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.Blog()
        try:
            return blog_resources.create_blog(self.db, author, name)
        except Exception as e:
            print(e)
            msg = 'Blog couldn\'t be created'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.ABORTED)
            return blog_pb2.Blog()

    def GetBlogInfo(self, request, context):
        id = request.id
        if id == "":
            msg = '`id` cannot be empty'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.Blog()

        try:
            blog = blog_resources.find_blog(self.db, id)
            if blog:
                return blog
            else:
                msg = 'Blog not found'
                context.set_details(msg)
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return blog_pb2.Blog()

        except Exception as e:
            print(e)
            msg = 'Blog couldn\'t be found'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.ABORTED)
            return blog_pb2.Blog()

    def CreateBlogPost(self, request, context):
        blog_id = request.blog_id
        if blog_id == "":
            msg = '`blog_id` cannot be empty'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.BlogPost()

        post_title = request.post_title
        if post_title == "":
            msg = '`post_title` cannot be empty'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.BlogPost()

        post_content = request.post_content
        if post_content == "":
            msg = '`post_content` cannot be empty'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.BlogPost()

        try:
            return blog_resources.create_blog_post(self.db, blog_id, post_title, post_content)
        except Exception as e:
            print(e)
            msg = 'BlogPost couldn\'t be created'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.ABORTED)
            return blog_pb2.BlogPost()

    def GetBlogPosts(self, request, context):
        id = request.id
        if id == "":
            msg = '`id` cannot be empty'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return blog_pb2.BlogPost()

        try:
            posts = blog_resources.find_blog_posts(self.db, id)
            if posts:
                for post in posts:
                    yield post
            else:
                msg = 'Blog Posts not found for this BlogId'
                context.set_details(msg)
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return blog_pb2.BlogPost()

        except Exception as e:
            print(e)
            msg = 'Blog Posts couldn\'t be found'
            context.set_details(msg)
            context.set_code(grpc.StatusCode.ABORTED)
            return blog_pb2.Blog()

    def RecordQuotes(self, request_iterator, context):
        quotes = []

        for quote in request_iterator:
            quotes.append(quote)

        return blog_pb2.QuoteSummary(quote_count=len(quotes),
                                     posts_count=len(
                                         set([quote.blog_post_id for quote in quotes])),
                                     quotes=quotes
                                     )

    def BlogPostChat(self, request_iterator, context):
        post_id = ""
        cursor = None

        for comment in request_iterator:
            if post_id:
                self.getAndSendNewComments(cursor, post_id)

            if comment.blog_post_id == "" or comment.author == "" or comment.content == "":
                msg = 'Invalid Comment received'
                context.set_details(msg)
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return blog_pb2.Comment()

            if post_id != comment.blog_post_id:
                post_id = comment.blog_post_id

            try:
                yield blog_resources.add_comment_to_blog_post(
                    self.db, post_id, comment.author, comment.content)

            except Exception as e:
                print(e)
                msg = 'Could not send message'
                context.set_details(msg)
                context.set_code(grpc.StatusCode.ABORTED)
                return blog_pb2.Comment()

            if post_id:
                self.getAndSendNewComments(cursor, post_id)

    def getAndSendNewComments(self, cursor: pymongo.CursorType, post_id: str) -> pymongo.CursorType:
        if cursor and not cursor.alive:
            cursor = blog_resources.get_comments_cursor(self.db, post_id)
        while True:
            if cursor.alive:
                try:
                    doc = cursor.next()
                    yield blog_pb2.Comment(
                        blog_post_id=post_id,
                        author=doc.author,
                        content=doc.content,
                        created_at=doc.created_at
                        # TODO Fix this created_at and change to Timestamp from google
                    )
                except StopIteration:
                    break
        return cursor


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    blog_pb2_grpc.add_BlogServiceServicer_to_server(
        BlogServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
