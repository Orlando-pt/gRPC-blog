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

    /**
     * It is highly recommended to complete this exercise
     * having has support the following tutorial, please read it and have fun!
     * https://grpc.io/docs/languages/java/basics/
     */
    private final BlogServiceGrpc.BlogServiceBlockingStub blockingStub;
    // TODO
//    private final BlogServiceGrpc.BlogServiceStub asyncStub;
    private static final Logger logger = Logger.getLogger(BlogClient.class.getName());
    public BlogClient(Channel channel) {
        // create blocking stub
        blockingStub = BlogServiceGrpc.newBlockingStub(channel);
        // TODO create asynchronous stub
//        asyncStub =
    }

    /**
     * Creates 3 blogs with random information
     * @return an array with the ids of the generated blogs
     */
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

    /**
     * Retrieve Blog information
     * @param blogIds list with ids of the desired blogs
     */
    private void getBlogInfo(List<String> blogIds) {
        for (String id: blogIds) {
            logger.info("Asking for Blog with id " + id);

            Blog blogResponse = blockingStub.getBlogInfo(
                    BlogId.newBuilder().setId(id).build()
            );

            logger.info(String.format(
                    "Blog with id %s, name %s and author %s, was obtained.",
                    blogResponse.getId(),
                    blogResponse.getName(),
                    blogResponse.getAuthor()
            ));
            System.out.println();
        }
    }

    /**
     * Creates posts on a specific blog
     * @param blogIds list with blog ids
     * @return list with the ids of posts created
     */
    private List<String> createBlogPosts(List<String> blogIds) {
        List<String> postsIds = new ArrayList<>();
        BlogPost blogPostResponse;
        BlogPostCreation blogPost;

        for (String id: blogIds) {

            /**
             * TODO 0
             * Create a Post instance that allows to call the server
             * and create a post on the given Blog
             *
             * It might help to check the .proto file for more information on which
             * fields belong to this service
             */
            blogPost = BlogPostCreation.getDefaultInstance(); // this code does not work

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

    /**
     * Retrieves a stream of blog posts
     * @param blogIds list with blog ids
     * @return list with post ids
     */
    private List<String> getBlogPosts(List<String> blogIds) {
        List<String> postsIds = new ArrayList<>();

        /**
         * TODO 1
         * This method allows to contact a service in which the server
         * sends a stream of messages.
         * In the next lines develop the necessary code to retrieve
         * the stream from the server.
         */
        // TODO 1 Here create a reference to Iterate through the received blog posts
        // Like the following one Iterator<String> aStringIterator
        // ? blogPostResponseIterator
        BlogPost blogPost;

        for (String id: blogIds) {
            // TODO 1 Add the appropriate information inside the next method call
//            blogPostResponseIterator = blockingStub.getBlogPosts();

            // TODO 2 When the tasks above are completed uncomment the next block of code
            /**
            while (blogPostResponseIterator.hasNext()) {
                blogPost = blogPostResponseIterator.next();

                logger.info(String.format(
                        "Post %s\nTitle: %s \nContent: %s",
                        blogPost.getId(),
                        blogPost.getTitle(),
                        blogPost.getContent()
                ));
                System.out.println();

                postsIds.add(blogPost.getId());
            }
             */
        }

        return postsIds;
    }

    /**
     * Sends a stream of Quotes
     * @param postIds lists of post ids
     * @throws InterruptedException
     */
    private void recordQuotesFromPosts(List<String> postIds) throws InterruptedException {
        final CountDownLatch finishLatch = new CountDownLatch(1);

        // This observer checks for whatever the server answers
        StreamObserver<QuoteSummary> responseObserver = new StreamObserver<QuoteSummary>() {
            @Override
            public void onNext(QuoteSummary summary) {
                /**
                 * As the server only sends a message (when all quotes were sent),
                 * then we can assume that this method will only be called one time with the
                 * quote summary
                 */
                logger.info(String.format(
                        "All quotes were sent. Yay!!"
                ));
                logger.info(String.format(
                        "In total were sent %d quotes relative to %d posts.",
                        summary.getQuoteCount(),
                        summary.getPostsCount()
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

        /**
         * TODO 3 This is an asynchronous call so please go to the constructor
         * of this class and create an async stub
         */
//        StreamObserver<Quote> requestObserver = asyncStub.recordQuotes(responseObserver);

        Quote quote;
        Random rand = new Random();
        try {

            for(String id: postIds) {
                /**
                 * TODO 3 Build quotes and send them to the server. Just build, the send we already took care of below ;)
                 * The server will be waiting for quotes
                 * until the client calls the onCompleted() method
                 */
//                quote = Quote.newBuilder()

                // TODO 3 When the tasks above are completed uncomment the next block of code
                /**
                logger.info(String.format(
                        "Sending quote %s of post %s",
                        quote.getContent(),
                        quote.getBlogPostId()
                ));

                requestObserver.onNext(quote);
                 */

                // Sleep for a bit before sending the next one.
                Thread.sleep(rand.nextInt(1000) + 500);

                if (finishLatch.getCount() == 0) {
                    // RPC completed or errored before we finished sending.
                    // Sending further requests won't error, but they will just be thrown away.
                    return;
                }
            }
        } catch (RuntimeException e) {
            // TODO 3 also to uncomment
//            requestObserver.onError(e);
            throw e;
        }

        // TODO you already know what to do
//        requestObserver.onCompleted();

        finishLatch.await(1, TimeUnit.MINUTES);
    }

    /**
     * Simulates a chat where client and server send each other
     * messages continuously
     * @param postId a list of post ids
     * @throws InterruptedException
     */
    private void sendBlogPostCommentsToChat(String postId) throws InterruptedException {
        final CountDownLatch finishLatch = new CountDownLatch(1);


        /**
         * TODO 4 For the next line to work it needs a response observer that is triggered each time the
         * server sends back a comment
         *
         * Implement the appropriate observer and add him into the method call
         */
//        StreamObserver<Comment> requestObserver = asyncStub.blogPostChat(The observer is going to be here);

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

                // TODO 4 uncomment
//                requestObserver.onNext(comment);

                // Sleep for a bit before sending the next one.
                Thread.sleep(rand.nextInt(1000) + 500);
            }
        } catch (RuntimeException e) {
            // TODO 4 uncomment
//            requestObserver.onError(e);
            throw e;
        }

        // TODO 4 and uncomment one last time
//        requestObserver.onCompleted();

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

            // TODO 1 uncomment
//            System.out.println("-------------- CreateBlogPost --------------");
//            List<String> postIds = client.createBlogPosts(blogIds);

            // TODO 2 uncomment
//            System.out.println("-------------- GetBlogPosts --------------");
//            client.getBlogPosts(blogIds);

            // TODO 3 uncomment
//            System.out.println("-------------- RecordQuotes --------------");
//            client.recordQuotesFromPosts(postIds);

            // TODO 4 uncomment
//            System.out.println("-------------- BlogPostChat --------------");
//            Random rand = new Random();
//            client.sendBlogPostCommentsToChat(postIds.get(rand.nextInt(postIds.size())));

            // TODO 4 uncomment the next line for bonus
//            System.out.println("\n-------------- Hope you enjoyed our little exercise. Until next time <3 --------------");
        } finally {
            // ManagedChannels use resources like threads and TCP connections. To prevent leaking these
            // resources the channel should be shut down when it will no longer be used. If it may be used
            // again leave it running.
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
