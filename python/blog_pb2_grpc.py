# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import blog_pb2 as blog__pb2


class BlogServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateBlog = channel.unary_unary(
                '/blog.BlogService/CreateBlog',
                request_serializer=blog__pb2.BlogCreation.SerializeToString,
                response_deserializer=blog__pb2.Blog.FromString,
                )
        self.GetBlogInfo = channel.unary_unary(
                '/blog.BlogService/GetBlogInfo',
                request_serializer=blog__pb2.BlogId.SerializeToString,
                response_deserializer=blog__pb2.Blog.FromString,
                )
        self.CreateBlogPost = channel.unary_unary(
                '/blog.BlogService/CreateBlogPost',
                request_serializer=blog__pb2.BlogPostCreation.SerializeToString,
                response_deserializer=blog__pb2.BlogPost.FromString,
                )
        self.GetBlogPosts = channel.unary_stream(
                '/blog.BlogService/GetBlogPosts',
                request_serializer=blog__pb2.BlogId.SerializeToString,
                response_deserializer=blog__pb2.BlogPost.FromString,
                )
        self.RecordQuotes = channel.stream_unary(
                '/blog.BlogService/RecordQuotes',
                request_serializer=blog__pb2.Quote.SerializeToString,
                response_deserializer=blog__pb2.QuoteSummary.FromString,
                )
        self.BlogPostChat = channel.stream_stream(
                '/blog.BlogService/BlogPostChat',
                request_serializer=blog__pb2.Comment.SerializeToString,
                response_deserializer=blog__pb2.Comment.FromString,
                )


class BlogServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateBlog(self, request, context):
        """A simple RPC.

        Creates a Blog (with auth TODO)

        An error should be provided if not possible (TODO).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlogInfo(self, request, context):
        """A simple RPC.

        Gets Blog Info given it's id

        An error should be provided if blog not found.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateBlogPost(self, request, context):
        """A simple RPC.

        Creates a Blog Post given it's Blog id and Blog Post (with auth TODO)

        An error should be provided if Blog Post was not created..
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlogPosts(self, request, context):
        """A server-to-client streaming RPC.

        Obtains the Blog Posts avaialble for a given Blog.  Results are
        streamed rather than returned at once (e.g. in a response message with a
        repeated field), as the Blog may have a large number of posts.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RecordQuotes(self, request_iterator, context):
        """A client-to-server streaming RPC.

        Accepts a stream of quotes while a blog post is being traversed, returning a
        QuoteSummary when traversal is completed.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BlogPostChat(self, request_iterator, context):
        """A Bidirectional streaming RPC.

        Accepts a stream of comments sent while a Blog Post is being read,
        while receiving other comments (e.g. from other users).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BlogServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateBlog': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateBlog,
                    request_deserializer=blog__pb2.BlogCreation.FromString,
                    response_serializer=blog__pb2.Blog.SerializeToString,
            ),
            'GetBlogInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBlogInfo,
                    request_deserializer=blog__pb2.BlogId.FromString,
                    response_serializer=blog__pb2.Blog.SerializeToString,
            ),
            'CreateBlogPost': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateBlogPost,
                    request_deserializer=blog__pb2.BlogPostCreation.FromString,
                    response_serializer=blog__pb2.BlogPost.SerializeToString,
            ),
            'GetBlogPosts': grpc.unary_stream_rpc_method_handler(
                    servicer.GetBlogPosts,
                    request_deserializer=blog__pb2.BlogId.FromString,
                    response_serializer=blog__pb2.BlogPost.SerializeToString,
            ),
            'RecordQuotes': grpc.stream_unary_rpc_method_handler(
                    servicer.RecordQuotes,
                    request_deserializer=blog__pb2.Quote.FromString,
                    response_serializer=blog__pb2.QuoteSummary.SerializeToString,
            ),
            'BlogPostChat': grpc.stream_stream_rpc_method_handler(
                    servicer.BlogPostChat,
                    request_deserializer=blog__pb2.Comment.FromString,
                    response_serializer=blog__pb2.Comment.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'blog.BlogService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BlogService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateBlog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blog.BlogService/CreateBlog',
            blog__pb2.BlogCreation.SerializeToString,
            blog__pb2.Blog.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBlogInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blog.BlogService/GetBlogInfo',
            blog__pb2.BlogId.SerializeToString,
            blog__pb2.Blog.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateBlogPost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/blog.BlogService/CreateBlogPost',
            blog__pb2.BlogPostCreation.SerializeToString,
            blog__pb2.BlogPost.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBlogPosts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/blog.BlogService/GetBlogPosts',
            blog__pb2.BlogId.SerializeToString,
            blog__pb2.BlogPost.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RecordQuotes(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/blog.BlogService/RecordQuotes',
            blog__pb2.Quote.SerializeToString,
            blog__pb2.QuoteSummary.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BlogPostChat(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/blog.BlogService/BlogPostChat',
            blog__pb2.Comment.SerializeToString,
            blog__pb2.Comment.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
