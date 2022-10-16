# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: blog.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nblog.proto\x12\x04\x62log\x1a\x1fgoogle/protobuf/timestamp.proto\"0\n\x04\x42log\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\",\n\x0c\x42logCreation\x12\x0e\n\x06\x61uthor\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"M\n\x10\x42logPostCreation\x12\x0f\n\x07\x62log_id\x18\x01 \x01(\t\x12\x12\n\npost_title\x18\x02 \x01(\t\x12\x14\n\x0cpost_content\x18\x03 \x01(\t\"6\n\x08\x42logPost\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"p\n\x07\x43omment\x12\x14\n\x0c\x62log_post_id\x18\x01 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12.\n\ncreated_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\".\n\x05Quote\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\x12\x14\n\x0c\x62log_post_id\x18\x02 \x01(\t\"U\n\x0cQuoteSummary\x12\x13\n\x0bquote_count\x18\x01 \x01(\x05\x12\x13\n\x0bposts_count\x18\x02 \x01(\x05\x12\x1b\n\x06quotes\x18\x03 \x03(\x0b\x32\x0b.blog.Quote\"\x14\n\x06\x42logId\x12\n\n\x02id\x18\x01 \x01(\t2\xb7\x02\n\x0b\x42logService\x12,\n\nCreateBlog\x12\x12.blog.BlogCreation\x1a\n.blog.Blog\x12\'\n\x0bGetBlogInfo\x12\x0c.blog.BlogId\x1a\n.blog.Blog\x12\x38\n\x0e\x43reateBlogPost\x12\x16.blog.BlogPostCreation\x1a\x0e.blog.BlogPost\x12.\n\x0cGetBlogPosts\x12\x0c.blog.BlogId\x1a\x0e.blog.BlogPost0\x01\x12\x33\n\x0cRecordQuotes\x12\x0b.blog.Quote\x1a\x12.blog.QuoteSummary\"\x00(\x01\x12\x32\n\x0c\x42logPostChat\x12\r.blog.Comment\x1a\r.blog.Comment\"\x00(\x01\x30\x01\x42\x18\n\npt.up.blogB\x08\x42logGRPCP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'blog_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\npt.up.blogB\010BlogGRPCP\001'
  _BLOG._serialized_start=53
  _BLOG._serialized_end=101
  _BLOGCREATION._serialized_start=103
  _BLOGCREATION._serialized_end=147
  _BLOGPOSTCREATION._serialized_start=149
  _BLOGPOSTCREATION._serialized_end=226
  _BLOGPOST._serialized_start=228
  _BLOGPOST._serialized_end=282
  _COMMENT._serialized_start=284
  _COMMENT._serialized_end=396
  _QUOTE._serialized_start=398
  _QUOTE._serialized_end=444
  _QUOTESUMMARY._serialized_start=446
  _QUOTESUMMARY._serialized_end=531
  _BLOGID._serialized_start=533
  _BLOGID._serialized_end=553
  _BLOGSERVICE._serialized_start=556
  _BLOGSERVICE._serialized_end=867
# @@protoc_insertion_point(module_scope)