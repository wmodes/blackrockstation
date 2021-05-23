''' A simple exmaple of a gRPC server.'''
from concurrent import futures
import logging

import grpc

import crossing_mast_pb2
import crossing_mast_pb2_grpc

class CrossingMastServicer(crossing_mast_pb2_grpc.CrossingMastServicer):
    def SetOn(self, request, unused_context):
        print('received SetOn command request.')
        response = crossing_mast_pb2.SetOnResponse()
        response.succeeded = True
        return response

    def SetOff(self, request, unused_context):
        print('received SetOff command request.')
        response = crossing_mast_pb2.SetOffResponse()
        response.succeeded = True
        return response

    def GetLogs(self, request, unused_context):
        print('received GetLogs command request.')
        print('GetLogs command is presently unhandled.')

    def StreamLogs(self, request, unused_context):
        print('received StreamLogs command.')
        print('StreamLogs is presently unhandled.')

def main():
    crossing_mast_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    crossing_mast_pb2_grpc.add_CrossingMastServicer_to_server(CrossingMastServicer(), crossing_mast_server)
    crossing_mast_server.add_insecure_port('[::]:50051')
    crossing_mast_server.start()
    crossing_mast_server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    main()