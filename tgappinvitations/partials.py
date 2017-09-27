from tg import expose

@expose('tgappinvitations.templates.little_partial')
def something(name):
    return dict(name=name)