import json

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, redirect

from ..forms import readingForm
from ..data.tarot import createReading, getReadingById, deleteReading

class NewReadingView(APIView):
    def get(self, request):
        form = readingForm()
        return render(request, 'tarot/new_reading.html', {'form': form})
    
    def post(self, request):
        form = readingForm(request.POST)
        if form.is_valid():
            userId = request.session.get('user_id')
            question = form.cleaned_data.get('question')
            readingType_str = form.cleaned_data.get('readingType')
            from ..models.tarot import ReadingType
            try:
                readingType = ReadingType[readingType_str]
            except KeyError:
                return Response({'error': f'Invalid reading type: {readingType_str}'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                newReading = createReading(userId, question, readingType)
                if not newReading:
                    return Response({'error': 'Could not create reading.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Redirect to the reading detail page after creation
                return redirect('reading', reading_id=newReading.id)
            except Exception as e:
                return Response({'error': f'Error creating reading: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST)

LAYOUT_MAP = {
    "LILIA": "tarot/layouts/lilias_safe_passage.html",
    "PPF": "tarot/layouts/past_present_future.html",
    "SINGLE": "tarot/layouts/random_card.html",
}

class ReadingView(APIView):
    def get(self, request, reading_id):
        try:
            reading = getReadingById(reading_id)
            if reading:
                reading_dict = reading.to_dict()
                template_key = reading_dict['readingType']
                print(template_key)
                reading_json = json.dumps(reading_dict)
                return render(request, 'tarot/reading_template.html', {
                    'reading': reading_dict, 
                    'reading_json': reading_json,
                    'layout_template': LAYOUT_MAP[template_key]
                })
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