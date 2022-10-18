package pt.up.blog;

import io.grpc.Channel;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.Status;
import io.grpc.stub.StreamObserver;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

public class BlogClient {

    private final BlogServiceGrpc.BlogServiceBlockingStub blockingStub;
    private final BlogServiceGrpc.BlogServiceStub asyncStub;
    private static final Logger logger = Logger.getLogger(BlogClient.class.getName());
    public BlogClient(Channel channel) {
        blockingStub = BlogServiceGrpc.newBlockingStub(channel);
        asyncStub = BlogServiceGrpc.newStub(channel);
    }

    private List<String> createBlogs() {
        List<String> blogIds = new ArrayList<>();

        for (int i = 0; i < 3; i++) {
            BlogCreation blogCreation = BlogCreation.newBuilder()
                    .setAuthor(generateRandomString(8))
                    .setName(generateRandomString(8))
                    .build();

            Blog blogResponse = blockingStub.createBlog(blogCreation);
            logger.info(String.format(
                    "Blog with id %s, name %s and author %s, was created.",
                    blogResponse.getId(),
                    blogResponse.getName(),
                    blogResponse.getAuthor()
            ));
            System.out.println();

            blogIds.add(blogResponse.getId());
        }

        return blogIds;
    }

    private void getBlogInfo(List<String> blogIds) {
        for (String id: blogIds) {
            logger.info("Asking for Blog with id " + id);
            Blog blogResponse = blockingStub.getBlogInfo(BlogId.newBuilder()
                    .setId(id).build());

            logger.info(String.format(
                    "Blog with id %s, name %s and author %s, was obtained.",
                    blogResponse.getId(),
                    blogResponse.getName(),
                    blogResponse.getAuthor()
            ));
            System.out.println();
        }
    }

    private List<String> createBlogPosts(List<String> blogIds) {
        List<String> postsIds = new ArrayList<>();
        BlogPost blogPostResponse;
        BlogPostCreation blogPost;

        for (String id: blogIds) {
            blogPost = BlogPostCreation.newBuilder()
                    .setBlogId(id)
                    .setPostTitle(generateRandomString(10))
                    .setPostContent(generateRandomString(30))
                    .build();

            blogPostResponse = blockingStub.createBlogPost(blogPost);
            logger.info(String.format(
                    "Blog Post with id %s, title %s and content %s, was created.",
                    blogPostResponse.getId(),
                    blogPostResponse.getTitle(),
                    blogPostResponse.getContent()
            ));
            System.out.println();

            postsIds.add(blogPostResponse.getId());
        }

        return postsIds;
    }

    private List<String> getBlogPosts(List<String> blogIds) {
        List<String> postsIdContent = new ArrayList<>();
        Iterator<BlogPost> blogPostResponseIterator;
        BlogPost blogPost;

        for (String id: blogIds) {
            blogPostResponseIterator = blockingStub.getBlogPosts(
                    BlogId.newBuilder().setId(id).build()
            );

            while (blogPostResponseIterator.hasNext()) {
                blogPost = blogPostResponseIterator.next();

                logger.info(String.format(
                        "Post %s\nTitle: %s \nContent: %s",
                        blogPost.getId(),
                        blogPost.getTitle(),
                        blogPost.getContent()
                ));
                System.out.println();

                postsIdContent.add(blogPost.getId());
            }
        }

        return postsIdContent;
    }

    private void recordQuotesFromPosts(List<String> postIds) throws InterruptedException {
        final CountDownLatch finishLatch = new CountDownLatch(1);

        StreamObserver<QuoteSummary> responseObserver = new StreamObserver<QuoteSummary>() {
            @Override
            public void onNext(QuoteSummary value) {
                logger.info(String.format(
                        "All quotes were sent. Yay!!"
                ));
            }

            @Override
            public void onError(Throwable t) {
                Status status = Status.fromThrowable(t);
                logger.warning(String.format("Record quotes Failed: %s", status.toString()));
                finishLatch.countDown();
            }

            @Override
            public void onCompleted() {
                logger.info("Finished Recording Quotes");
                finishLatch.countDown();
            }
        };

        StreamObserver<Quote> requestObserver = asyncStub.recordQuotes(responseObserver);

        Quote quote;
        Random rand = new Random();
        try {

            for(String id: postIds) {
                quote = Quote.newBuilder()
                        .setContent(generateRandomString(15))
                        .setBlogPostId(id)
                        .build();

                logger.info(String.format(
                        "Sending quote %s of post %s",
                        quote.getContent(),
                        quote.getBlogPostId()
                ));

                requestObserver.onNext(quote);

                // Sleep for a bit before sending the next one.
                Thread.sleep(rand.nextInt(1000) + 500);

                if (finishLatch.getCount() == 0) {
                    // RPC completed or errored before we finished sending.
                    // Sending further requests won't error, but they will just be thrown away.
                    return;
                }
            }
        } catch (RuntimeException e) {
            requestObserver.onError(e);
            throw e;
        }

        requestObserver.onCompleted();

        finishLatch.await(1, TimeUnit.MINUTES);
    }

    private void sendBlogPostCommentsToChat(String postId) throws InterruptedException {
        final CountDownLatch finishLatch = new CountDownLatch(1);

        StreamObserver<Comment> requestObserver = asyncStub.blogPostChat(
                new StreamObserver<Comment>() {
                    @Override
                    public void onNext(Comment value) {
                        logger.info(String.format(
                                "Received comment of blog %s:\nDate: %s\nAuthor: %s\nContent: %s",
                                value.getBlogPostId(),
                                value.getCreatedAt(),
                                value.getAuthor(),
                                value.getContent()
                        ));
                        System.out.println();
                    }

                    @Override
                    public void onError(Throwable t) {
                        logger.warning(String.format("Chat Failed: %s", t.toString()));
                        finishLatch.countDown();
                    }

                    @Override
                    public void onCompleted() {
                        logger.info("Chat completed.");
                        finishLatch.countDown();
                    }
                }
        );

        Comment comment;
        Random rand = new Random();
        try {
            for (int i = 0; i < 2; i++) {
                comment = Comment.newBuilder()
                        .setBlogPostId(postId)
                        .setAuthor(generateRandomString(10))
                        .setContent(generateRandomString(20))
                        .build();

                logger.info(String.format(
                        "Sending comment with id %s and author %s",
                        comment.getBlogPostId(),
                        comment.getAuthor()
                ));

                requestObserver.onNext(comment);

                // Sleep for a bit before sending the next one.
                Thread.sleep(rand.nextInt(1000) + 500);
            }
        } catch (RuntimeException e) {
            requestObserver.onError(e);
            throw e;
        }

        requestObserver.onCompleted();

        finishLatch.await(1, TimeUnit.MINUTES);
    }

    // utils
    private String generateRandomString(int length) {
        int leftLimit = 97; // letter 'a'
        int rightLimit = 122; // letter 'z'
        Random random = new Random();

        return random.ints(leftLimit, rightLimit + 1)
          .limit(length)
          .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
          .toString();
    }

    public static void main(String[] args) throws Exception {
        String target = "localhost:50051";

        ManagedChannel channel = ManagedChannelBuilder.forTarget(target)
                // Channels are secure by default (via SSL/TLS). For the example we disable TLS to avoid
                // needing certificates.
                .usePlaintext()
                .build();
        try {
            BlogClient client = new BlogClient(channel);
            System.out.println("-------------- CreateBlog --------------");
            List<String> blogIds = client.createBlogs();

            System.out.println("-------------- GetBlogInfo --------------");
            client.getBlogInfo(blogIds);

            System.out.println("-------------- CreateBlogPost --------------");
            List<String> postIds = client.createBlogPosts(blogIds);

            System.out.println("-------------- GetBlogPosts --------------");
            client.getBlogPosts(blogIds);

            System.out.println("-------------- RecordQuotes --------------");
            client.recordQuotesFromPosts(postIds);

            System.out.println("-------------- BlogPostChat --------------");
            Random rand = new Random();
            client.sendBlogPostCommentsToChat(postIds.get(rand.nextInt(postIds.size())));
        } finally {
            // ManagedChannels use resources like threads and TCP connections. To prevent leaking these
            // resources the channel should be shut down when it will no longer be used. If it may be used
            // again leave it running.
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
