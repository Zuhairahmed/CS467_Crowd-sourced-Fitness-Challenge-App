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
    name = db.Column(db.Text(), nullable=False, unique=True)
    description = db.Column(db.Text(), nullable=False)
    creator = db.Column(db.Text(), nullable=False)
    kind_id = db.Column(db.Integer, db.ForeignKey('kind.id'))
    badges = db.relationship('Badge', secondary=challenge_badges, lazy='dynamic')
    favorites_id = db.Column(db.Integer, db.ForeignKey('favorites.id', use_alter=True, name='fk_favorites_challenge'))
    walloffames = db.relationship('WallOfFame', backref='walloffame', lazy='dynamic')
    goals = db.relationship('Goal', backref='goal', lazy='dynamic')
    tags = db.relationship('Tag', secondary=challenge_tags, lazy='dynamic')
    chats = db.relationship('Chat', secondary=challenge_chats, lazy='dynamic')
    images = db.relationship('Image', secondary=challenge_images, lazy='dynamic')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    firstname = db.Column(db.Text(), nullable=False)
    lastname = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False, unique=True)
    images = db.relationship('Image', backref='image', lazy='dynamic')
    badges = db.relationship('Badge', secondary=user_badges, lazy='dynamic')
    chats = db.relationship('Chat', backref='chat', lazy='dynamic')
    favorites = db.relationship('Favorites', backref='favorites', lazy='dynamic')
    walloffame_id = db.Column(db.Integer, db.ForeignKey('walloffame.id', use_alter=True, name='fk_walloffame_user'), nullable=True)
    goals_progress = db.relationship('Progress', backref='progress', lazy='dynamic')
    challenges_completed = db.Column(db.Integer, nullable=False)

class Badge(db.Model):
    __tablename__ = 'badge'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', secondary=user_badges, overlaps='badges', lazy='dynamic')
    challenges = db.relationship('Challenge', secondary=challenge_badges, overlaps='badges', lazy='dynamic')
    image = db.Column(db.Text(), nullable=False, unique=True)

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    first_target_number = db.Column(db.Integer, nullable=False)
    second_target_number = db.Column(db.Integer, nullable=False)
    third_target_number = db.Column(db.Integer, nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=True)
    progress_id = db.Column(db.Integer, db.ForeignKey('progress.id'))

class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True)
    first_goal_progress = db.Column(db.Integer, nullable=False)
    second_goal_progress = db.Column(db.Integer, nullable=False)
    third_goal_progress = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goals = db.relationship('Goal', backref='progress_goal', lazy='dynamic')

class Kind(db.Model):
    __tablename__ = 'kind'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    challenges = db.relationship('Challenge', backref='challenge', lazy='dynamic')

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    challenges = db.relationship('Challenge', secondary=challenge_tags, overlaps='tags', lazy='dynamic')

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenges = db.relationship('Challenge', secondary=challenge_chats, overlaps='chats', lazy='dynamic')

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenges = db.relationship('Challenge', secondary=challenge_images, overlaps='images', lazy='dynamic')

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', use_alter=True, name='fk_user_favorites'))
    challenges = db.relationship('Challenge', backref='challenge_favorites', lazy='dynamic')

class WallOfFame(db.Model):
    __tablename__ = 'walloffame'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='user', lazy='dynamic')
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id', use_alter=True, name='fk_challenge_walloffame'))