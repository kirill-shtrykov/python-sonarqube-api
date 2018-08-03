"""
Utility to manage the users on a SonarQube server.
"""
import argparse
from prettytable import PrettyTable
from sonarqube_api.api import SonarAPIHandler


parser = argparse.ArgumentParser(description='Manage users on a SonarQube server')

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

# User management arguments
commands = parser.add_subparsers(help='commands', dest='command')
# List
users_list = commands.add_parser("list", help="Get all the active users of the SonarQube instance")
users_list.add_argument("--deactivated", action='store_true', help="Include deactivated users")
users_list.add_argument("--logins", help="comma-separated list of user logins")
# Create
users_create = commands.add_parser("create", help="Create a user")
users_create.add_argument("login", help="User login")
users_create.add_argument("user_pass", help="User password")
users_create.add_argument("name", help="User name")
users_create.add_argument("--email", help="User email")
# Update
users_update = commands.add_parser("update", help="Update a user")
users_update.add_argument("login", help="User login")
users_update.add_argument("--name", help="User name")
users_update.add_argument("--email", help="User email")
# Deactivate
users_deactivate = commands.add_parser("deactivate", help="Deactivate a user")
users_deactivate.add_argument("login", help="User login")


def main():
    """
    Manage a SonarQube's users, using a
    SonarAPIHandler connected to the given host.
    """
    options = parser.parse_args()
    h = SonarAPIHandler(host=options.host, port=options.port,
                        user=options.user, password=options.password,
                        token=options.authtoken, base_path=options.basepath)

    if options.command == 'list':
        users = h.get_users(options.logins, options.deactivated).json()
        table = PrettyTable(['Login', 'Name', 'Email', 'Groups', 'Active'])
        for user in users['users']:
            table.add_row([user.get('login'),
                           user.get('name'),
                           user.get('email'),
                           user.get('groups'),
                           user.get('active')])
        print(table)
    elif options.command == 'create':
        res = h.create_user(options.login, options.user_pass, options.name, options.email).json()
        print(res['user'])
    elif options.command == 'update':
        res = h.update_user(options.login, options.name, options.email).json()
        print(res['user'])
    elif options.command == 'deactivate':
        res = h.deactivate_user(options.login).json()
        print(res['user'])
