import logging
import re
from collections import defaultdict
from typing import List
from typing import NamedTuple

log = logging.getLogger(__name__)


ACLGroup = NamedTuple('ACLGroup', [
    ('name', str),
    ('members', List[str]),
])

ACLRule = NamedTuple('ACLRule', [
    ('group_name', str),
    ('action_patterns', List[re._pattern_type]),
    ('allow', bool),
])


class ACLEngine:
    def __init__(self, acl_config) -> None:
        # Mapping of group name to group
        self.groups_by_name = {}

        # Mapping of member name to set of group names
        self.group_names_by_member = defaultdict(set)

        log.info("Parsing ACL groups")
        for group_dict in acl_config['groups']:
            name = group_dict['name']
            members = group_dict['members']

            group = ACLGroup(name=name, members=members)
            self.groups_by_name[name] = group

            for member in members:
                self.group_names_by_member[member].add(name)

        log.info("Parsing ACL rules")
        self.rules = []
        for rule_dict in acl_config['rules']:
            group_name = rule_dict['group']
            allow = rule_dict['allow']
            action_patterns = [
                re.compile(pattern) for pattern in rule_dict['action_patterns']
            ]

            rule = ACLRule(group_name=group_name, allow=allow, action_patterns=action_patterns)
            self.rules.append(rule)

        log.info("Load public action patterns")
        self.public_action_patterns = [
            re.compile(pattern) for pattern in acl_config['public_action_patterns']
        ]

        log.info("Finished initializing ACL engine")

    def has_access_to_action(self, *, user_id: str, action: str) -> bool:
        member_groups = self.group_names_by_member.get(user_id, set())

        for rule in self.rules:
            # Skip this rule if it doesn't apply to this user
            if rule.group_name not in member_groups:
                continue

            for action_pattern in rule.action_patterns:
                if action_pattern.match(action):
                    return rule.allow

        # At this point, we know that none of the defined rules apply to this user,
        # so check for whether this action matches any public action
        for pattern in self.public_action_patterns:
            if pattern.match(action):
                return True

        # None of the rules matched this request, and it wasn't a public action, so deny
        return False
