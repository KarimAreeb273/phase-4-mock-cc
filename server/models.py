from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    serialize_rules = ('-hero_powers', '-powers.heroes',
                       '-created_at', 'updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='hero')
    powers = association_proxy('hero_powers', 'powers')

# class Hero(db.Model, SerializerMixin):
#     __tablename__ = 'hero'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     super_name = db.Column(db.String, unique=True, nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

#     hero_powers = db.relationship('HeroPower', back_populates='hero')
#     powers = association_proxy('hero_powers', 'powers')
#     serialize_rules = ('-hero_powers', '-created_at', '-updated_at', '-powers.created_at', '-powers.updated_at', '-powers.hero')

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('-hero_powers', '-heroes.powers',
                       '-created_at', 'updated_at')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='power')

    @validates('description')
    def validate_description(self, key, description):
        if not description and len(description) < 20:
            raise ValueError('Description must exist and be at least 20 characters long.')
        return description

# class Power(db.Model, SerializerMixin):
#     __tablename__ = 'power'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)
#     description = db.Column(db.String, nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

#     hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all,delete, delete-orphan")
#     heros = association_proxy('hero_powers', 'hero')
#     serialize_rules = ('-hero_powers', '-created_at', '-updated_at', '-hero.power')

#     @validates('description')
#     def validate_description(self, key, value):
#         if len(value) < 20:
#             raise ValueError('Invalid description length')
#         return value

class HeroPower(db.Model,SerializerMixin):
    __tablename__ = 'hero_powers'

    serialize_rules = ('-hero.hero_powers', '-hero.powers',
                       '-power.hero_powers', '-power.heroes',
                       '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    @validates('strength')
    def validate_strength(self, key, strength):
        if not strength == 'Strong' and not strength == 'Weak' and not strength == 'Average':
            raise ValueError('Invalid strength, must be "Strong", "Weak" or "Average".')
        return strength

# class HeroPower(db.Model, SerializerMixin):
#     __tablename__ = 'hero_powers'

#     id = db.Column(db.Integer, primary_key=True)
#     strength = db.Column(db.String, nullable=False)
#     hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
#     power_id = db.Column(db.Integer, db.ForeignKey('power.id'))
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

#     hero = db.relationship('Hero', back_populates='hero_powers')
#     power = db.relationship('Power', back_populates='hero_powers')

#     serialize_rules = ('-hero.power', '-hero.hero_powers', '-power.hero', '-power.hero_powers', '-created_at', '-updated_at')

#     @validates('strength')
#     def validate_strength(self, key, value):
#         if not value == 'Strong' or 'Weak' or 'Average':
#             raise ValueError("Invalid Type")
#         return value

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)

