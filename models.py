from peewee import *
from flask_login import UserMixin
from datetime import date, datetime
import os
from playhouse.db_url import connect

DATABASE = connect(os.environ.get('DATABASE_URL'))
DATABASE = PostgresqlDatabase('better_app', host='localhost', port=5432)

class Person(UserMixin, Model):
    first_name = CharField()
    last_name = CharField()
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE       
    
class PersonSetting(Model):
    ACTIVE_STATUSES = (
        (0, "Mostly sedatary (less than 2 hrs a week)"),
        (1, "Moderate (2-4 hrs a week)"),
        (2, "Mostly active (more than 4 hrs a week)")
    )

    GOALS = (
        (0, "Feel more rested (sleep focused)"),
        (1, "Feel happier (mood focused)"),
        (2, "Feel healthier (fitness/diet focused)"),
        (3, "Feel better (all of the above)")
    )
    person = ForeignKeyField(Person, backref='settings')
    active_status = IntegerField(choices=ACTIVE_STATUSES)
    goal = IntegerField(choices=GOALS)
    zip_code = CharField()
    
    def get_status_label(self):
        return dict(self.ACTIVE_STATUSES)[self.active_status]
    
    def get_goal(self):
        return dict(self.GOALS)[self.goal]

    class Meta:
        database = DATABASE

class Fitness(Model):
    person=ForeignKeyField(Person, backref='workouts')
    #############MAKE THESE REQUIRED############
    exercise_name = CharField()
    calories = IntegerField()
    time_duration = IntegerField()
    #############MAKE THESE REQUIRED############

    repetitions = IntegerField()
    sets = IntegerField()
    weight = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE

class Mood(Model):
    RATINGS = (
        (0, "Wow, today sucks!"),
        (1, "Not good, but I guess it could be worse."),
        (2, "Ya know, I'm alright today."),
        (3, "Today's been kinda great."),
        (4, "This was the most amazing day!")
    )
    
    person = ForeignKeyField(Person, backref='moods')
    date = DateField(
        formats="%d/%m/%Y",
        default=date.today
    )
    rating = IntegerField(choices=RATINGS)
    
    def get_rating(self):
        return dict(self.RATINGS)[self.rating]

    class Meta:
        database = DATABASE

class Meal(Model):
    person = ForeignKeyField(Person, backref='meals')
    meal_name = CharField()
    protein = IntegerField()
    carbs = IntegerField()
    fat = IntegerField()
    total_calories = IntegerField()
    created_at = DateTimeField(
        default=datetime.now
    )

    class Meta:
        database = DATABASE

class Sleep(Model):
    person = ForeignKeyField(Person, backref='sleeps')
    date = DateField(
        formats="%d/%m/%Y",
        default=date.today
    )
    start_time = TimeField(
        formats='%H:%M',
        default=datetime.now
    )
    end_time = TimeField(
        formats='%H:%M',
        default=datetime.now
    )

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Person, PersonSetting, Fitness, Mood, Meal, Sleep], safe=True)
    print("TABLES Created")
    DATABASE.close()
