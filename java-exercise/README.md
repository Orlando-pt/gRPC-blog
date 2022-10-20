gRPC Example
==============================================

## <a name="to-build-the-examples"></a> To build the example

1. From the main directory:
```
$ ./gradlew installDist
```

This creates the script `blog-client` in the
`build/install/blog/bin/` directory that runs the blog client. The
blog requires the server to be running.

To try the client run:

```
$ ./build/install/blog/bin/blog-client
```

That's it!
