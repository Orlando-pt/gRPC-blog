gRPC Example
==============================================

## <a name="to-build-the-examples"></a> To build the example

1. Compile the .proto file using the gRPC compiler to generate Java code both for Client and Serve:
```
$ ./gradlew installDist
```

It generates the code that includes the stubs and data classes at `build/generated/`.

This also creates the script `blog-client` in the
`build/install/blog/bin/` directory that runs the blog client. The
blog requires the server to be running.

To try the client run:

```
$ ./build/install/blog/bin/blog-client
```

That's it!
