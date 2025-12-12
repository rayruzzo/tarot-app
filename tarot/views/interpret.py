from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tarot.llm import interpreter

class InterpretationAPIView(APIView):
    def post(self, request):
        reading = request.data.get('reading')
        reading_id = reading.get('_id') if reading else None
        if not reading_id:
            return Response({'error': 'Missing reading_id'}, status=status.HTTP_400_BAD_REQUEST)
        # Generate and save interpretation
        interpretation = interpreter.generate_interpretation_prompt(reading_id)
        interpreter.save_interpretation(reading_id, interpretation)
        return Response({'interpretation': interpretation}, status=status.HTTP_200_OK)

    def get(self, request):
        reading_id = request.query_params.get('reading_id')
        if not reading_id:
            return Response({'error': 'Missing reading_id'}, status=status.HTTP_400_BAD_REQUEST)
        interpretation = interpreter.get_interpretation(reading_id)
        if not interpretation:
            return Response({'error': 'No interpretation found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'interpretation': interpretation}, status=status.HTTP_200_OK)
