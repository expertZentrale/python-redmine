"""
Defines Redmine resources.
"""

from .base import BaseResource, registry
from .expert import (
    ExpertAgileData,
    ExpertAgileSprint,
    HelpdeskContact,
    HelpdeskMailbox,
    HelpdeskProjectSetting,
    HelpdeskTicket,
)
from .redmineup import (
    AgileData,
    AgileSprint,
    Checklist,
    Contact,
    ContactTag,
    CrmQuery,
    Deal,
    DealCategory,
    DealStatus,
    Note,
    QuestionsStatus,
    Ticket,
    TicketJournal,
)
from .standard import (
    Attachment,
    CustomField,
    Enumeration,
    File,
    Group,
    Issue,
    IssueCategory,
    IssueJournal,
    IssueRelation,
    IssueStatus,
    News,
    Project,
    ProjectMembership,
    Query,
    Role,
    TimeEntry,
    Tracker,
    User,
    Version,
    WikiPage,
)
