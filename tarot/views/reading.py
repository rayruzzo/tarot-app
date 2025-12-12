from rest_framework.decorators import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from ..forms import readingForm
from ..data.tarot import createReading, getReadingById, deleteReading
from ..utils import TEMPLATE_DISPATCH

@method_decorator(login_required, name='dispatch')
class NewReadingView(APIView):
    def get(self, request):
        form = readingForm()
        return render(request, 'tarot/reading.html', {'form': form})
    
    def post(self, request):
        form = readingForm(request.POST)
        if form.is_valid():
            userId = request.session.get('user_id')
            question = form.cleaned_data['question']
            readingType = form.cleaned_data['readingType']
            try:
                newReading = createReading(userId, question, readingType)
                return render(request, TEMPLATE_DISPATCH[readingType], {'reading': newReading})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class ReadingView(APIView):
    def get(self, request, reading_id):
        try:
            reading = getReadingById(reading_id)
            if reading:
                return render(request, TEMPLATE_DISPATCH[reading.readingType], {'reading': reading})
            else:
                return Response({'error': 'Reading not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request, reading_id):
        try:
            deleteReading(reading_id)
            return Response({'message': 'Reading deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)