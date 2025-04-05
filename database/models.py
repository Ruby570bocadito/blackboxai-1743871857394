from datetime import datetime
from database import db

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    vector_type = db.Column(db.String(50), nullable=False)  # email/web/usb/document
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')  # draft/active/completed
    sandbox_mode = db.Column(db.Boolean, default=True)
    targets = db.relationship('Target', backref='campaign', lazy=True)
    events = db.relationship('Event', backref='campaign', lazy=True)

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80))
    position = db.Column(db.String(80))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    responses = db.relationship('Response', backref='target', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # email_open/link_click/form_submit
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credentials = db.Column(db.Text)  # JSON formatted
    payload_executed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    target_id = db.Column(db.Integer, db.ForeignKey('target.id'), nullable=False)