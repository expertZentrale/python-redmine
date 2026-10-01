"""
Defines managers for resources of the redmine_expert_helpdesk and redmine_expert_agile plugins.
"""

from . import ResourceManager


class HelpdeskTicketManager(ResourceManager):
    def _process_get_response(self, request, response):
        # Ticket show always emits an empty messages array unless include=messages was requested,
        # we drop it so that accessing ticket.messages lazily loads them via the include mechanism
        if 'messages' not in str(request.get('include', '')).split(','):
            response[self.container].pop('messages', None)

        return super()._process_get_response(request, response)


class HelpdeskMailboxManager(ResourceManager):
    def test_connection(self, mailbox_id):
        """
        Tests mailbox connection and returns connection test result dict, failed tests are returned
        with ``ok`` set to False instead of raising an exception.

        :param int mailbox_id: (required). Mailbox id.
        """
        engine = self.redmine.engine
        url = f'{self.redmine.url}{self.resource_class.query_one.format(mailbox_id)[:-5]}/test_connection.json'
        response = engine.session.request('post', url, **engine.construct_request_kwargs('post', None, None, {}))

        if response.status_code == 422:
            try:
                return response.json()['connection_test']
            except (ValueError, TypeError, KeyError):
                pass

        result = engine.process_response(response)
        return result['connection_test'] if isinstance(result, dict) else result


class HelpdeskProjectSettingManager(ResourceManager):
    def _prepare_update_request(self, request):
        request = super()._prepare_update_request(request)

        # SLA priority overrides are expected as a sibling of the settings container
        if 'sla_priorities' in request[self.container]:
            request['sla_priorities'] = request[self.container].pop('sla_priorities')

        return request

    def _process_update_response(self, request, response):
        if isinstance(response, dict) and self.container in response:
            return self.to_resource(response[self.container])

        return response
