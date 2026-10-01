responses = {
    'contact': {
        'get': {
            'contact': {
                'id': 1,
                'is_company': False,
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'company': 'Ivan Gmbh',
                'birthday': '1980-10-21',
                'author': {'id': 1, 'name': 'Admin'},
                'assigned_to': {'id': 5, 'name': 'John Smith'},
                'address': {'full_address': 'Moscow', 'street': 'foo', 'city': 'Moscow', 'country_code': 'RU'},
                'phones': [{'number': '1234567'}],
                'emails': [{'address': 'ivan@ivanov.com'}],
                'tag_list': ['vip'],
                'custom_fields': [{'id': 1, 'name': 'Foo', 'value': 'bar'}],
                'projects': [{'id': 1, 'name': 'Sales'}],
                'created_on': '2026-01-01T10:00:00Z',
                'updated_on': '2026-01-02T10:00:00Z',
            }
        },
        'filter': {
            'contacts': [
                {'id': 1, 'first_name': 'Ivan', 'last_name': 'Ivanov'},
                {'id': 2, 'first_name': 'ACME', 'is_company': True},
            ],
            'total_count': 2,
            'offset': 0,
            'limit': 25,
        },
        'tickets': {
            'contact': {
                'id': 1,
                'first_name': 'Ivan',
                'helpdesk_tickets': [{'id': 42, 'from_address': 'ivan@ivanov.com'}],
            }
        },
    },
    'contact_tag': {
        'all': {
            'tags': [{'id': 1, 'name': 'vip', 'color': 1}, {'id': 2, 'name': 'online', 'color': 2}],
            'total_count': 2,
        },
    },
    'note': {
        'get': {
            'note': {
                'id': 1,
                'source': {'id': 1, 'name': 'Ivan Ivanov', 'type': 'Contact'},
                'subject': 'Call',
                'content': 'Called him',
                'type_id': 1,
                'author': {'id': 1, 'name': 'Admin'},
                'custom_fields': [],
                'created_on': 'Tue, 10 Jan 2023 11:11:00 +0100',
                'updated_on': 'Tue, 10 Jan 2023 11:12:00 +0100',
            }
        },
    },
    'deal': {
        'get': {
            'deal': {
                'id': 1,
                'name': 'Big deal',
                'price': '1000.0',
                'currency': 'EUR',
                'probability': 80,
                'due_date': '2026-12-12',
                'project': {'id': 1, 'name': 'Sales'},
                'status': {'id': 2, 'name': 'Won'},
                'category': {'id': 3, 'name': 'Integration'},
                'contact': {'id': 1, 'name': 'Ivan Ivanov'},
                'related_contacts': [{'id': 2, 'name': 'ACME'}],
                'custom_fields': [],
                'created_on': '2026-01-01T10:00:00Z',
            }
        },
        'filter': {
            'deals': [{'id': 1, 'name': 'Big deal'}, {'id': 2, 'name': 'Small deal'}],
            'total_count': 2,
            'offset': 0,
            'limit': 25,
        },
    },
    'deal_status': {
        'all': {
            'deal_statuses': [
                {'id': 1, 'name': 'Pending', 'position': 1, 'is_default': True, 'status_type': 0, 'color': 11184810},
                {'id': 2, 'name': 'Won', 'position': 2, 'is_default': False, 'status_type': 1, 'color': 65280},
            ],
            'total_count': 2,
        },
    },
    'deal_category': {
        'filter': {
            'deal_categories': [{'id': 1, 'name': 'Integration'}, {'id': 2, 'name': 'Software'}],
            'total_count': 2,
        },
        'create': {'category': {'id': 3, 'name': 'Consulting'}},
    },
    'crm_query': {
        'filter': {
            'queries': [
                {'id': 1, 'name': 'VIP', 'is_public': True, 'project_id': None},
                {'id': 2, 'name': 'Mine', 'is_public': False, 'project_id': 3},
            ],
            'total_count': 2,
            'offset': 0,
            'limit': 25,
        },
    },
    'ticket': {
        'get': {
            'helpdesk_ticket': {
                'id': 42,
                'from_address': 'client@mail.com',
                'to_address': 'support@product.com',
                'cc_address': None,
                'ticket_date': '2023-01-10',
                'content': 'ticket content',
                'source': 'Phone',
                'is_incoming': True,
                'reaction_time': 60,
                'contact': {'id': 1, 'name': 'Ivan Ivanov'},
            }
        },
        'journals': {
            'helpdesk_ticket': {
                'id': 42,
                'journals': [{'id': 7, 'notes': 'foobar', 'created_on': '2023-01-10T10:00:00Z'}],
                'journal_messages': [{'journal_id': 7, 'is_incoming': False, 'content': 'foobar'}],
            }
        },
        'filter': {'helpdesk_tickets': [{'id': 42}, {'id': 43}], 'total_count': 2, 'offset': 0, 'limit': 25},
    },
    'ticket_journal': {
        'create': {'journal_message': {'id': 321, 'to_address': 'client@mail.com', 'content': 'working on it'}},
    },
    'agile_sprint': {
        'get': {'agile_sprint': {'id': 5, 'project_id': 1, 'name': 'Sprint 5', 'story_points': 13, 'done_ratio': 40.0}},
        'filter': {
            'project_id': 1,
            'project_name': 'Scrum',
            'sprints': [{'id': 5, 'name': 'Sprint 5', 'start_date': '2026-01-05'}, {'id': 6, 'name': 'Sprint 6'}],
        },
        'issues': {
            'agile_sprint': {
                'id': 5,
                'project_id': 1,
                'name': 'Sprint 5',
                'issues': [{'id': 42, 'subject': 'Foo', 'story_points': 3}],
            }
        },
    },
    'agile_data': {
        'get': {
            'agile_data': {
                'id': 9,
                'issue_id': 42,
                'position': 2,
                'story_points': 3,
                'agile_sprint_id': 5,
                'color': None,
            }
        },
    },
    'checklist': {
        'get': {
            'checklist': {
                'id': 1,
                'issue_id': 42,
                'subject': 'FooBar',
                'is_done': False,
                'position': 1,
                'is_section': False,
                'created_at': '2026-01-01T10:00:00Z',
                'updated_at': '2026-01-01T10:00:00Z',
            }
        },
        'filter': {
            'checklists': [{'id': 1, 'issue_id': 42, 'subject': 'Foo'}, {'id': 2, 'issue_id': 42, 'subject': 'Bar'}],
            'total_count': 2,
        },
    },
    'questions_status': {
        'all': {'questions_statuses': [{'id': 1, 'name': 'Open', 'color': '#00ff00', 'is_closed': False}]},
    },
}
