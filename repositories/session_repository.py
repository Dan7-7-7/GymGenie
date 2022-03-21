from db.run_sql import run_sql
from models.session import Session
from models.member import Member

def save(session):
    sql = "INSERT INTO sessions (name, start_time, duration, capacity) VALUES (%s, %s, %s, %s) RETURNING *"
    values = [session.name, session.start_time, session.duration, session.capacity]
    result = run_sql(sql, values)[0]
    session.id = result['id']
    return session

def select(id):
    session = None
    sql = "SELECT * FROM sessions WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    if result is not None:
        session = Session(result['name'], result['start_time'], result['duration'], result['capacity'], result['id'])
    return session

def select_all():
    sessions = []
    sql = "SELECT * FROM sessions"
    results = run_sql(sql)
    for row in results:
        session = Session(row['name'], row['start_time'], row['duration'], row['capacity'], row['id'])
        sessions.append(session)
    return sessions

def update(session):
    sql = "UPDATE sessions SET (name, start_time, duration, capacity) = (%s, %s, %s, %s) WHERE id = %s"
    values = [session.name, session.start_time, session.duration, session.capacity, session.id]
    run_sql(sql, values)

def members(session):
    members = []
    sql = "SELECT members.* FROM members INNER JOIN bookings ON members.id = bookings.member_id WHERE session_id = %s"
    values = [session.id]
    results = run_sql(sql, values)
    for row in results:
        member = Member(row['name'], row['age'], row['premium'], row['id'])
        members.append(member)
    return members