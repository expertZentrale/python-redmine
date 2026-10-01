"""
Tests for REST API additions of Redmine 6.0 - 7.0.
"""

import json

from redminelib import Redmine, exceptions, resources

from . import BaseRedmineTestCase


class RedmineAPIAdditionsTestCase(BaseRedmineTestCase):
    def test_oauth_token_is_sent_as_bearer(self):
        redmine = Redmine(self.url, oauth_token='abc')
        self.response.json.return_value = {'user': {'id': 1}}
        redmine.user.get('current')
        self.assertEqual(self.patch_requests.call_args[1]['headers'], {'Authorization': 'Bearer abc'})

    def test_oauth_token_in_session(self):
        self.response.json.return_value = {'user': {'id': 1}}

        with self.redmine.session(oauth_token='xyz'):
            self.redmine.user.get('current')

        self.assertEqual(self.patch_requests.call_args[1]['headers'], {'Authorization': 'Bearer xyz'})
        self.redmine.user.get('current')
        self.assertEqual(self.patch_requests.call_args[1]['headers'], {})

    def test_api_key_wins_over_oauth_token(self):
        redmine = Redmine(self.url, key='123', oauth_token='abc')
        self.assertEqual(redmine.engine.requests['headers'], {'X-Redmine-API-Key': '123'})

    def test_issue_journal_updated_by(self):
        self.response.json.return_value = {
            'issue': {
                'id': 1,
                'journals': [
                    {
                        'id': 1,
                        'user': {'id': 1},
                        'updated_on': '2026-01-01T10:00:00Z',
                        'updated_by': {'id': 2, 'name': 'Jane'},
                    }
                ],
            }
        }
        journal = self.redmine.issue.get(1, include=['journals']).journals[0]
        self.assertIsInstance(journal.updated_by, resources.User)
        self.assertEqual(journal.updated_by.id, 2)

    def test_custom_field_projects(self):
        self.response.json.return_value = {
            'custom_fields': [{'id': 1, 'name': 'Foo', 'is_for_all': False, 'projects': [{'id': 3, 'name': 'Bar'}]}]
        }
        field = self.redmine.custom_field.get(1)
        self.assertFalse(field.is_for_all)
        self.assertIsInstance(field.projects[0], resources.Project)

    def test_wiki_page_project(self):
        self.response.json.return_value = {
            'wiki_page': {'title': 'Foo', 'version': 1, 'project': {'id': 3, 'name': 'Bar'}}
        }
        page = self.redmine.wiki_page.get('Foo', project_id='bar')
        self.assertIsInstance(page.project, resources.Project)
        self.assertEqual(page.project_id, 'bar')
        page = self.redmine.wiki_page.to_resource({'title': 'Foo', 'project': {'id': 3, 'name': 'Bar'}})
        self.assertEqual(page.project_id, 3)
        self.assertEqual(page.url, f'{self.url}/projects/3/wiki/Foo')

    def test_group_add_users_bulk(self):
        self.response.json.return_value = {'group': {'id': 1, 'name': 'Foo'}}
        group = self.redmine.group.get(1)
        self.response.content = ''
        self.assertEqual(group.user.add([1, 2]), True)
        self.assertEqual(self.patch_requests.call_args[0][1], f'{self.url}/groups/1/users.json')
        self.assertEqual(json.loads(self.patch_requests.call_args[1]['data']), {'user_ids': [1, 2]})

    def test_group_remove_users_bulk(self):
        self.response.json.return_value = {'group': {'id': 1, 'name': 'Foo'}}
        group = self.redmine.group.get(1)
        self.response.content = ''
        self.assertEqual(group.user.remove([1, 2]), True)
        args, kwargs = self.patch_requests.call_args
        self.assertEqual((args[0], args[1]), ('delete', f'{self.url}/groups/1/users.json'))
        self.assertEqual(kwargs['params'], {'user_ids[]': [1, 2]})
        self.redmine.ver = (6, 1, 0)
        self.assertRaises(
            exceptions.VersionMismatchError, lambda: self.redmine.group.to_resource({'id': 1}).user.remove([1])
        )
        self.redmine.ver = (7, 0, 0)
        self.assertEqual(self.redmine.group.to_resource({'id': 1}).user.remove((3,)), True)

    def test_user_auth_source_include(self):
        self.response.json.return_value = {'user': {'id': 1, 'login': 'foo', 'auth_source': {'id': 2, 'name': 'LDAP'}}}
        user = self.redmine.user.get(1, include=['auth_source'])
        self.assertEqual(self.patch_requests.call_args[1]['params'], {'include': 'auth_source'})
        self.assertEqual(user.auth_source, {'id': 2, 'name': 'LDAP'})
