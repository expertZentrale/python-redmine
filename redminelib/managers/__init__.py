"""
Defines manager classes.
"""

from .base import ResourceManager
from .expert import HelpdeskMailboxManager, HelpdeskProjectSettingManager, HelpdeskTicketManager
from .standard import FileManager, IssueManager, NewsManager, ProjectManager, UserManager, WikiPageManager
