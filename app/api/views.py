from rest_framework.views import APIView, Response


class HelloWorldView(APIView):

    @staticmethod
    def get(request):

        return Response({'message': 'Hello World!'})
