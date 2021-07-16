from fitness_friends_challenge import db

challenge_badges = db.Table('challengebadges',
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey('badge.id'), primary_key=True))

user_badges = db.Table('userbadges',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey('badge.id'), primary_key=True))

challenge_chats = db.Table('challengechats',
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True))

challenge_tags = db.Table('challengetags',
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True))

challenge_images = db.Table('challengeimages',
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True))

class Challenge(db.Model):
    __tablename__ = 'challenge'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    kind_id = db.Column(db.Integer, db.ForeignKey('kind.id'))
    badges = db.relationship('Badge', secondary=challenge_badges, lazy='dynamic')
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id'))
    walloffames = db.relationship('WallOfFame', lazy='dynamic')
    goals = db.relationship('Goal', lazy='dynamic')
    tags = db.relationship('Tag', secondary=challenge_tags, lazy='dynamic')
    chats = db.relationship('Chat', secondary=challenge_chats, lazy='dynamic')
    images = db.relationship('Image', secondary=challenge_images, lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def convert_to_json(self):
        return {'name': self.name}

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)
    firstname = db.Column(db.Text(), nullable=False)
    lastname = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    images = db.relationship('Image', lazy='dynamic')
    badges = db.relationship('Badge', secondary=user_badges, lazy='dynamic')
    challenges = db.relationship('Challenge', lazy='dynamic')
    chats = db.relationship('Chat', lazy='dynamic')

    def convert_to_json(self):
        return {'username': self.username, 'password': self.password,
                'firstname': self.firstname, 'lastname': self.lastname,
                'email': self.email}

class Badge(db.Model):
    __tablename__ = 'badge'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', lazy='dynamic')
    challenges = db.relationship('Challenge', lazy='dynamic')
    image = db.Column(db.Text(), nullable=False)

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge_id'))

class Kind(db.Model):
    __tablename__ = 'kind'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    challenges = db.relationship('Challenge', lazy='dynamic')

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'))

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'))

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'))
    challenges = db.relationship('Challenge', lazy='dynamic')

class WallOfFame(db.Model):
    __tablename__ = 'walloffame'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', lazy='dynamic')
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge_id'))