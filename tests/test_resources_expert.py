import datetime
import json

from redminelib import exceptions, managers, resources

from . import BaseRedmineTestCase, mock
from .responses.expert import responses


class ExpertResourcesTestCase(BaseRedmineTestCase):
    def assertRequest(self, method, path, params=None):
        args, kwargs = self.patch_requests.call_args
        self.assertEqual(args[0], method)
        self.assertEqual(args[1], f'{self.url}{path}')

        if params is not None:
            self.assertEqual(kwargs['params'], params)

    def request_data(self):
        return json.loads(self.patch_requests.call_args[1]['data'])

    def test_requirements(self):
        self.response.status_code = 404

        for name, plugin in (
            ('helpdesk_contact', 'redmine_expert_helpdesk'),
            ('helpdesk_ticket', 'redmine_expert_helpdesk'),
            ('helpdesk_mailbox', 'redmine_expert_helpdesk'),
            ('helpdesk_project_setting', 'redmine_expert_helpdesk'),
            ('expert_agile_data', 'redmine_expert_agile'),
        ):
            with self.assertRaises(exceptions.ResourceRequirementsError) as cm:
                getattr(self.redmine, name).get(1)

            self.assertIn(f'{plugin} >= ', str(cm.exception))

        with self.assertRaises(exceptions.ResourceRequirementsError):
            self.redmine.expert_agile_sprint.get(1, project_id=1)

        with self.assertRaises(exceptions.ResourceRequirementsError):
            list(self.redmine.helpdesk_ticket.filter(project_id=1))

    def test_redmine_version(self):
        self.redmine.ver = (4, 2, 0)

        with self.assertRaises(exceptions.ResourceVersionMismatchError):
            self.redmine.helpdesk_ticket  # noqa: B018

    # HelpdeskContact

    def test_helpdesk_contact_get(self):
        self.response.json.return_value = responses['helpdesk_contact']['get']
        contact = self.redmine.helpdesk_contact.get(1)
        self.assertRequest('get', '/helpdesk/contacts/1.json')
        self.assertEqual(contact.email, 'jane@example.com')
        self.assertIsInstance(contact.project, resources.Project)
        self.assertEqual(contact.project.id, 1)
        self.assertIsInstance(contact.created_on, datetime.datetime)
        self.assertEqual(repr(contact), '<redminelib.resources.HelpdeskContact #1 "Jane Doe">')

    def test_helpdesk_contact_filter(self):
        self.response.json.return_value = responses['helpdesk_contact']['filter']
        contacts = self.redmine.helpdesk_contact.filter(project_id='support', search='acme')
        self.assertEqual([c.id for c in contacts], [1, 2])
        self.assertRequest('get', '/projects/support/helpdesk/contacts.json')
        self.assertEqual(self.patch_requests.call_args[1]['params']['search'], 'acme')
        self.assertEqual(repr(contacts[1]), '<redminelib.resources.HelpdeskContact #2 "john@example.com">')

    def test_helpdesk_contact_filter_requires_project(self):
        self.assertRaises(exceptions.ResourceFilterError, lambda: self.redmine.helpdesk_contact.filter(email='x'))
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.helpdesk_contact.all())

    def test_helpdesk_contact_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['helpdesk_contact']['get']
        contact = self.redmine.helpdesk_contact.create(project_id='support', email='jane@example.com', name='Jane')
        self.assertRequest('post', '/projects/support/helpdesk/contacts.json')
        self.assertEqual(self.request_data(), {'helpdesk_contact': {'email': 'jane@example.com', 'name': 'Jane'}})
        self.assertEqual(contact.id, 1)

    def test_helpdesk_contact_update(self):
        self.response.json.return_value = responses['helpdesk_contact']['get']
        contact = self.redmine.helpdesk_contact.get(1)
        self.response.content = ''
        contact.phone = '+49 999'
        contact.save()
        self.assertRequest('put', '/helpdesk/contacts/1.json')
        self.assertEqual(self.request_data(), {'helpdesk_contact': {'phone': '+49 999'}})

        with self.assertRaises(exceptions.ReadonlyAttrError):
            contact.email = 'other@example.com'

    def test_helpdesk_contact_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.helpdesk_contact.delete(1), True)
        self.assertRequest('delete', '/helpdesk/contacts/1.json')

    # HelpdeskTicket

    def test_helpdesk_ticket_custom_manager(self):
        self.assertIsInstance(self.redmine.helpdesk_ticket, managers.HelpdeskTicketManager)

    def test_helpdesk_ticket_get(self):
        self.response.json.return_value = responses['helpdesk_ticket']['get']
        ticket = self.redmine.helpdesk_ticket.get(42)
        self.assertRequest('get', '/helpdesk/tickets/42.json')
        self.assertEqual(ticket.subject, 'Printer on fire')
        self.assertIsInstance(ticket.status, resources.IssueStatus)
        self.assertIsInstance(ticket.priority, resources.Enumeration)
        self.assertIsInstance(ticket.author, resources.User)
        self.assertIsInstance(ticket.contact, resources.HelpdeskContact)
        self.assertEqual(ticket.contact.email, 'jane@example.com')
        self.assertIsInstance(ticket.mailbox, resources.HelpdeskMailbox)
        self.assertEqual(ticket.mailbox.address, 'support@example.com')
        self.assertEqual(ticket.sla['reaction']['status'], 'running')
        self.assertEqual(ticket.url, f'{self.url}/issues/42')

    def test_helpdesk_ticket_messages_lazy_include(self):
        self.response.json.return_value = responses['helpdesk_ticket']['get']
        ticket = self.redmine.helpdesk_ticket.get(42)
        self.assertIsNone(ticket.raw()['messages'])
        self.response.json.return_value = responses['helpdesk_ticket']['get_messages']
        self.assertEqual(ticket.messages[0]['direction'], 'in')
        self.assertRequest('get', '/helpdesk/tickets/42.json', params={'include': 'messages'})

    def test_helpdesk_ticket_get_with_messages(self):
        self.response.json.return_value = responses['helpdesk_ticket']['get_messages']
        ticket = self.redmine.helpdesk_ticket.get(42, include=['messages'])
        self.assertEqual(self.patch_requests.call_count, 1)
        self.assertEqual(ticket.messages[0]['id'], 9)
        self.assertEqual(self.patch_requests.call_count, 1)

    def test_helpdesk_ticket_filter(self):
        self.response.json.return_value = responses['helpdesk_ticket']['filter']
        tickets = self.redmine.helpdesk_ticket.filter(project_id=1)
        self.assertEqual([t.id for t in tickets], [42, 41])
        self.assertRequest('get', '/projects/1/helpdesk/tickets.json')

    def test_helpdesk_ticket_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['helpdesk_ticket']['get']
        ticket = self.redmine.helpdesk_ticket.create(
            project_id='support', subject='Printer on fire', contact_email='jane@example.com', contact_name='Jane'
        )
        self.assertRequest('post', '/projects/support/helpdesk/tickets.json')
        self.assertEqual(
            self.request_data(),
            {
                'helpdesk_ticket': {
                    'subject': 'Printer on fire',
                    'contact_email': 'jane@example.com',
                    'contact_name': 'Jane',
                }
            },
        )
        self.assertEqual(ticket.id, 42)

    def test_helpdesk_ticket_update(self):
        self.response.json.return_value = responses['helpdesk_ticket']['get']
        ticket = self.redmine.helpdesk_ticket.get(42)
        self.response.content = ''
        ticket.save(status_id=2, contact_id=3, notes='Replaced toner')
        self.assertRequest('put', '/helpdesk/tickets/42.json')
        self.assertEqual(
            self.request_data(), {'helpdesk_ticket': {'status_id': 2, 'contact_id': 3, 'notes': 'Replaced toner'}}
        )

        with self.assertRaises(exceptions.ReadonlyAttrError):
            ticket.sla = {}

    def test_helpdesk_ticket_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.helpdesk_ticket.delete(42), True)
        self.assertRequest('delete', '/helpdesk/tickets/42.json')

    def test_helpdesk_ticket_issue(self):
        self.response.json.return_value = responses['helpdesk_ticket']['get']
        ticket = self.redmine.helpdesk_ticket.get(42)
        self.response.json.return_value = {'issue': {'id': 42, 'subject': 'Printer on fire'}}
        self.assertIsInstance(ticket.issue, resources.Issue)
        self.assertRequest('get', '/issues/42.json')

    # HelpdeskMailbox

    def test_helpdesk_mailbox_get(self):
        self.response.json.return_value = responses['helpdesk_mailbox']['get']
        mailbox = self.redmine.helpdesk_mailbox.get(7)
        self.assertRequest('get', '/helpdesk/mailboxes/7.json')
        self.assertEqual(mailbox.available_reply_transports, ['provider', 'smtp'])
        self.assertEqual(repr(mailbox), '<redminelib.resources.HelpdeskMailbox #7 "support@example.com">')

    def test_helpdesk_mailbox_filter(self):
        self.response.json.return_value = responses['helpdesk_mailbox']['filter']
        mailboxes = self.redmine.helpdesk_mailbox.filter(project_id=1, enabled=True)
        self.assertEqual(len(mailboxes), 2)
        self.assertRequest('get', '/projects/1/helpdesk/mailboxes.json')

    def test_helpdesk_mailbox_create_update_delete(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['helpdesk_mailbox']['get']
        mailbox = self.redmine.helpdesk_mailbox.create(
            project_id=1, mailbox_address='support@example.com', provider='imap', mail_password='secret'
        )
        self.assertRequest('post', '/projects/1/helpdesk/mailboxes.json')
        self.assertEqual(self.request_data()['helpdesk_mailbox']['mail_password'], 'secret')
        self.response.status_code = 204
        self.response.content = ''
        mailbox.save(enabled=False)
        self.assertRequest('put', '/helpdesk/mailboxes/7.json')
        self.assertEqual(mailbox.delete(), True)
        self.assertRequest('delete', '/helpdesk/mailboxes/7.json')

        with self.assertRaises(exceptions.ReadonlyAttrError):
            mailbox.mail_password_set = False

    def test_helpdesk_mailbox_test_connection(self):
        self.response.json.return_value = responses['helpdesk_mailbox']['get']
        mailbox = self.redmine.helpdesk_mailbox.get(7)
        self.response.json.return_value = responses['helpdesk_mailbox']['test_connection_ok']
        result = mailbox.test_connection()
        self.assertRequest('post', '/helpdesk/mailboxes/7/test_connection.json')
        self.assertEqual(result, {'ok': True, 'message': 'OK', 'folders': ['INBOX', 'Sent']})

    def test_helpdesk_mailbox_test_connection_failed(self):
        self.response.status_code = 422
        self.response.json.return_value = responses['helpdesk_mailbox']['test_connection_failed']
        result = self.redmine.helpdesk_mailbox.test_connection(7)
        self.assertEqual(result, {'ok': False, 'message': 'Authentication failed'})

    def test_helpdesk_mailbox_test_connection_errors(self):
        self.response.status_code = 403
        self.assertRaises(exceptions.ForbiddenError, lambda: self.redmine.helpdesk_mailbox.test_connection(7))
        self.response.status_code = 422
        self.response.json.return_value = {'errors': ['Mailbox is invalid']}
        self.assertRaises(exceptions.ValidationError, lambda: self.redmine.helpdesk_mailbox.test_connection(7))

    # HelpdeskProjectSetting

    def test_helpdesk_project_setting_get(self):
        self.response.json.return_value = responses['helpdesk_project_setting']['get']
        setting = self.redmine.helpdesk_project_setting.get('support')
        self.assertRequest('get', '/projects/support/helpdesk/settings.json')
        self.assertEqual(setting.project_id, 1)
        self.assertEqual(setting.internal_id, 1)
        self.assertFalse(setting.is_new())
        self.assertEqual(setting.sla_work_days, '1,2,3,4,5')
        self.assertEqual(setting.sla_priorities[0]['priority_id'], 2)
        self.assertEqual(repr(setting), '<redminelib.resources.HelpdeskProjectSetting #1>')

    def test_helpdesk_project_setting_update(self):
        self.response.json.return_value = responses['helpdesk_project_setting']['get']
        setting = self.redmine.helpdesk_project_setting.update(
            'support',
            sla_enabled=False,
            sla_priorities=[{'priority_id': 2, 'reaction_minutes': 30, 'solution_minutes': None}],
        )
        self.assertRequest('put', '/projects/support/helpdesk/settings.json')
        self.assertEqual(
            self.request_data(),
            {
                'helpdesk_project_setting': {'sla_enabled': False},
                'sla_priorities': [{'priority_id': 2, 'reaction_minutes': 30, 'solution_minutes': None}],
            },
        )
        self.assertIsInstance(setting, resources.HelpdeskProjectSetting)

    def test_helpdesk_project_setting_update_without_body(self):
        self.response.status_code = 204
        self.response.content = ''
        self.assertEqual(self.redmine.helpdesk_project_setting.update(1, sla_enabled=True), True)

    def test_helpdesk_project_setting_save(self):
        self.response.json.return_value = responses['helpdesk_project_setting']['get']
        setting = self.redmine.helpdesk_project_setting.get('support')
        setting.save(send_reply_by_default=False)
        self.assertRequest('put', '/projects/1/helpdesk/settings.json')
        self.assertEqual(self.request_data(), {'helpdesk_project_setting': {'send_reply_by_default': False}})

    def test_helpdesk_project_setting_unsupported_methods(self):
        manager = self.redmine.helpdesk_project_setting
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: manager.all())
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: manager.create(foo=1))
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: manager.delete(1))

    # Core issue extensions

    def test_issue_create_with_helpdesk_init(self):
        self.response.status_code = 201
        self.response.json.return_value = {'issue': {'id': 1, 'subject': 'Foo'}}
        self.redmine.issue.create(
            project_id=1,
            subject='Foo',
            helpdesk_init={'contact_email': 'jane@example.com', 'mailbox_id': 7, 'send_mail': True},
        )
        self.assertEqual(
            self.request_data(),
            {
                'issue': {'subject': 'Foo'},
                'helpdesk_init': {'contact_email': 'jane@example.com', 'mailbox_id': 7, 'send_mail': '1'},
            },
        )

    def test_issue_create_with_helpdesk_init_without_mail(self):
        self.response.status_code = 201
        self.response.json.return_value = {'issue': {'id': 1, 'subject': 'Foo'}}
        self.redmine.issue.create(project_id=1, subject='Foo', helpdesk_init={'send_mail': False})
        self.assertEqual(self.request_data()['helpdesk_init'], {'send_mail': '0'})

    def test_issue_create_with_expert_agile_data_attributes(self):
        self.response.status_code = 201
        self.response.json.return_value = {'issue': {'id': 1, 'subject': 'Foo'}}
        self.redmine.issue.create(
            project_id=1, subject='Foo', expert_agile_data_attributes={'story_points': 5, 'sprint_id': 3}
        )
        self.assertEqual(
            self.request_data()['issue']['expert_agile_data_attributes'], {'story_points': 5, 'sprint_id': 3}
        )

    # ExpertAgileSprint

    def test_expert_agile_sprint_get(self):
        self.response.json.return_value = responses['expert_agile_sprint']['get']
        sprint = self.redmine.expert_agile_sprint.get(3, project_id='scrum')
        self.assertRequest('get', '/projects/scrum/expert_agile_sprints/3.json')
        self.assertEqual(sprint.status, 'active')
        self.assertEqual(sprint.sharing, 'none')
        self.assertEqual(sprint.start_date, datetime.date(2026, 1, 5))
        self.assertEqual(sprint.story_points, 13)
        self.assertEqual(sprint.url, f'{self.url}/projects/1/expert_agile_sprints/3')
        self.assertEqual(repr(sprint), '<redminelib.resources.ExpertAgileSprint #3 "Sprint 3">')

    def test_expert_agile_sprint_get_requires_project(self):
        self.assertRaises(exceptions.ValidationError, lambda: self.redmine.expert_agile_sprint.get(3))

    def test_expert_agile_sprint_filter(self):
        self.response.json.return_value = responses['expert_agile_sprint']['filter']
        sprints = self.redmine.expert_agile_sprint.filter(project_id='scrum')
        self.assertEqual([s.id for s in sprints], [3, 2])
        self.assertEqual(sprints.total_count, 2)
        self.assertEqual(sprints[1].sharing, 'tree')
        self.assertRequest('get', '/projects/scrum/expert_agile_sprints.json')

    def test_expert_agile_sprint_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['expert_agile_sprint']['get']
        sprint = self.redmine.expert_agile_sprint.create(
            project_id='scrum',
            name='Sprint 3',
            start_date=datetime.date(2026, 1, 5),
            end_date=datetime.date(2026, 1, 16),
            status='active',
            sharing='none',
        )
        self.assertRequest('post', '/projects/scrum/expert_agile_sprints.json')
        self.assertEqual(
            self.request_data(),
            {
                'expert_agile_sprint': {
                    'name': 'Sprint 3',
                    'start_date': '2026-01-05',
                    'end_date': '2026-01-16',
                    'status': 1,
                    'sharing': 0,
                }
            },
        )
        self.assertEqual(sprint.id, 3)

    def test_expert_agile_sprint_new_save(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['expert_agile_sprint']['get']
        sprint = self.redmine.expert_agile_sprint.new()
        sprint.project_id = 'scrum'
        sprint.name = 'Sprint 3'
        sprint.sharing = 'tree'
        self.assertEqual(sprint.sharing, 'tree')
        sprint.save()
        self.assertRequest('post', '/projects/scrum/expert_agile_sprints.json')
        self.assertEqual(self.request_data(), {'expert_agile_sprint': {'name': 'Sprint 3', 'sharing': 3}})
        self.assertFalse(sprint.is_new())

    def test_expert_agile_sprint_save_uses_own_project(self):
        self.response.json.return_value = responses['expert_agile_sprint']['filter']
        sprint = self.redmine.expert_agile_sprint.filter(project_id='scrum')[1]
        self.response.status_code = 204
        self.response.content = ''
        sprint.save(name='Sprint 2b')
        self.assertRequest('put', '/projects/1/expert_agile_sprints/2.json')
        self.assertEqual(self.request_data(), {'expert_agile_sprint': {'name': 'Sprint 2b'}})

        with self.assertRaises(exceptions.ReadonlyAttrError):
            sprint.project_id = 2

    def test_expert_agile_sprint_activate_and_close(self):
        self.response.json.return_value = responses['expert_agile_sprint']['get']
        sprint = self.redmine.expert_agile_sprint.get(3, project_id=1)
        self.response.status_code = 204
        self.response.content = ''
        sprint.close()
        self.assertEqual(self.request_data(), {'expert_agile_sprint': {'status': 2}})
        self.assertEqual(sprint.status, 'closed')
        sprint.activate()
        self.assertEqual(self.request_data(), {'expert_agile_sprint': {'status': 1}})
        self.assertRequest('put', '/projects/1/expert_agile_sprints/3.json')

    def test_expert_agile_sprint_delete(self):
        self.response.json.return_value = responses['expert_agile_sprint']['get']
        sprint = self.redmine.expert_agile_sprint.get(3, project_id='scrum')
        self.response.status_code = 204
        self.response.content = ''
        self.assertEqual(sprint.delete(), True)
        self.assertRequest('delete', '/projects/1/expert_agile_sprints/3.json')
        self.assertEqual(self.redmine.expert_agile_sprint.delete(3, project_id='scrum'), True)
        self.assertRequest('delete', '/projects/scrum/expert_agile_sprints/3.json')

    def test_expert_agile_sprint_refresh(self):
        self.response.json.return_value = responses['expert_agile_sprint']['filter']
        sprint = self.redmine.expert_agile_sprint.filter(project_id='scrum')[0]
        self.response.json.return_value = responses['expert_agile_sprint']['get']
        sprint.refresh()
        self.assertRequest('get', '/projects/1/expert_agile_sprints/3.json')
        self.assertEqual(sprint.issue_count, 4)

    def test_expert_agile_sprint_unknown_status_passthrough(self):
        self.response.json.return_value = {'expert_agile_sprint': {'id': 3, 'project_id': 1, 'status': 7}}
        sprint = self.redmine.expert_agile_sprint.get(3, project_id=1)
        self.assertEqual(sprint.status, 7)

    # ExpertAgileData

    def test_expert_agile_data_get(self):
        self.response.json.return_value = responses['expert_agile_data']['get']
        data = self.redmine.expert_agile_data.get(42)
        self.assertRequest('get', '/issues/42/expert_agile_data.json')
        self.assertEqual(data.internal_id, 42)
        self.assertEqual(data.story_points, 5)
        self.assertEqual(data.sprint_id, 3)
        self.assertEqual(data.position, '1024.0')
        self.assertFalse(data.is_new())
        self.assertEqual(data.url, f'{self.url}/issues/42')
        self.assertEqual(repr(data), '<redminelib.resources.ExpertAgileData #42>')

    def test_expert_agile_data_empty(self):
        self.response.json.return_value = responses['expert_agile_data']['empty']
        data = self.redmine.expert_agile_data.get(43)
        self.assertIsNone(data.story_points)
        self.assertFalse(data.is_new())

    def test_expert_agile_data_save(self):
        self.response.json.return_value = responses['expert_agile_data']['get']
        data = self.redmine.expert_agile_data.get(42)
        self.response.status_code = 204
        self.response.content = ''
        data.save(story_points=8, sprint_id=None)
        self.assertRequest('put', '/issues/42/expert_agile_data.json')
        self.assertEqual(self.request_data(), {'expert_agile_data': {'story_points': 8, 'sprint_id': None}})

        for attr in ('position', 'issue_id'):
            with self.assertRaises(exceptions.ReadonlyAttrError):
                setattr(data, attr, 1)

    def test_expert_agile_data_update_via_manager(self):
        self.response.status_code = 204
        self.response.content = ''
        self.assertEqual(self.redmine.expert_agile_data.update(42, story_points=3), True)
        self.assertEqual(self.request_data(), {'expert_agile_data': {'story_points': 3}})

    def test_expert_agile_data_unsupported_methods(self):
        manager = self.redmine.expert_agile_data
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: manager.all())
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: manager.filter(issue_id=1))
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: manager.create(issue_id=1))
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: manager.delete(1))

    def test_expert_agile_data_issue(self):
        self.response.json.return_value = responses['expert_agile_data']['get']
        data = self.redmine.expert_agile_data.get(42)
        self.response.json.return_value = {'issue': {'id': 42, 'subject': 'Foo'}}
        self.assertIsInstance(data.issue, resources.Issue)

    @mock.patch('redminelib.resources.expert.ExpertAgileSprint.requirements', [])
    def test_not_found_without_requirements(self):
        self.response.status_code = 404
        self.assertRaises(
            exceptions.ResourceNotFoundError, lambda: self.redmine.expert_agile_sprint.get(1, project_id=1)
        )
