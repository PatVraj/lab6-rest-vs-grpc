#!/usr/bin/env python3

import grpc
from concurrent import futures
from PIL import Image
import io
import base64

import lab6_pb2
import lab6_pb2_grpc


class Lab6Service(lab6_pb2_grpc.Lab6ServiceServicer):

    # ADD
    def Add(self, request, context):
        result = request.a + request.b

        return lab6_pb2.addReply(
            sum=result
        )

    # DOT PRODUCT
    def DotProduct(self, request, context):
        a = request.a
        b = request.b

        result = float(sum(x * y for x, y in zip(a, b)))

        return lab6_pb2.dotProductReply(
            dotproduct=result
        )

    # RAW IMAGE
    def RawImage(self, request, context):
        try:
            img_bytes = request.img

            ioBuffer = io.BytesIO(img_bytes)
            img = Image.open(ioBuffer)

            return lab6_pb2.imageReply(
                width=img.size[0],
                height=img.size[1]
            )

        except:
            return lab6_pb2.imageReply(
                width=0,
                height=0
            )

    # JSON IMAGE
    def JsonImage(self, request, context):
        try:
            b64_img = request.img

            img_bytes = base64.b64decode(
                b64_img,
                validate=True
            )

            ioBuffer = io.BytesIO(img_bytes)
            img = Image.open(ioBuffer)

            return lab6_pb2.imageReply(
                width=img.size[0],
                height=img.size[1]
            )

        except:
            return lab6_pb2.imageReply(
                width=0,
                height=0
            )


def serve():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(
        Lab6Service(),
        server
    )

    server.add_insecure_port('[::]:50051')

    server.start()

    print("gRPC server running on port 50051")

    server.wait_for_termination()


if __name__ == '__main__':
    serve()