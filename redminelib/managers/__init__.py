"""
Defines manager classes.
"""

from .base import ResourceManager
from .expert import HelpdeskMailboxManager, HelpdeskProjectSettingManager, HelpdeskTicketManager
from .redmineup import AgileSprintManager, ContactManager, NoteManager, TicketManager
from .standard import FileManager, IssueManager, NewsManager, ProjectManager, UserManager, WikiPageManager
