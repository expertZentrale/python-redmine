import datetime
import io
import json

from redminelib import exceptions, managers, resources

from . import BaseRedmineTestCase
from .responses.redmineup import responses


class RedmineUPResourcesTestCase(BaseRedmineTestCase):
    def assertRequest(self, method, path, params=None):
        args, kwargs = self.patch_requests.call_args
        self.assertEqual(args[0], method)
        self.assertEqual(args[1], f'{self.url}{path}')

        if params is not None:
            self.assertEqual(kwargs['params'], params)

    def request_data(self):
        return json.loads(self.patch_requests.call_args[1]['data'])

    def request_params(self):
        return self.patch_requests.call_args[1]['params']

    def test_requirements(self):
        self.response.status_code = 404

        for name, plugin in (
            ('contact', 'redmine_contacts'),
            ('note', 'redmine_contacts'),
            ('deal', 'redmine_contacts'),
            ('ticket', 'redmine_contacts_helpdesk'),
            ('agile_data', 'redmine_agile'),
            ('checklist', 'redmine_checklists'),
        ):
            with self.assertRaises(exceptions.ResourceRequirementsError) as cm:
                getattr(self.redmine, name).get(1)

            self.assertIn(f'{plugin} >= ', str(cm.exception))

        with self.assertRaises(exceptions.ResourceRequirementsError):
            list(self.redmine.questions_status.all())

    # Contact

    def test_contact_custom_manager(self):
        self.assertIsInstance(self.redmine.contact, managers.ContactManager)

    def test_contact_get(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.assertRequest('get', '/contacts/1.json')
        self.assertEqual(repr(contact), '<redminelib.resources.Contact #1 "Ivan Ivanov">')
        self.assertEqual(contact.birthday, datetime.date(1980, 10, 21))
        self.assertIsInstance(contact.assigned_to, resources.User)
        self.assertIsInstance(contact.projects[0], resources.Project)
        self.assertEqual(contact.emails, [{'address': 'ivan@ivanov.com'}])
        self.assertEqual(contact.tag_list, ['vip'])

    def test_contact_includes(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.response.json.return_value = responses['contact']['tickets']
        self.assertIsInstance(contact.tickets[0], resources.Ticket)
        self.assertRequest('get', '/contacts/1.json', params={'include': 'tickets'})
        self.response.json.return_value = {'contact': {'id': 1, 'notes': [{'id': 3, 'content': 'x'}]}}
        self.assertIsInstance(contact.notes[0], resources.Note)

    def test_contact_all_and_filter(self):
        self.response.json.return_value = responses['contact']['filter']
        contacts = self.redmine.contact.all(include=['projects'])
        self.assertEqual(repr(contacts[1]), '<redminelib.resources.Contact #2 "ACME">')
        self.assertRequest('get', '/contacts.json')
        self.assertEqual(self.request_params()['include'], 'projects')
        list(self.redmine.contact.filter(project_id='sales', tags=['vip', 'online'], search='Ivan'))
        self.assertEqual(self.request_params()['tags'], 'vip,online')
        self.assertEqual(self.request_params()['project_id'], 'sales')

    def test_contact_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.create(
            project_id='sales',
            first_name='Ivan',
            phones=['1234567', '7654321'],
            emails=['ivan@ivanov.com'],
            tag_list=['vip'],
            birthday=datetime.date(1980, 10, 21),
        )
        self.assertRequest('post', '/projects/sales/contacts.json')
        self.assertEqual(
            self.request_data(),
            {
                'contact': {
                    'first_name': 'Ivan',
                    'phone': '1234567, 7654321',
                    'email': 'ivan@ivanov.com',
                    'tag_list': ['vip'],
                    'birthday': '1980-10-21',
                }
            },
        )
        self.assertEqual(contact.id, 1)

    def test_contact_avatar_is_sent_as_attachment(self):
        self.response.status_code = 201
        self.response.json.side_effect = [{'upload': {'token': '123456'}}, responses['contact']['get']]
        self.redmine.contact.create(
            project_id=1, first_name='Ivan', avatar={'path': io.BytesIO(b'jpeg'), 'filename': 'ivan.jpg'}
        )
        self.assertEqual(
            self.request_data(),
            {
                'contact': {'first_name': 'Ivan'},
                'attachments': [{'token': '123456', 'filename': 'ivan.jpg', 'description': 'avatar'}],
            },
        )

    def test_contact_update_and_delete(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.response.status_code = 204
        self.response.content = ''
        contact.save(job_title='CEO', avatar={'token': 'abc', 'filename': 'a.png', 'description': 'avatar'})
        self.assertRequest('put', '/contacts/1.json')
        self.assertEqual(
            self.request_data(),
            {
                'contact': {'job_title': 'CEO'},
                'attachments': [{'token': 'abc', 'filename': 'a.png', 'description': 'avatar'}],
            },
        )
        self.assertEqual(contact.delete(), True)
        self.assertRequest('delete', '/contacts/1.json')

    def test_contact_project_add_remove(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.response.status_code = 204
        self.response.content = ''
        self.assertEqual(contact.project.add('vacation'), True)
        self.assertRequest('post', '/contacts/1/projects.json')
        self.assertEqual(self.request_data(), {'project': {'id': 'vacation'}})
        self.assertEqual(contact.project.remove('vacation'), True)
        self.assertRequest('delete', '/contacts/1/projects/vacation.json', params={'project[id]': 'vacation'})

    def test_contact_export_urls(self):
        self.response.json.return_value = responses['contact']['get']
        self.assertEqual(self.redmine.contact.get(1).export_url('vcf'), f'{self.url}/contacts/1.vcf')

    def test_project_and_user_contacts_relations(self):
        self.response.json.return_value = responses['contact']['filter']
        project = self.redmine.project.to_resource({'id': 1, 'name': 'Sales'})
        self.assertEqual(len(project.contacts), 2)
        self.assertEqual(self.request_params()['project_id'], 1)
        user = self.redmine.user.to_resource({'id': 5, 'login': 'jsmith'})
        list(user.contacts)
        self.assertEqual(self.request_params()['assigned_to_id'], 5)

    # ContactTag

    def test_contact_tag_all_and_get(self):
        self.response.json.return_value = responses['contact_tag']['all']
        tags = self.redmine.contact_tag.all()
        self.assertEqual([t.name for t in tags], ['vip', 'online'])
        self.assertRequest('get', '/contacts_tags.json')
        self.assertEqual(self.redmine.contact_tag.get(2).name, 'online')
        self.assertRaises(exceptions.ResourceNotFoundError, lambda: self.redmine.contact_tag.get(99))

    def test_contact_tag_contacts(self):
        self.response.json.return_value = responses['contact_tag']['all']
        tag = self.redmine.contact_tag.get(1)
        self.response.json.return_value = responses['contact']['filter']
        list(tag.contacts)
        self.assertEqual(self.request_params()['tags'], 'vip')

    # Note

    def test_note_get(self):
        self.response.json.return_value = responses['note']['get']
        note = self.redmine.note.get(1)
        self.assertRequest('get', '/notes/1.json')
        self.assertEqual(
            note.created_on,
            datetime.datetime(2023, 1, 10, 11, 11, tzinfo=datetime.timezone(datetime.timedelta(hours=1))),
        )
        self.assertIsInstance(note.source, resources.Contact)
        self.assertEqual(note.source.id, 1)
        self.assertIsInstance(note.author, resources.User)

    def test_note_dates_in_configured_timezone(self):
        self.redmine.timezone = datetime.timezone.utc
        self.response.json.return_value = responses['note']['get']
        self.assertEqual(
            self.redmine.note.get(1).created_on, datetime.datetime(2023, 1, 10, 10, 11, tzinfo=datetime.timezone.utc)
        )

    def test_contact_avatar_content_type(self):
        self.response.status_code = 201
        self.response.json.side_effect = [{'upload': {'token': '1'}}, responses['contact']['get']]
        self.redmine.contact.create(
            project_id=1, first_name='Ivan', avatar={'path': io.BytesIO(b'png'), 'content_type': 'image/png'}
        )
        self.assertEqual(
            self.request_data()['attachments'],
            [{'token': '1', 'filename': 'avatar', 'description': 'avatar', 'content_type': 'image/png'}],
        )

    def test_note_unknown_source_type_and_bad_date(self):
        self.response.json.return_value = {
            'note': {'id': 1, 'source': {'id': 1, 'type': 'Invoice2'}, 'created_on': 'Tue, xx'}
        }
        note = self.redmine.note.get(1)
        self.assertEqual(note.source, {'id': 1, 'type': 'Invoice2'})
        self.assertEqual(note.created_on, 'Tue, xx')

    def test_note_create_merges_note_time(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['note']['get']
        self.redmine.note.create(
            project_id='sales',
            source_type='Contact',
            source_id=1,
            content='Called him',
            type_id=1,
            created_on=datetime.date(2023, 1, 10),
            note_time='11:11',
        )
        self.assertRequest('post', '/notes.json')
        self.assertEqual(
            self.request_data(),
            {
                'note': {
                    'project_id': 'sales',
                    'source_type': 'Contact',
                    'source_id': 1,
                    'content': 'Called him',
                    'type_id': 1,
                    'created_on': '2023-01-10 11:11',
                }
            },
        )

    def test_note_update_delete(self):
        self.response.json.return_value = responses['note']['get']
        note = self.redmine.note.get(1)
        self.response.status_code = 204
        self.response.content = ''
        note.save(subject='Meeting')
        self.assertRequest('put', '/notes/1.json')
        self.assertEqual(self.request_data(), {'note': {'subject': 'Meeting'}})
        self.assertEqual(self.redmine.note.delete(1), True)

    def test_note_unsupported(self):
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.note.all())

    # Deal

    def test_deal_get(self):
        self.response.json.return_value = responses['deal']['get']
        deal = self.redmine.deal.get(1)
        self.assertRequest('get', '/deals/1.json')
        self.assertIsInstance(deal.status, resources.DealStatus)
        self.assertIsInstance(deal.category, resources.DealCategory)
        self.assertIsInstance(deal.contact, resources.Contact)
        self.assertIsInstance(deal.related_contacts[0], resources.Contact)
        self.assertEqual(deal.due_date, datetime.date(2026, 12, 12))

    def test_deal_all_includes_closed(self):
        self.response.json.return_value = responses['deal']['filter']
        list(self.redmine.deal.all())
        self.assertRequest('get', '/deals.json?status_id=*')

    def test_deal_filter(self):
        self.response.json.return_value = responses['deal']['filter']
        list(self.redmine.deal.filter(project_id='sales', status_id=1, search='big'))
        self.assertRequest('get', '/deals.json')
        self.assertEqual(self.request_params()['status_id'], 1)

    def test_deal_create_sends_price_as_string(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['deal']['get']
        self.redmine.deal.create(project_id='sales', name='Big deal', price=1000, due_date=datetime.date(2026, 12, 12))
        self.assertRequest('post', '/projects/sales/deals.json')
        self.assertEqual(self.request_data(), {'deal': {'name': 'Big deal', 'price': '1000', 'due_date': '2026-12-12'}})

    def test_deal_update_delete_and_notes(self):
        self.response.json.return_value = responses['deal']['get']
        deal = self.redmine.deal.get(1)
        self.response.json.return_value = {'deal': {'id': 1, 'notes': [{'id': 3, 'content': 'x'}]}}
        self.assertIsInstance(deal.notes[0], resources.Note)
        self.response.status_code = 204
        self.response.content = ''
        deal.save(status_id=2, probability=100)
        self.assertEqual(self.request_data(), {'deal': {'status_id': 2, 'probability': 100}})
        self.assertEqual(deal.delete(), True)
        self.assertRequest('delete', '/deals/1.json')

    def test_deal_relations(self):
        self.response.json.return_value = responses['deal']['filter']
        project = self.redmine.project.to_resource({'id': 1, 'name': 'Sales'})
        list(project.deals)
        self.assertEqual(self.request_params()['project_id'], 1)
        user = self.redmine.user.to_resource({'id': 5, 'login': 'jsmith'})
        list(user.deals)
        self.assertEqual(self.request_params()['assigned_to_id'], 5)

    # DealStatus / DealCategory / CrmQuery

    def test_deal_status(self):
        self.response.json.return_value = responses['deal_status']['all']
        statuses = self.redmine.deal_status.all()
        self.assertEqual(len(statuses), 2)
        self.assertRequest('get', '/deal_statuses.json')
        status = self.redmine.deal_status.get(2)
        self.assertEqual(status.name, 'Won')
        self.assertEqual(resources.DealStatus.statuses[status.status_type], 'won')
        self.response.json.return_value = responses['deal']['filter']
        list(statuses[0].deals)
        self.assertEqual(self.request_params()['status_id'], 1)

    def test_deal_category(self):
        self.response.json.return_value = responses['deal_category']['filter']
        categories = self.redmine.deal_category.filter(project_id='sales')
        self.assertEqual(len(categories), 2)
        self.assertRequest('get', '/projects/sales/deal_categories.json')
        category = self.redmine.deal_category.get(2, project_id='sales')
        self.assertEqual(category.name, 'Software')
        self.response.json.return_value = responses['deal']['filter']
        list(category.deals)
        self.assertEqual(self.request_params()['category_id'], 2)
        self.assertEqual(self.request_params()['status_id'], '*')

    def test_deal_category_create_update_delete(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['deal_category']['create']
        category = self.redmine.deal_category.create(project_id='sales', name='Consulting')
        self.assertRequest('post', '/projects/sales/deal_categories.json')
        self.assertEqual(self.request_data(), {'category': {'name': 'Consulting'}})
        self.assertEqual(category.id, 3)
        self.response.status_code = 204
        self.response.content = ''
        category.save(name='Advisory')
        self.assertRequest('put', '/deal_categories/3.json')
        self.assertEqual(self.request_data(), {'category': {'name': 'Advisory'}})
        self.assertEqual(self.redmine.deal_category.delete(3, reassign_to_id=1), True)
        self.assertRequest('delete', '/deal_categories/3.json', params={'reassign_to_id': 1})

    def test_project_deal_categories_relation(self):
        self.response.json.return_value = responses['deal_category']['filter']
        project = self.redmine.project.to_resource({'id': 1, 'identifier': 'sales'})
        self.assertEqual(len(project.deal_categories), 2)
        self.assertRequest('get', '/projects/1/deal_categories.json')

    def test_crm_query(self):
        self.response.json.return_value = responses['crm_query']['filter']
        queries = self.redmine.crm_query.filter(resource='deal')
        self.assertEqual(len(queries), 2)
        self.assertRequest('get', '/crm_queries.json?object_type=deal')
        query = self.redmine.crm_query.get(2, resource='contact')
        self.assertEqual(query.name, 'Mine')
        self.response.json.return_value = responses['contact']['filter']
        list(query.contacts)
        self.assertEqual(self.request_params()['query_id'], 2)
        self.assertEqual(self.request_params()['project_id'], 3)
        self.response.json.return_value = responses['deal']['filter']
        list(queries[0].deals)
        self.assertNotIn('project_id', self.request_params())

    # Ticket / TicketJournal

    def test_ticket_custom_manager(self):
        self.assertIsInstance(self.redmine.ticket, managers.TicketManager)

    def test_ticket_get(self):
        self.response.json.return_value = responses['ticket']['get']
        ticket = self.redmine.ticket.get(42)
        self.assertRequest('get', '/helpdesk_tickets/42.json')
        self.assertEqual(ticket.ticket_date, datetime.date(2023, 1, 10))
        self.assertIsInstance(ticket.contact, resources.Contact)
        self.assertEqual(ticket.url, f'{self.url}/issues/42')
        self.response.json.return_value = {'issue': {'id': 42, 'subject': 'Foo'}}
        self.assertIsInstance(ticket.issue, resources.Issue)

    def test_ticket_journals(self):
        self.response.json.return_value = responses['ticket']['journals']
        ticket = self.redmine.ticket.get(42, include=['journals', 'journal_messages'])
        self.assertEqual(self.request_params()['include'], 'journals,journal_messages')
        self.assertIsInstance(ticket.journals[0], resources.TicketJournal)
        self.assertEqual(ticket.journal_messages[0]['journal_id'], 7)
        self.response.status_code = 204
        self.response.content = ''
        ticket.journals[0].save(notes='new notes')
        self.assertRequest('put', '/journals/7.json')
        self.assertEqual(self.request_data(), {'journal': {'notes': 'new notes'}})

    def test_ticket_all_filter(self):
        self.response.json.return_value = responses['ticket']['filter']
        self.assertEqual(len(self.redmine.ticket.all(limit=50)), 2)
        self.assertRequest('get', '/helpdesk_tickets.json')
        list(self.redmine.ticket.filter(source='phone', from_address='client@mail.com'))
        self.assertEqual(self.request_params()['source'], 2)

    def test_ticket_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['ticket']['get']
        self.redmine.ticket.create(
            ticket_time='10:01',
            source='2',
            helpdesk_send_as='2',
            ticket_date=datetime.date(2023, 1, 10),
            cc_address=['a@b.c', 'd@e.f'],
            issue={'project_id': 'helpdesk', 'subject': 'ticket subject', 'tracker_id': 6},
            contact={'email': 'client@mail.com'},
        )
        self.assertRequest('post', '/helpdesk_tickets.json')
        data = self.request_data()['helpdesk_ticket']
        self.assertEqual(data['send_as'], 'initial_message')
        self.assertNotIn('helpdesk_send_as', data)
        self.assertEqual(data['ticket_date'], '2023-01-10')
        self.assertEqual(data['cc_address'], 'a@b.c,d@e.f')
        self.assertEqual(list(data)[-1], 'ticket_time')

    def test_ticket_new_save(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['ticket']['get']
        ticket = self.redmine.ticket.new()
        ticket.issue = {'project_id': 'helpdesk', 'subject': 'ticket subject'}
        ticket.contact = {'email': 'client@mail.com'}
        ticket.helpdesk_send_as = '1'
        self.assertEqual(ticket.issue, {'project_id': 'helpdesk', 'subject': 'ticket subject'})
        ticket.save()
        self.assertEqual(self.request_data()['helpdesk_ticket']['send_as'], 'auto_answer')
        self.assertEqual(ticket.id, 42)

    def test_ticket_update_delete(self):
        self.response.json.return_value = responses['ticket']['get']
        ticket = self.redmine.ticket.get(42)
        ticket.save(to_address='other@product.com')
        self.assertRequest('put', '/helpdesk_tickets/42.json')
        self.assertEqual(self.request_data(), {'helpdesk_ticket': {'to_address': 'other@product.com'}})

        with self.assertRaises(exceptions.ReadonlyAttrError):
            ticket.issue = {}

        self.response.status_code = 204
        self.response.content = ''
        self.assertEqual(ticket.delete(), True)
        self.assertRequest('delete', '/helpdesk_tickets/42.json')

    def test_ticket_reply(self):
        self.response.json.return_value = responses['ticket']['get']
        ticket = self.redmine.ticket.get(42)
        self.response.status_code = 201
        self.response.json.return_value = responses['ticket_journal']['create']
        journal = ticket.reply(status_id=2, content='working on it')
        self.assertRequest('post', '/journal_messages.json')
        self.assertEqual(
            self.request_data(), {'journal_message': {'issue_id': 42, 'status_id': 2, 'content': 'working on it'}}
        )
        self.assertEqual(repr(journal), '<redminelib.resources.TicketJournal #321>')

    def test_contact_tickets_relation_is_include(self):
        self.response.json.return_value = responses['contact']['tickets']
        contact = self.redmine.contact.get(1, include=['tickets'])
        self.assertEqual(contact.tickets[0].id, 42)
        self.assertEqual(self.patch_requests.call_count, 1)

    def test_issue_create_with_redmineup_helpdesk_params(self):
        self.response.status_code = 201
        self.response.json.return_value = {'issue': {'id': 1, 'subject': 'Foo'}}
        self.redmine.issue.create(
            project_id=1,
            subject='Foo',
            helpdesk_send_as=2,
            customer_id=3,
            helpdesk_ticket_attributes={'source': 2},
        )
        self.assertEqual(
            self.request_data(),
            {
                'issue': {'subject': 'Foo', 'helpdesk_ticket_attributes': {'source': 2}},
                'helpdesk_send_as': 2,
                'customer_id': 3,
            },
        )

    # AgileSprint / AgileData

    def test_agile_sprint_get(self):
        self.response.json.return_value = responses['agile_sprint']['get']
        sprint = self.redmine.agile_sprint.get(5, project_id='scrum')
        self.assertRequest('get', '/projects/scrum/agile_sprints/5.json')
        self.assertEqual(sprint.story_points, 13)
        self.assertEqual(sprint.url, f'{self.url}/projects/1/agile_sprints/5')
        self.response.json.return_value = responses['agile_sprint']['issues']
        self.assertIsInstance(sprint.issues[0], resources.Issue)
        self.assertRequest('get', '/projects/1/agile_sprints/5.json')
        self.assertEqual(self.request_params()['include'], 'issues')

    def test_agile_sprint_filter(self):
        self.response.json.return_value = responses['agile_sprint']['filter']
        sprints = self.redmine.agile_sprint.filter(project_id='scrum')
        self.assertEqual([s.id for s in sprints], [5, 6])
        self.assertEqual(sprints.total_count, 2)
        self.assertEqual(sprints[0].start_date, datetime.date(2026, 1, 5))
        self.assertRequest('get', '/projects/scrum/agile_sprints.json')
        self.assertEqual(sprints[0].url, f'{self.url}/projects/scrum/agile_sprints/5')

    def test_agile_sprint_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['agile_sprint']['get']
        self.redmine.agile_sprint.create(
            project_id='scrum',
            name='Sprint 5',
            status='active',
            sharing='tree',
            start_date=datetime.date(2026, 1, 5),
            end_date=datetime.date(2026, 1, 16),
        )
        self.assertRequest('post', '/projects/scrum/agile_sprints.json')
        self.assertEqual(
            self.request_data(),
            {
                'agile_sprint': {
                    'name': 'Sprint 5',
                    'status': 1,
                    'sharing': 3,
                    'start_date': '2026-01-05',
                    'end_date': '2026-01-16',
                }
            },
        )

    def test_agile_sprint_update_redirect_is_success(self):
        self.response.json.return_value = responses['agile_sprint']['filter']
        sprint = self.redmine.agile_sprint.filter(project_id='scrum')[0]
        self.response.status_code = 302
        self.assertEqual(sprint.save(status='closed').status, 2)
        self.assertRequest('put', '/projects/scrum/agile_sprints/5.json')
        self.assertEqual(self.request_data(), {'agile_sprint': {'status': 2}})
        self.assertIs(self.patch_requests.call_args[1]['allow_redirects'], False)
        self.assertNotIn('allow_redirects', self.redmine.engine.requests)

    def test_agile_sprint_update_keeps_engine_redirect_option(self):
        self.redmine.engine.requests['allow_redirects'] = True
        self.response.status_code = 302
        self.assertEqual(self.redmine.agile_sprint.update(5, project_id=1, name='x'), True)
        self.assertIs(self.redmine.engine.requests['allow_redirects'], True)

    def test_agile_sprint_update_errors(self):
        self.response.status_code = 500
        self.assertRaises(exceptions.ServerError, lambda: self.redmine.agile_sprint.update(5, project_id=1, name='x'))
        self.response.status_code = 418
        self.assertRaises(exceptions.UnknownError, lambda: self.redmine.agile_sprint.update(5, project_id=1, name='x'))
        self.assertRaises(exceptions.ResourceNoFieldsProvidedError, lambda: self.redmine.agile_sprint.update(5))

    def test_agile_sprint_delete_and_refresh(self):
        self.response.json.return_value = responses['agile_sprint']['filter']
        sprint = self.redmine.agile_sprint.filter(project_id='scrum')[0]
        self.response.json.return_value = responses['agile_sprint']['get']
        sprint.refresh()
        self.assertRequest('get', '/projects/scrum/agile_sprints/5.json')
        self.response.content = ''
        self.assertEqual(sprint.delete(), True)
        self.assertRequest('delete', '/projects/1/agile_sprints/5.json')

    def test_agile_data(self):
        self.response.json.return_value = responses['agile_data']['get']
        data = self.redmine.agile_data.get(42)
        self.assertRequest('get', '/issues/42/agile_data.json')
        self.assertEqual(data.internal_id, 42)
        self.assertEqual(data.story_points, 3)
        self.assertFalse(data.is_new())
        self.assertEqual(repr(data), '<redminelib.resources.AgileData #42>')
        self.response.json.return_value = {'issue': {'id': 42, 'subject': 'Foo'}}
        self.assertIsInstance(data.issue, resources.Issue)
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.agile_data.update(42, story_points=1))

    def test_issue_agile_data_attributes_and_filter(self):
        self.response.status_code = 201
        self.response.json.return_value = {'issue': {'id': 1, 'subject': 'Foo'}}
        self.redmine.issue.create(
            project_id=1, subject='Foo', agile_data_attributes={'story_points': 3, 'agile_sprint_id': 5}
        )
        self.assertEqual(
            self.request_data()['issue']['agile_data_attributes'], {'story_points': 3, 'agile_sprint_id': 5}
        )

    # Checklist

    def test_checklist_get(self):
        self.response.json.return_value = responses['checklist']['get']
        checklist = self.redmine.checklist.get(1)
        self.assertRequest('get', '/checklists/1.json')
        self.assertEqual(checklist.created_at, datetime.datetime(2026, 1, 1, 10, 0))
        self.assertEqual(repr(checklist), '<redminelib.resources.Checklist #1 "FooBar">')

    def test_checklist_filter_and_issue_relation(self):
        self.response.json.return_value = responses['checklist']['filter']
        self.assertEqual(len(self.redmine.checklist.filter(issue_id=42)), 2)
        self.assertRequest('get', '/issues/42/checklists.json')
        issue = self.redmine.issue.to_resource({'id': 42, 'subject': 'Foo'})
        self.assertEqual([c.subject for c in issue.checklists], ['Foo', 'Bar'])
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.checklist.all())

    def test_checklist_create_update_delete(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['checklist']['get']
        checklist = self.redmine.checklist.create(issue_id=42, subject='FooBar', is_done=False)
        self.assertRequest('post', '/issues/42/checklists.json')
        self.assertEqual(self.request_data(), {'checklist': {'subject': 'FooBar', 'is_done': False}})
        self.response.status_code = 204
        self.response.content = ''
        checklist.save(is_done=True, position=2)
        self.assertRequest('put', '/checklists/1.json')
        self.assertEqual(self.request_data(), {'checklist': {'is_done': True, 'position': 2}})
        self.assertEqual(checklist.delete(), True)
        self.assertRequest('delete', '/checklists/1.json')

    def test_checklist_new_is_new(self):
        checklist = self.redmine.checklist.new()
        self.assertTrue(checklist.is_new())

    def test_issue_checklists_sent_as_index_keyed_hash(self):
        self.response.status_code = 201
        self.response.json.return_value = {'issue': {'id': 1, 'subject': 'Foo'}}
        self.redmine.issue.create(
            project_id=1, subject='Foo', checklists=[{'subject': 'A'}, {'subject': 'B', 'is_done': True}]
        )
        self.assertEqual(
            self.request_data()['issue']['checklists_attributes'],
            {'0': {'subject': 'A'}, '1': {'subject': 'B', 'is_done': True}},
        )
        self.response.status_code = 204
        self.response.content = ''
        self.redmine.issue.update(1, checklists={'0': {'id': 5, '_destroy': '1'}})
        self.assertEqual(self.request_data()['issue']['checklists_attributes'], {'0': {'id': 5, '_destroy': '1'}})

    # QuestionsStatus

    def test_questions_status(self):
        self.response.json.return_value = responses['questions_status']['all']
        statuses = self.redmine.questions_status.all()
        self.assertEqual(statuses[0].name, 'Open')
        self.assertEqual(statuses.total_count, 1)
        self.assertRequest('get', '/questions_statuses.json')
