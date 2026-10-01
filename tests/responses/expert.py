responses = {
    'helpdesk_contact': {
        'get': {
            'helpdesk_contact': {
                'id': 1,
                'email': 'jane@example.com',
                'name': 'Jane Doe',
                'company': 'ACME',
                'phone': '+49 123',
                'notes': None,
                'info_request_opt_out': False,
                'project': {'id': 1},
                'created_on': '2026-01-01T10:00:00Z',
                'updated_on': '2026-01-02T10:00:00Z',
            }
        },
        'filter': {
            'helpdesk_contacts': [
                {'id': 1, 'email': 'jane@example.com', 'name': 'Jane Doe', 'project': {'id': 1}},
                {'id': 2, 'email': 'john@example.com', 'name': None, 'project': {'id': 1}},
            ],
            'total_count': 2,
            'offset': 0,
            'limit': 25,
        },
    },
    'helpdesk_ticket': {
        'get': {
            'helpdesk_ticket': {
                'id': 42,
                'project': {'id': 1, 'name': 'Support'},
                'tracker': {'id': 3, 'name': 'Ticket'},
                'status': {'id': 1, 'name': 'New'},
                'priority': {'id': 2, 'name': 'Normal'},
                'subject': 'Printer on fire',
                'description': 'Please help',
                'author': {'id': 5, 'name': 'Agent'},
                'done_ratio': 0,
                'created_on': '2026-01-01T10:00:00Z',
                'updated_on': '2026-01-01T11:00:00Z',
                'closed_on': None,
                'contact': {'id': 1, 'email': 'jane@example.com', 'name': 'Jane Doe', 'company': 'ACME', 'phone': ''},
                'mailbox': {'id': 7, 'address': 'support@example.com', 'provider': 'graph'},
                'sla': {
                    'reaction': {'status': 'running', 'minutes': 60, 'target': 120, 'due_at': '2026-01-01T12:00:00Z'},
                    'solution': {'status': 'met', 'minutes': 10, 'target': 480},
                },
                'messages': [],
            }
        },
        'get_messages': {
            'helpdesk_ticket': {
                'id': 42,
                'subject': 'Printer on fire',
                'messages': [
                    {
                        'id': 9,
                        'direction': 'in',
                        'subject': 'Printer on fire',
                        'sent_at': '2026-01-01T10:00:00Z',
                        'recipient_to': 'support@example.com',
                        'recipient_cc': None,
                        'recipient_bcc': None,
                        'contact': {'id': 1},
                        'mailbox': {'id': 7},
                        'created_on': '2026-01-01T10:00:00Z',
                    }
                ],
            }
        },
        'filter': {
            'helpdesk_tickets': [
                {'id': 42, 'subject': 'Printer on fire', 'project': {'id': 1, 'name': 'Support'}},
                {'id': 41, 'subject': 'Login broken', 'project': {'id': 1, 'name': 'Support'}},
            ],
            'total_count': 2,
            'offset': 0,
            'limit': 25,
        },
    },
    'helpdesk_mailbox': {
        'get': {
            'helpdesk_mailbox': {
                'id': 7,
                'project': {'id': 1, 'name': 'Support'},
                'mailbox_address': 'support@example.com',
                'enabled': True,
                'provider': 'imap',
                'available_reply_transports': ['provider', 'smtp'],
                'mail_password_set': True,
                'created_on': '2026-01-01T10:00:00Z',
                'updated_on': '2026-01-01T10:00:00Z',
            }
        },
        'filter': {
            'helpdesk_mailboxes': [
                {'id': 7, 'mailbox_address': 'support@example.com', 'enabled': True},
                {'id': 8, 'mailbox_address': 'sales@example.com', 'enabled': False},
            ],
            'total_count': 2,
            'offset': 0,
            'limit': 25,
        },
        'test_connection_ok': {'connection_test': {'ok': True, 'message': 'OK', 'folders': ['INBOX', 'Sent']}},
        'test_connection_failed': {'connection_test': {'ok': False, 'message': 'Authentication failed'}},
    },
    'helpdesk_project_setting': {
        'get': {
            'helpdesk_project_setting': {
                'project': {'id': 1},
                'send_reply_by_default': True,
                'sla_enabled': True,
                'sla_work_days': '1,2,3,4,5',
                'sla_work_start': '08:00',
                'sla_work_end': '17:00',
                'sla_priorities': [
                    {'priority_id': 2, 'priority_name': 'Normal', 'reaction_minutes': 60, 'solution_minutes': 480}
                ],
            }
        },
    },
    'expert_agile_sprint': {
        'get': {
            'expert_agile_sprint': {
                'id': 3,
                'project_id': 1,
                'name': 'Sprint 3',
                'description': None,
                'status': 'active',
                'sharing': 'none',
                'start_date': '2026-01-05',
                'end_date': '2026-01-16',
                'issue_count': 4,
                'story_points': 13,
            }
        },
        'filter': {
            'expert_agile_sprints': [
                {'id': 3, 'project_id': 1, 'name': 'Sprint 3', 'status': 'active', 'sharing': 'none'},
                {'id': 2, 'project_id': 1, 'name': 'Sprint 2', 'status': 'closed', 'sharing': 'tree'},
            ],
            'total_count': 2,
        },
    },
    'expert_agile_data': {
        'get': {'expert_agile_data': {'issue_id': 42, 'position': '1024.0', 'story_points': 5, 'sprint_id': 3}},
        'empty': {'expert_agile_data': {'issue_id': 43, 'position': None, 'story_points': None, 'sprint_id': None}},
    },
}
