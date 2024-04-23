from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship(User, backref='posts')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    post = relationship(Post, backref='comments')
    owner = relationship(User, backref='comments')


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    post = relationship(Post, backref='likes')
    owner = relationship(User, backref='likes')


class Followers(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True, nullable=False)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    following_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_following = Column(Boolean, default=False)
    follower = relationship(User, foreign_keys=[follower_id], backref='follower')
    following = relationship(User, foreign_keys=[following_id], backref='following')


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    room = relationship(Room, backref='messages')
    owner = relationship(User, backref='messages')
