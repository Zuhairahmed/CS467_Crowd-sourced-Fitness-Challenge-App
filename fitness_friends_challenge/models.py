from fitness_friends_challenge import db

challenge_badges = db.Table('challengebadges',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id')),
    db.Column('badge_id', db.Integer, db.ForeignKey('badge.id')))

user_badges = db.Table('userbadges',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('badge_id', db.Integer, db.ForeignKey('badge.id')))

challenge_chats = db.Table('challengechats',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id')))

challenge_tags = db.Table('challengetags',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

challenge_images = db.Table('challengeimages',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id')),
    db.Column('image_id', db.Integer, db.ForeignKey('image.id')))

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
    chats = db.relationship('Chat', lazy='dynamic')
    favorites = db.relationship('Favorites', lazy='dynamic')
    #walloffame_id = db.Column(db.Integer, db.ForeignKey('walloffame.id'))

class Badge(db.Model):
    __tablename__ = 'badge'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', secondary=user_badges, lazy='dynamic')
    challenges = db.relationship('Challenge', secondary=challenge_badges, lazy='dynamic')
    image = db.Column(db.Text(), nullable=False)

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))

class Kind(db.Model):
    __tablename__ = 'kind'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    challenges = db.relationship('Challenge', lazy='dynamic')

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    challenges = db.relationship('Challenge', secondary=challenge_tags, lazy='dynamic')

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenges = db.relationship('Challenge', secondary=challenge_chats, lazy='dynamic')

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenges = db.relationship('Challenge', secondary=challenge_images, lazy='dynamic')

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenges = db.relationship('Challenge', lazy='dynamic')

class WallOfFame(db.Model):
    __tablename__ = 'walloffame'
    id = db.Column(db.Integer, primary_key=True)
    #users = db.relationship('User', lazy='dynamic')
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))