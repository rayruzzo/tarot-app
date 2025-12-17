from datetime import datetime
from .tarot import getReadingById
from ..models import JournalEntryType, GuidedJournalEntry, FreeFormJournalEntry


def create_journal_entry(readingId, entry_type, **kwargs):
    date = datetime.now().date()
    reading = getReadingById(readingId)
    try:
        existing = None
        if entry_type == JournalEntryType.GUIDED:
            existing = GuidedJournalEntry.objects(readingId=str(reading.id)).first()
        elif entry_type == JournalEntryType.FREEFORM:
            existing = FreeFormJournalEntry.objects(readingId=readingId).first()
        if existing:
            return {"status": "exists", "data": existing}

        if entry_type == JournalEntryType.GUIDED:
            journal = GuidedJournalEntry(
                created_at=date,
                updated_at=date,
                readingId=str(reading.id),
                type=entry_type.value,
                feel=kwargs['feel'],
                notice=kwargs['notice'],
                connect=kwargs['connect'],
                context=kwargs['context'],
                action=kwargs['action'],            
            )
        elif entry_type == JournalEntryType.FREEFORM:
            journal = FreeFormJournalEntry(
                created_at=date,
                updated_at=date,
                readingId=readingId,
                type=entry_type.value,
                content=kwargs['content']
            )
        else:
            return {"status": "error", "message": "Unknown journal entry type."}
        journal.save()
        reading.journal = journal
        reading.save()
        return {"status": "success", "data": journal}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def update_journal_entry(entry_id, entry_type, **kwargs):
    try:
        if entry_type == JournalEntryType.GUIDED:
            journal = GuidedJournalEntry.objects.get(id=entry_id)
            journal.feel = kwargs.get('feel', journal.feel)
            journal.notice = kwargs.get('notice', journal.notice)
            journal.connect = kwargs.get('connect', journal.connect)
            journal.context = kwargs.get('context', journal.context)
            journal.action = kwargs.get('action', journal.action)
        elif entry_type == JournalEntryType.FREEFORM:
            journal = FreeFormJournalEntry.objects.get(id=entry_id)
            journal.content = kwargs.get('content', journal.content)
        journal.updated_at = datetime.now().date()
        journal.save()
        return {"status": "success", "data": journal}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def delete_journal_entry(entry_id, entry_type):
    try:
        if entry_type == JournalEntryType.GUIDED:
            journal = GuidedJournalEntry.objects.get(id=entry_id)
        elif entry_type == JournalEntryType.FREEFORM:
            journal = FreeFormJournalEntry.objects.get(id=entry_id)
        journal.delete()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def get_journal_entry(readingId):
    try:
        guided_entries = GuidedJournalEntry.objects.filter(readingId=readingId)
        freeform_entries = FreeFormJournalEntry.objects.filter(readingId=readingId)
        entries = list(guided_entries) + list(freeform_entries)

        return {"status": "success", "data": entries[0]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def get_all_journal_entries(user_id):
    try:
        guided_entries = GuidedJournalEntry.objects.filter(readingId__userId=user_id)
        freeform_entries = FreeFormJournalEntry.objects.filter(readingId__userId=user_id)
        entries = list(guided_entries) + list(freeform_entries)
        if n:
            entries = entries[:n]   
        return {"status": "success", "data": entries}
    except Exception as e:
        return {"status": "error", "message": str(e)}