from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import config
from models.roles import Roles
from models.users import Users
from models.permissions import Permission
from models.revokeToken import BlockTokenModel
from models.userToken import UserToken
from models.views import View

migrate = Migrate(config.app, config.db, compare_type=True)
config.app.app_context().push()
config.db.init_app(config.app)
config.db.create_all(app=config.app)
config.db.session.commit()


manager = Manager(config.app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
