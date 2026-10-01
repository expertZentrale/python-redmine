"""
Defines resources of the RedmineUP plugins: CRM (redmine_contacts), Helpdesk (redmine_contacts_helpdesk),
Agile (redmine_agile), Checklists (redmine_checklists) and Questions (redmine_questions).

Resource names and their API follow the former Python-Redmine Pro Edition where it had them.
"""

import email.utils
import os

from .. import exceptions, managers
from . import BaseResource

CRM_REQUIREMENTS = [('redmine_contacts', (3, 3, 0))]
HELPDESK_REQUIREMENTS = [('redmine_contacts_helpdesk', (4, 1, 12))]
AGILE_REQUIREMENTS = [('redmine_agile', (1, 6, 0))]
CHECKLISTS_REQUIREMENTS = [('redmine_checklists', (3, 0, 0))]
QUESTIONS_REQUIREMENTS = [('redmine_questions', (1, 0, 0))]


class Contact(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = CRM_REQUIREMENTS
    container_all = 'contacts'
    container_one = 'contact'
    container_filter = 'contacts'
    container_create = 'contact'
    container_update = 'contact'
    query_all_export = '/contacts.{format}'
    query_one_export = '/contacts/{}.{format}'
    query_all = '/contacts.json'
    query_one = '/contacts/{}.json'
    query_filter = '/contacts.json'
    query_create = '/projects/{project_id}/contacts.json'
    query_update = '/contacts/{}.json'
    query_delete = '/contacts/{}.json'
    search_hints = ['contact']
    manager_class = managers.ContactManager

    _repr = [['id', 'first_name', 'last_name'], ['id', 'first_name'], ['id', 'company']]
    _includes = ['notes', 'contacts', 'deals', 'issues', 'tickets']
    _includes_map = {'tickets': 'helpdesk_tickets'}
    _unconvertible = BaseResource._unconvertible + [
        'first_name',
        'last_name',
        'middle_name',
        'company',
        'website',
        'skype_name',
        'job_title',
        'background',
    ]
    _resource_map = {'author': 'User', 'assigned_to': 'User'}
    _resource_set_map = {
        'custom_fields': 'CustomField',
        'projects': 'Project',
        'notes': 'Note',
        'contacts': 'Contact',
        'deals': 'Deal',
        'issues': 'Issue',
        'tickets': 'Ticket',
    }
    _attach_relations = {'Project': 'contacts', 'User': 'contacts'}

    class Project:
        """
        Contact's projects implementation.
        """

        def __init__(self, contact):
            self._redmine = contact.manager.redmine
            self._contact_id = contact.internal_id

        def add(self, project_id):
            """
            Adds contact to the project.

            :param project_id: (required). Project id or identifier.
            :type project_id: int or string
            """
            url = f'{self._redmine.url}/contacts/{self._contact_id}/projects.json'
            return self._redmine.engine.request('post', url, data={'project': {'id': project_id}})

        def remove(self, project_id):
            """
            Removes contact from the project, a contact has to stay in at least one project.

            :param project_id: (required). Project id or identifier.
            :type project_id: int or string
            """
            url = f'{self._redmine.url}/contacts/{self._contact_id}/projects/{project_id}.json'
            return self._redmine.engine.request('delete', url, params={'project[id]': project_id})

    @classmethod
    def decode(cls, attr, value, manager):
        # The plugin only takes phones and emails as comma separated strings
        if attr in ('phones', 'emails') and isinstance(value, (list, tuple)):
            return attr[:-1], ', '.join(str(v) for v in value)
        elif attr == 'tags' and isinstance(value, (list, tuple)):
            return attr, ','.join(value)
        elif attr == 'avatar' and isinstance(value, dict) and 'token' not in value:
            path = value.get('path', '')
            filename = value.get('filename') or (os.path.basename(path) if isinstance(path, str) else 'avatar')
            token = manager.redmine.upload(path, filename=filename)['token']
            avatar = {'token': token, 'filename': filename, 'description': 'avatar'}

            if value.get('content_type'):
                avatar['content_type'] = value['content_type']

            return attr, avatar

        return super().decode(attr, value, manager)

    def __getattr__(self, attr):
        if attr == 'project':
            return Contact.Project(self)

        return super().__getattr__(attr)


class ContactTag(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = [('redmine_contacts', (3, 4, 0))]
    container_all = 'tags'
    query_all = '/contacts_tags.json'

    _resource_set_map = {'contacts': 'Contact'}

    def __getattr__(self, attr):
        if attr == 'contacts':
            return self.manager.new_manager('Contact').filter(tags=self.name)

        return super().__getattr__(attr)


class Note(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = CRM_REQUIREMENTS
    container_one = 'note'
    container_create = 'note'
    container_update = 'note'
    query_one = '/notes/{}.json'
    query_create = '/notes.json'
    query_update = '/notes/{}.json'
    query_delete = '/notes/{}.json'
    manager_class = managers.NoteManager

    _repr = [['id', 'subject'], ['id']]
    _unconvertible = BaseResource._unconvertible + ['subject', 'content']
    _resource_map = {'author': 'User'}
    _resource_set_map = {'custom_fields': 'CustomField', 'attachments': 'Attachment'}

    @classmethod
    def encode(cls, attr, value, manager):
        # Note show renders RFC 822 dates instead of the ISO ones used everywhere else
        if attr in ('created_on', 'updated_on') and isinstance(value, str) and ',' in value:
            try:
                value = email.utils.parsedate_to_datetime(value)
            except (TypeError, ValueError):
                return attr, value

            if manager.redmine.timezone is not None:
                value = value.astimezone(manager.redmine.timezone)

            return attr, value
        elif attr == 'source' and isinstance(value, dict) and value.get('type'):
            try:
                return attr, manager.new_manager(value['type']).to_resource(value)
            except exceptions.ResourceError:
                return attr, value

        return super().encode(attr, value, manager)


class Deal(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = CRM_REQUIREMENTS
    container_all = 'deals'
    container_one = 'deal'
    container_filter = 'deals'
    container_create = 'deal'
    container_update = 'deal'
    query_all_export = '/deals.{format}'
    # The plugin shows open deals only by default
    query_all = '/deals.json?status_id=*'
    query_one = '/deals/{}.json'
    query_filter = '/deals.json'
    query_create = '/projects/{project_id}/deals.json'
    query_update = '/deals/{}.json'
    query_delete = '/deals/{}.json'

    _repr = [['id', 'name']]
    _includes = ['notes', 'lines']
    _unconvertible = BaseResource._unconvertible + ['background', 'currency']
    _resource_map = {
        'project': 'Project',
        'status': 'DealStatus',
        'category': 'DealCategory',
        'author': 'User',
        'assigned_to': 'User',
        'contact': 'Contact',
    }
    _resource_set_map = {'custom_fields': 'CustomField', 'related_contacts': 'Contact', 'notes': 'Note'}
    _single_attr_id_map = {
        'status_id': 'status',
        'category_id': 'category',
        'assigned_to_id': 'assigned_to',
        'contact_id': 'contact',
    }
    _attach_relations = {'Project': 'deals', 'User': 'deals'}

    @classmethod
    def decode(cls, attr, value, manager):
        # Deal create parses the price as a string, a JSON number makes it fail
        if attr == 'price' and isinstance(value, (int, float)) and not isinstance(value, bool):
            return attr, str(value)

        return super().decode(attr, value, manager)


class DealStatus(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = CRM_REQUIREMENTS
    container_all = 'deal_statuses'
    query_all = '/deal_statuses.json'

    statuses = {0: 'open', 1: 'won', 2: 'lost'}

    _relations = ['deals']
    _relations_name = 'status'
    _resource_set_map = {'deals': 'Deal'}


class DealCategory(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = CRM_REQUIREMENTS
    container_filter = 'deal_categories'
    container_create = 'category'
    container_update = 'category'
    query_filter = '/projects/{project_id}/deal_categories.json'
    query_create = '/projects/{project_id}/deal_categories.json'
    query_update = '/deal_categories/{}.json'
    query_delete = '/deal_categories/{}.json'

    _relations = ['deals']
    _relations_name = 'category'
    _resource_set_map = {'deals': 'Deal'}
    _attach_relations = {'Project': 'deal_categories'}

    def __getattr__(self, attr):
        if attr == 'deals':
            return self.manager.new_manager('Deal').filter(category_id=self.internal_id, status_id='*')

        return super().__getattr__(attr)


class CrmQuery(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = CRM_REQUIREMENTS
    container_filter = 'queries'
    query_filter = '/crm_queries.json?object_type={resource}'

    def __getattr__(self, attr):
        if attr in ('contacts', 'deals'):
            filters = {'query_id': self.internal_id}

            if self._decoded_attrs.get('project_id'):
                filters['project_id'] = self._decoded_attrs['project_id']

            return self.manager.new_manager(attr[:-1].capitalize()).filter(**filters)

        return super().__getattr__(attr)


class Ticket(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = HELPDESK_REQUIREMENTS
    container_all = 'helpdesk_tickets'
    container_one = 'helpdesk_ticket'
    container_filter = 'helpdesk_tickets'
    container_create = 'helpdesk_ticket'
    container_update = 'helpdesk_ticket'
    query_all = '/helpdesk_tickets.json'
    query_one = '/helpdesk_tickets/{}.json'
    query_filter = '/helpdesk_tickets.json'
    query_create = '/helpdesk_tickets.json'
    query_update = '/helpdesk_tickets/{}.json'
    query_delete = '/helpdesk_tickets/{}.json'
    query_url = '/issues/{}'
    manager_class = managers.TicketManager

    # Requests take a source code or name, responses contain a localized label
    sources = {'email': 0, 'web': 1, 'phone': 2, 'twitter': 3, 'conversation': 4}

    _repr = [['id', 'from_address'], ['id']]
    _includes = ['journals', 'journal_messages']
    _unconvertible = BaseResource._unconvertible + ['content', 'from_address', 'to_address', 'cc_address']
    # issue and contact are set as nested dicts on ticket creation
    _create_readonly = ['id', 'created_on', 'updated_on'] + [
        'reaction_time',
        'first_response_time',
        'resolve_time',
        'last_agent_response_at',
        'last_customer_response_at',
        'message_file',
    ]
    _update_readonly = _create_readonly + ['issue']
    _resource_map = {'contact': 'Contact', 'message_file': 'Attachment'}
    _resource_set_map = {'journals': 'TicketJournal'}

    @classmethod
    def decode(cls, attr, value, manager):
        if attr == 'source' and isinstance(value, str) and value.lower() in cls.sources:
            return attr, cls.sources[value.lower()]
        elif attr == 'cc_address' and isinstance(value, (list, tuple)):
            return attr, ','.join(value)

        return super().decode(attr, value, manager)

    def reply(self, **fields):
        """
        Replies to the customer, i.e. adds a journal and sends it as an email.

        :param dict fields: (required). Fields for the reply, see TicketJournal create.
        """
        return self.manager.new_manager('TicketJournal').create(issue_id=self.internal_id, **fields)

    def __getattr__(self, attr):
        if attr == 'issue' and not self.is_new():
            return self.manager.new_manager('Issue').get(self.internal_id)

        return super().__getattr__(attr)


class TicketJournal(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = HELPDESK_REQUIREMENTS
    container_create = 'journal_message'
    container_update = 'journal'
    query_create = '/journal_messages.json'
    query_update = '/journals/{}.json'

    _repr = [['id']]
    _unconvertible = ['notes', 'content']
    _create_readonly = ['id', 'created_on', 'message_date', 'message_id']
    _update_readonly = _create_readonly[:]


class AgileSprint(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = AGILE_REQUIREMENTS
    container_one = 'agile_sprint'
    container_filter = 'sprints'
    container_create = 'agile_sprint'
    container_update = 'agile_sprint'
    query_one = '/projects/{project_id}/agile_sprints/{}.json'
    query_filter = '/projects/{project_id}/agile_sprints.json'
    query_create = '/projects/{project_id}/agile_sprints.json'
    query_update = '/projects/{project_id}/agile_sprints/{}.json'
    query_delete = '/projects/{project_id}/agile_sprints/{}.json'
    manager_class = managers.AgileSprintManager

    # Status and sharing have to be written as integers
    statuses = {'open': 0, 'active': 1, 'closed': 2}
    sharings = {'none': 0, 'descendants': 1, 'hierarchy': 2, 'tree': 3, 'system': 4}

    _repr = [['id', 'name']]
    _includes = ['issues']
    _create_readonly = BaseResource._create_readonly + ['story_points', 'done_ratio', 'estimated_hours', 'spent_hours']
    _update_readonly = _create_readonly + ['project_id']
    _resource_set_map = {'issues': 'Issue'}

    @classmethod
    def decode(cls, attr, value, manager):
        if attr == 'status' and isinstance(value, str):
            return attr, cls.statuses.get(value, value)
        elif attr == 'sharing' and isinstance(value, str):
            return attr, cls.sharings.get(value, value)

        return super().decode(attr, value, manager)

    @property
    def sprint_project_id(self):
        # Sprint list items don't contain the project, it is part of the list request instead
        return self._decoded_attrs.get('project_id') or self.manager.params.get('project_id')

    @property
    def url(self):
        return (
            self.manager.redmine.url + self.query_one.format(self.internal_id, project_id=self.sprint_project_id)[:-5]
        )

    def refresh(self, itself=True, **params):
        params.setdefault('project_id', self.sprint_project_id)
        return super().refresh(itself, **params)

    def pre_update(self):
        self._changes.setdefault('project_id', self.sprint_project_id)

    def delete(self, **params):
        params.setdefault('project_id', self.sprint_project_id)
        return super().delete(**params)


class AgileData(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = AGILE_REQUIREMENTS
    internal_id_key = 'issue_id'
    container_one = 'agile_data'
    query_one = '/issues/{}/agile_data.json'
    query_url = '/issues/{}'

    _repr = [['issue_id']]
    _resource_map = {'agile_sprint': 'AgileSprint'}

    def is_new(self):
        return 'issue_id' not in self._decoded_attrs

    def __getattr__(self, attr):
        if attr == 'issue':
            return self.manager.new_manager('Issue').get(self.internal_id)

        return super().__getattr__(attr)


class Checklist(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = CHECKLISTS_REQUIREMENTS
    container_one = 'checklist'
    container_filter = 'checklists'
    container_create = 'checklist'
    container_update = 'checklist'
    query_one = '/checklists/{}.json'
    query_filter = '/issues/{issue_id}/checklists.json'
    query_create = '/issues/{issue_id}/checklists.json'
    query_update = '/checklists/{}.json'
    query_delete = '/checklists/{}.json'

    _repr = [['id', 'subject'], ['id']]
    _unconvertible = BaseResource._unconvertible + ['subject']
    _create_readonly = ['id', 'created_at', 'updated_at']
    _update_readonly = _create_readonly[:]
    _attach_relations = {'Issue': 'checklists'}


class QuestionsStatus(BaseResource):
    redmine_version = (4, 0, 0)
    requirements = QUESTIONS_REQUIREMENTS
    container_all = 'questions_statuses'
    query_all = '/questions_statuses.json'
