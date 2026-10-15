#!/usr/bin/env python3

import grpc
import lab6_pb2
import lab6_pb2_grpc
import random
import time
import argparse
import base64


# Parse command-line arguments

parser = argparse.ArgumentParser(
    description='gRPC client for measuring server operations'
)

parser.add_argument('host')
parser.add_argument(
    'cmd',
    choices=['add', 'rawImage', 'dotProduct', 'jsonImage']
)
parser.add_argument('reps', type=int)

parser.add_argument(
    '-p', '--port',
    type=int,
    default=50051,
    help='gRPC server port (default: 50051)'
)

parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help='Print the response from the server'
)

args = parser.parse_args()

if args.reps <= 0:
    parser.error("reps must be greater than zero")


# Prepare request data

if args.cmd == 'add':

    request = lab6_pb2.addMsg(
        a=5,
        b=10
    )

elif args.cmd == 'dotProduct':

    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    request = lab6_pb2.dotProductMsg(
        a=a,
        b=b
    )

elif args.cmd == 'rawImage':

    img = open(
        'Flatirons_Winter_Sunrise_edit_2.jpg',
        'rb'
    ).read()

    request = lab6_pb2.rawImageMsg(
        img=img
    )

elif args.cmd == 'jsonImage':

    img = open(
        'Flatirons_Winter_Sunrise_edit_2.jpg',
        'rb'
    ).read()

    img_base64 = base64.b64encode(img).decode('utf-8')

    request = lab6_pb2.jsonImageMsg(
        img=img_base64
    )


# Establish gRPC connection
with grpc.insecure_channel(f'{args.host}:{args.port}') as channel:
    
    grpc.channel_ready_future(channel).result(timeout=10)
    stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

    print(
        f"Running {args.reps} reps against "
        f"{args.host}:{args.port}"
    )

    # Perform requested operation
    start = time.perf_counter()
    for _ in range(args.reps):
        if args.cmd == 'add':
            response = stub.Add(request)
        elif args.cmd == 'dotProduct':
            response = stub.DotProduct(request)
        elif args.cmd == 'rawImage':
            response = stub.RawImage(request)
        elif args.cmd == 'jsonImage':
            response = stub.JsonImage(request)

    delta = ((time.perf_counter() - start) / args.reps) * 1000

    # Print results
    if args.debug:
        print("Response is:", response)
        
    if args.cmd == 'add':
        print("Sum:", response.sum)
    elif args.cmd == 'dotProduct':
        print("Dot product:", response.dotproduct)
    elif args.cmd in ['rawImage', 'jsonImage']:
        print("Width:", response.width)
        print("Height:", response.height)

    print("Took", delta, "ms per operation")