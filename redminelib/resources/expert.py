"""
Defines resources of the redmine_expert_helpdesk and redmine_expert_agile plugins.
"""

from .. import managers
from . import BaseResource

HELPDESK_REQUIREMENTS = [('redmine_expert_helpdesk', (0, 20, 0))]
AGILE_REQUIREMENTS = [('redmine_expert_agile', (0, 6, 0))]


class HelpdeskContact(BaseResource):
    redmine_version = (5, 0, 0)
    requirements = HELPDESK_REQUIREMENTS
    container_one = 'helpdesk_contact'
    container_filter = 'helpdesk_contacts'
    container_create = 'helpdesk_contact'
    container_update = 'helpdesk_contact'
    query_one = '/helpdesk/contacts/{}.json'
    query_filter = '/projects/{project_id}/helpdesk/contacts.json'
    query_create = '/projects/{project_id}/helpdesk/contacts.json'
    query_update = '/helpdesk/contacts/{}.json'
    query_delete = '/helpdesk/contacts/{}.json'

    _repr = [['id', 'name'], ['id', 'email']]
    _unconvertible = BaseResource._unconvertible + ['email', 'company', 'phone', 'notes']
    _update_readonly = BaseResource._update_readonly + ['email']
    _resource_map = {'project': 'Project'}


class HelpdeskTicket(BaseResource):
    redmine_version = (5, 0, 0)
    requirements = HELPDESK_REQUIREMENTS
    container_one = 'helpdesk_ticket'
    container_filter = 'helpdesk_tickets'
    container_create = 'helpdesk_ticket'
    container_update = 'helpdesk_ticket'
    query_one = '/helpdesk/tickets/{}.json'
    query_filter = '/projects/{project_id}/helpdesk/tickets.json'
    query_create = '/projects/{project_id}/helpdesk/tickets.json'
    query_update = '/helpdesk/tickets/{}.json'
    query_delete = '/helpdesk/tickets/{}.json'
    query_url = '/issues/{}'
    manager_class = managers.HelpdeskTicketManager

    _repr = [['id', 'subject'], ['id']]
    _includes = ['messages']
    _unconvertible = BaseResource._unconvertible + ['subject', 'notes']
    _create_readonly = BaseResource._create_readonly + ['contact', 'mailbox', 'sla', 'closed_on']
    _update_readonly = _create_readonly[:]
    _resource_map = {
        'project': 'Project',
        'tracker': 'Tracker',
        'status': 'IssueStatus',
        'priority': 'Enumeration',
        'author': 'User',
        'assigned_to': 'User',
        'contact': 'HelpdeskContact',
        'mailbox': 'HelpdeskMailbox',
    }
    _single_attr_id_map = {
        'tracker_id': 'tracker',
        'status_id': 'status',
        'priority_id': 'priority',
        'assigned_to_id': 'assigned_to',
        'contact_id': 'contact',
    }

    def __getattr__(self, attr):
        if attr == 'issue':
            return self.manager.new_manager('Issue').get(self.internal_id)

        return super().__getattr__(attr)


class HelpdeskMailbox(BaseResource):
    redmine_version = (5, 0, 0)
    requirements = HELPDESK_REQUIREMENTS
    container_one = 'helpdesk_mailbox'
    container_filter = 'helpdesk_mailboxes'
    container_create = 'helpdesk_mailbox'
    container_update = 'helpdesk_mailbox'
    query_one = '/helpdesk/mailboxes/{}.json'
    query_filter = '/projects/{project_id}/helpdesk/mailboxes.json'
    query_create = '/projects/{project_id}/helpdesk/mailboxes.json'
    query_update = '/helpdesk/mailboxes/{}.json'
    query_delete = '/helpdesk/mailboxes/{}.json'
    manager_class = managers.HelpdeskMailboxManager

    _repr = [['id', 'mailbox_address'], ['id', 'address']]
    _unconvertible = BaseResource._unconvertible + [
        'mailbox_address',
        'address',
        'allow_list',
        'deny_list',
        'autoresponder_subject',
        'autoresponder_body',
        'reply_header',
        'reply_footer',
        'last_error',
    ]
    _create_readonly = BaseResource._create_readonly + [
        'outgoing_route',
        'microsoft_hosted',
        'available_reply_transports',
        'oauth_connected',
        'oauth_connected_at',
        'oauth_token_expires_at',
        'mail_password_set',
        'oauth_client_secret_set',
        'oauth_sa_key_set',
        'oauth_refresh_token_set',
        'last_fetched_at',
        'last_error',
        'last_error_at',
    ]
    _update_readonly = _create_readonly[:]
    _resource_map = {'project': 'Project'}

    def __getattr__(self, attr):
        if attr == 'test_connection':
            return lambda: self.manager.test_connection(self.internal_id)

        return super().__getattr__(attr)


class HelpdeskProjectSetting(BaseResource):
    redmine_version = (5, 0, 0)
    requirements = HELPDESK_REQUIREMENTS
    internal_id_key = 'project_id'
    container_one = 'helpdesk_project_setting'
    container_update = 'helpdesk_project_setting'
    query_one = '/projects/{}/helpdesk/settings.json'
    query_update = '/projects/{}/helpdesk/settings.json'
    manager_class = managers.HelpdeskProjectSettingManager

    _repr = [['project_id']]
    _unconvertible = BaseResource._unconvertible + [
        'reply_subject_template',
        'sla_work_days',
        'sla_work_start',
        'sla_work_end',
        'ai_prompt',
        'ai_answer_prompt',
        'info_request_keywords',
        'info_request_sender_blacklist',
        'info_request_ai_prompt',
        'info_request_subject',
        'info_request_body',
    ]
    _resource_map = {'project': 'Project'}

    @property
    def project_id(self):
        return (self._decoded_attrs.get('project') or {}).get('id')

    def is_new(self):
        return 'project' not in self._decoded_attrs


class ExpertAgileSprint(BaseResource):
    redmine_version = (5, 0, 0)
    requirements = AGILE_REQUIREMENTS
    container_one = 'expert_agile_sprint'
    container_filter = 'expert_agile_sprints'
    container_create = 'expert_agile_sprint'
    container_update = 'expert_agile_sprint'
    query_one = '/projects/{project_id}/expert_agile_sprints/{}.json'
    query_filter = '/projects/{project_id}/expert_agile_sprints.json'
    query_create = '/projects/{project_id}/expert_agile_sprints.json'
    query_update = '/projects/{project_id}/expert_agile_sprints/{}.json'
    query_delete = '/projects/{project_id}/expert_agile_sprints/{}.json'

    # Status and sharing are returned as names but have to be written as integers
    statuses = {'open': 0, 'active': 1, 'closed': 2}
    sharings = {'none': 0, 'descendants': 1, 'hierarchy': 2, 'tree': 3, 'system': 4}

    _repr = [['id', 'name']]
    _create_readonly = BaseResource._create_readonly + ['issue_count', 'story_points']
    _update_readonly = _create_readonly + ['project_id']

    @classmethod
    def decode(cls, attr, value, manager):
        if attr == 'status' and isinstance(value, str):
            return attr, cls.statuses.get(value, value)
        elif attr == 'sharing' and isinstance(value, str):
            return attr, cls.sharings.get(value, value)

        return super().decode(attr, value, manager)

    @classmethod
    def encode(cls, attr, value, manager):
        if attr == 'status' and isinstance(value, int):
            return attr, {v: k for k, v in cls.statuses.items()}.get(value, value)
        elif attr == 'sharing' and isinstance(value, int):
            return attr, {v: k for k, v in cls.sharings.items()}.get(value, value)

        return super().encode(attr, value, manager)

    @property
    def url(self):
        return self.manager.redmine.url + self.query_one.format(self.internal_id, project_id=self.project_id)[:-5]

    def refresh(self, itself=True, **params):
        params.setdefault('project_id', self.project_id)
        return super().refresh(itself, **params)

    def pre_update(self):
        # Sprints can only be addressed through their project, project_id is consumed by the URL
        self._changes.setdefault('project_id', self.project_id)

    def delete(self, **params):
        params.setdefault('project_id', self.project_id)
        return super().delete(**params)

    def activate(self):
        """
        Makes this sprint the active one, the previously active sprint of the project is reopened by Redmine.
        """
        return self.save(status='active')

    def close(self):
        """
        Closes the sprint, Redmine refuses this while the sprint still contains open issues.
        """
        return self.save(status='closed')


class ExpertAgileData(BaseResource):
    redmine_version = (5, 0, 0)
    requirements = AGILE_REQUIREMENTS
    internal_id_key = 'issue_id'
    container_one = 'expert_agile_data'
    container_update = 'expert_agile_data'
    query_one = '/issues/{}/expert_agile_data.json'
    query_update = '/issues/{}/expert_agile_data.json'
    query_url = '/issues/{}'

    _repr = [['issue_id']]
    _unconvertible = BaseResource._unconvertible + ['position']
    _create_readonly = BaseResource._create_readonly + ['issue_id', 'position']
    _update_readonly = _create_readonly[:]

    def is_new(self):
        return 'issue_id' not in self._decoded_attrs

    def __getattr__(self, attr):
        if attr == 'issue':
            return self.manager.new_manager('Issue').get(self.internal_id)

        return super().__getattr__(attr)
