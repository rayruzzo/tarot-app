from bson import ObjectId

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect

from ..data.journal import create_journal_entry, get_journal_entry, delete_journal_entry, update_journal_entry, get_all_journal_entries
from ..models import JournalEntryType, GuidedQuestions
from ..forms import GuidedJournalEntryForm, FreeFormJournalEntryForm


class UserJournalView(APIView):
    def get(self, request, user_id):
        entries = get_all_journal_entries(user_id)
        return Response(entries, status=status.HTTP_200_OK)

class JournalEntryView(APIView):
    def get(self, request, reading_id):
        entry = get_journal_entry(reading_id)['data']
        questions = {
            'feel': GuidedQuestions.FEEL.value,
            'notice': GuidedQuestions.NOTICE.value,
            'connect': GuidedQuestions.CONNECT.value,
            'context': GuidedQuestions.CONTEXT.value,
            'action': GuidedQuestions.ACTION.value
        }
        return render(request, 'journal/journal_entry.html', {'entry': entry.to_dict(), 'questions': questions})

    def post(self, request, reading_id):
        try:
            data = request.data
            type_str = data.get('type')
            try:
                type_enum = JournalEntryType[type_str]
            except (KeyError, TypeError):
                return Response({'error': f'Invalid journal entry type: {type_str}'}, status=status.HTTP_400_BAD_REQUEST)


            if type_enum == JournalEntryType.FREEFORM:
                content = data.get('content')
                entry = create_journal_entry(reading_id, type_enum, content=content)
                return redirect(f"/readings/{reading_id}/journal/")


            if type_enum == JournalEntryType.GUIDED:
                questions = {
                    'feel': data.get('feel'),
                    'notice': data.get('notice'),
                    'connect': data.get('connect'),
                    'context': data.get('context'),
                    'action': data.get('action')
                }
                entry = create_journal_entry(reading_id, type_enum, **questions)
                print(entry.type)
                return redirect(f"/readings/{reading_id}/journal/", {'entry': entry.to_dict()})

            return Response({'error': 'Unhandled journal entry type.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  
    def put(self, request, entry_id):
        try:
            data = request.data
            type = data.get('type')
            if type == JournalEntryType.FREEFORM:
                content = data.get('content')
                entry = update_journal_entry(entry_id, type, content)
                return Response(entry, status=status.HTTP_200_OK)
            
            if type == JournalEntryType.GUIDED:
                questions = {
                    'feel': data.get('feel'),
                    'notice': data.get('notice'),
                    'connect': data.get('connect'),
                    'context': data.get('context'),
                    'action': data.get('action')
                }
                entry = update_journal_entry(entry_id, type, questions)
                return Response(entry, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, entry_id):
        try:
            delete_journal_entry(entry_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreateJournalEntryView(APIView):
    def get(self, request, *args, **kwargs):
        guided_form = GuidedJournalEntryForm()
        freeform_form = FreeFormJournalEntryForm()
        reading_id = kwargs.get('reading_id')
        return render(request, 'journal/new_journal.html', {
            'guided_form': guided_form,
            'freeform_form': freeform_form,
            'reading_id': reading_id
        })