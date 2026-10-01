"""
Defines managers for resources of the RedmineUP plugins (CRM, Helpdesk, Agile, Checklists, Questions).
"""

from .. import exceptions
from . import ResourceManager


class ContactManager(ResourceManager):
    def _move_avatar(self, request, container):
        # The plugin replaces the previous avatar only when the new one comes in top-level attachments,
        # which it iterates as a form style hash, an array makes it crash after saving
        avatar = request[container].pop('avatar', None)

        if avatar is not None:
            request['attachments'] = {'1': avatar}

        return request

    def _prepare_create_request(self, request):
        return self._move_avatar(super()._prepare_create_request(request), self.container)

    def _prepare_update_request(self, request):
        return self._move_avatar(super()._prepare_update_request(request), self.container)


class NoteManager(ResourceManager):
    def _merge_note_time(self, request):
        # The plugin has no note_time, it is merged into created_on which is interpreted in user's time zone
        note = request[self.container]
        note_time = note.pop('note_time', None)

        if note_time:
            note['created_on'] = f'{str(note.get("created_on", ""))[:10]} {note_time}'.strip()

        return request

    def _prepare_create_request(self, request):
        return self._merge_note_time(super()._prepare_create_request(request))

    def _prepare_update_request(self, request):
        return self._merge_note_time(super()._prepare_update_request(request))


class TicketManager(ResourceManager):
    send_as = {'1': 'auto_answer', '2': 'initial_message'}

    def _prepare_create_request(self, request):
        request = super()._prepare_create_request(request)
        ticket = request[self.container]

        # Helpdesk ticket API knows send_as only, helpdesk_send_as is what core issue API expects
        if 'helpdesk_send_as' in ticket:
            send_as = str(ticket.pop('helpdesk_send_as'))
            ticket['send_as'] = self.send_as.get(send_as, send_as)

        # ticket_time only adjusts an already assigned ticket_date, so it has to come last
        if 'ticket_time' in ticket:
            ticket['ticket_time'] = ticket.pop('ticket_time')

        return request

    def _process_update_response(self, request, response):
        # Ticket update answers with the ticket, Pro Edition returned True
        return True if response is not None else response


class AgileSprintManager(ResourceManager):
    def update(self, resource_id, **fields):
        """
        Updates a sprint. The plugin answers with a redirect to the HTML page of the sprint, which is not
        followed, but treated as success.
        """
        if not fields:
            return super().update(resource_id, **fields)

        engine = self.redmine.engine
        original = engine.requests.get('allow_redirects')
        engine.requests['allow_redirects'] = False

        try:
            return super().update(resource_id, **fields)
        except exceptions.UnknownError as e:
            if e.status_code in (301, 302, 303):
                return True
            raise
        finally:
            if original is None:
                engine.requests.pop('allow_redirects', None)
            else:
                engine.requests['allow_redirects'] = original
