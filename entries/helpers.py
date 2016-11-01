from flask import render_template, request, g
from models import Entry, Tag

def object_list(template_name, query, paginate_by=20, **context):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    object_list = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list, **context)

def entry_list(template, query, **context):
    query = filter_status_by_user(query)

    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
    query = query.filter(Entry.status.in_(valid_statuses)) 
    if request.args.get('q'):
        query = query.filter(
            (Entry.body.contains(search)) |
            (Entry.title.contains(search))
        )
    return object_list(template, query, **context)

def get_entry_or_404(slug, author=None):
    query = Entry.query.filter(Entry.slug == slug)
    if author:
        query = query.filter(Entry.author == author)
    else:
        query = filter_status_by_user(query)
    return query.first_or_404()

def filter_status_by_user(query):
    if not g.user.is_authenticated:
        return query.filter(Entry.status == Entry.STATUS_PUBLIC)
    else:
        # Allow user to view their own drafts.
        query = query.filter(
            (Entry.status == Entry.STATUS_PUBLIC) |
            ((Entry.author == g.user) & (Entry.status != Entry.STATUS_DELETED))
        )
        return query