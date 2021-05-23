''' A simple example of a gRPC client.'''

import logging

import grpc

import crossing_mast_pb2
import crossing_mast_pb2_grpc


def main():
  channel = grpc.insecure_channel('localhost:50051')
  crossing_mast_stub = crossing_mast_pb2_grpc.CrossingMastStub(channel)
  request = crossing_mast_pb2.SetOnRequest()

  # Call the crossing master SetOn
  response = crossing_mast_stub.SetOn(request)
  print(f'Crossing mast turned on succesfully: {response.succeeded}')


if __name__ == '__main__':
  logging.basicConfig()
  main()
