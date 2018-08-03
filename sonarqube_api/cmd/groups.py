"""
Utility to manage the groups on a SonarQube server.
"""
import argparse
from prettytable import PrettyTable
from sonarqube_api.api import SonarAPIHandler


parser = argparse.ArgumentParser(description='Manage groups on a SonarQube server')

# Connection arguments
parser.add_argument('--host', dest='host', type=str,
                    default='http://localhost',
                    help='Host of the SonarQube server')
parser.add_argument('--port', dest='port', type=str,
                    default='9000',
                    help='Port of the SonarQube server instance')
parser.add_argument('--user', dest='user', type=str,
                    default=None,
                    help='Authentication user')
parser.add_argument('--password', dest='password', type=str,
                    default=None,
                    help='Authentication password')
parser.add_argument('--authtoken', dest='authtoken', type=str,
                    default=None,
                    help='Authentication token')
parser.add_argument('--basepath', dest='basepath', type=str,
                    default=None,
                    help='The base-path of the Sonar installation. Defaults to "/"')

# Groups management arguments
commands = parser.add_subparsers(help='commands', dest='command')
# List
groups_list = commands.add_parser("list", help="Search for user groups")
groups_list.add_argument("--fields", help="Comma-separated list of the fields")
groups_list.add_argument("--query", help="Limit search to names in this query")
# Create
groups_create = commands.add_parser("create", help="Create a group")
groups_create.add_argument("name", help="Name for the new group")
groups_create.add_argument("--description", help="Description for the new group")
# Update
groups_update = commands.add_parser("update", help="Update a group")
groups_update.add_argument("gid", help="Identifier of the group")
groups_update.add_argument("--name", help="New name for the group")
groups_update.add_argument("--description", help="New description for the group")
# Delete
groups_delete = commands.add_parser("delete", help="Delete a group")
groups_delete.add_argument("--gid", help="Group id")
groups_delete.add_argument("--name", help="Group name")
# Add user
groups_adduser = commands.add_parser("add-user", help="Add a user to a group")
groups_adduser.add_argument("login", help="User login")
groups_adduser.add_argument("--gid", help="Group id")
groups_adduser.add_argument("--name", help="Group name")
# Remove user
groups_remuser = commands.add_parser("remove-user", help="Remove a user from a group")
groups_remuser.add_argument("login", help="User login")
groups_remuser.add_argument("--gid", help="Group id")
groups_remuser.add_argument("--name", help="Group name")
# List users
groups_lstusers = commands.add_parser("list-users", help="List users in a group")
groups_lstusers.add_argument("--gid", help="Group id")
groups_lstusers.add_argument("--name", help="Group name")
groups_lstusers.add_argument("--query", help="Limit search to names in this query")


def main():
    """
    Manage a SonarQube's groups, using a
    SonarAPIHandler connected to the given host.
    """
    options = parser.parse_args()
    h = SonarAPIHandler(host=options.host, port=options.port,
                        user=options.user, password=options.password,
                        token=options.authtoken, base_path=options.basepath)

    if options.command == 'list':
        groups = h.get_groups(options.fields, options.query).json()
        table = PrettyTable(['ID', 'Name', 'Description', 'Members', 'Default'])
        for group in groups['groups']:
            table.add_row([group.get('id'),
                           group.get('name'),
                           group.get('description'),
                           group.get('membersCount'),
                           group.get('default')])
        print(table)
    elif options.command == 'create':
        res = h.create_group(options.name, options.description).json()
        print(res['group'])
    elif options.command == 'update':
        res = h.update_group(options.gid, options.name, options.description).json()
        print(res['group'])
    elif options.command == 'delete':
        res = h.delete_group(options.gid, options.name)
        if res.status_code == 204:
            print("Group was successfully deleted")
        else:
            print("Error[%s] %s" % (res.status_code, res.reason))
    elif options.command == 'add-user':
        res = h.add_user_group(options.login, options.gid, options.name)
        if res.status_code == 204:
            print("User was successfully added")
        else:
            print("Error[%s] %s" % (res.status_code, res.reason))
    elif options.command == 'remove-user':
        res = h.remove_user_group(options.login, options.gid, options.name)
        if res.status_code == 204:
            print("User was successfully removed")
        else:
            print("Error[%s] %s" % (res.status_code, res.reason))
    elif options.command == 'list-users':
        users = h.get_group_users(options.gid, options.name, options.query).json()
        table = PrettyTable(['Login', 'Name'])
        for user in users['users']:
            table.add_row([user['login'], user['name']])
        print(table)
