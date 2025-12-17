from bson import ObjectId

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect

from ..data.journal import create_journal_entry, get_journal_entry, delete_journal_entry, update_journal_entry, get_all_journal_entries
from ..models import JournalEntryType, GuidedQuestions, GuidedJournalEntry, FreeFormJournalEntry
from ..forms import GuidedJournalEntryForm, FreeFormJournalEntryForm


class UserJournalView(APIView):
    def get(self, request, user_id):
        entries = get_all_journal_entries(user_id)
        return Response(entries, status=status.HTTP_200_OK)

class JournalEntryView(APIView):
    def get(self, request, reading_id):
        entry = get_journal_entry(reading_id)['data']
        guided_questions = {
            'feel': GuidedQuestions.FEEL.value,
            'notice': GuidedQuestions.NOTICE.value,
            'connect': GuidedQuestions.CONNECT.value,
            'context': GuidedQuestions.CONTEXT.value,
            'action': GuidedQuestions.ACTION.value
        }
        return render(request, 'journal/journal_entry.html', {'entry': entry.to_dict(), 'questions': guided_questions})

    def post(self, request, reading_id, entry_id):
        try:
            data = request.data
            type_str = data.get('type')
            try:
                type_enum = JournalEntryType[type_str]
            except (KeyError, TypeError):
                return Response({'error': f'Invalid journal entry type: {type_str}'}, status=status.HTTP_400_BAD_REQUEST)

            if type_enum == JournalEntryType.FREEFORM:
                content = data.get('content')
                entry = update_journal_entry(entry_id, type_enum, content=content)
                return redirect(f"/readings/{reading_id}/, {'entry': entry.to_dict()}")


            if type_enum == JournalEntryType.GUIDED:
                kwargs = {
                    'feel': data.get('feel'),
                    'notice': data.get('notice'),
                    'connect': data.get('connect'),
                    'context': data.get('context'),
                    'action': data.get('action')
                }
                entry = create_journal_entry(reading_id, type_enum, **kwargs)
                print(entry.type)
                return redirect(f"/readings/{reading_id}/journal/", {'entry': entry.to_dict()})

            return Response({'error': 'Unhandled journal entry type.'}, status=status.HTTP_400_BAD_REQUEST)
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
        return render(request, 'journal/_journal_form.html', {
            'guided_form': guided_form,
            'freeform_form': freeform_form,
            'reading_id': reading_id
        })
    
class EditJournalEntryView(APIView):
    def get(self, request, **kwargs):
        entry_id = kwargs.get('entry_id')
        entry_type = request.query_params.get('entry_type')
        print(entry_type)
        if entry_type == '1':
            entry = GuidedJournalEntry.objects.get(id=ObjectId(entry_id)) 
            guided_form = GuidedJournalEntryForm(initial=entry.to_dict())
            freeform_form = FreeFormJournalEntryForm(initial=entry.to_dict())
        elif entry_type == '0':
            entry = FreeFormJournalEntry.objects.get(id=ObjectId(entry_id))
            freeform_form = FreeFormJournalEntryForm(initial=entry.to_dict())
            guided_form = GuidedJournalEntryForm(initial=entry.to_dict())
        else:
            return Response({'error': 'Invalid journal entry type'}, status=status.HTTP_400_BAD_REQUEST)

        context = {
            'guided_form': guided_form,
            'freeform_form': freeform_form,
            'entry': entry.to_dict(),
            'entry_id': entry_id,
            'reading_id': entry.readingId if entry and getattr(entry, 'readingId', None) else None,
        }
        return render(request, 'journal/edit_journal.html', context)
    def post(self, request, reading_id, entry_id):
        try:
            data = request.data
            type_str = data.get('type')
            try:
                type_enum = JournalEntryType[type_str]
            except (KeyError, TypeError):
                return Response({'error': f'Invalid journal entry type: {type_str}'}, status=status.HTTP_400_BAD_REQUEST)

            if type_enum == JournalEntryType.FREEFORM:
                content = data.get('content')
                entry = update_journal_entry(entry_id, type_enum, content)
                return redirect(f"/readings/{reading_id}/")

            if type_enum == JournalEntryType.GUIDED:
                kwargs = {
                    'feel': data.get('feel'),
                    'notice': data.get('notice'),
                    'connect': data.get('connect'),
                    'context': data.get('context'),
                    'action': data.get('action')
                }
                entry = update_journal_entry(entry_id, type_enum, **kwargs)
                return redirect(f"/readings/{reading_id}/")

            return Response({'error': 'Invalid journal entry type.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        