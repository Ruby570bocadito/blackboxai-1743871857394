from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from database.models import Campaign, Event
from database import db
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
import socket

email_bp = Blueprint('email', __name__, url_prefix='/email')

def create_tracking_pixel(campaign_id, target_id):
    """Generate HTML for tracking pixel with unique identifiers"""
    pixel_id = uuid.uuid4().hex
    return f'<img src="{current_app.config["BASE_URL"]}/track/{campaign_id}/{target_id}/{pixel_id}" width="1" height="1" alt="">'

@email_bp.route('/send', methods=['POST'])
def send_campaign():
    data = request.json
    if not all(k in data for k in ['campaign_id', 'subject', 'template', 'targets']):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        campaign = Campaign.query.get(data['campaign_id'])
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        # SMTP connection setup
        smtp = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        if current_app.config['MAIL_USE_TLS']:
            smtp.starttls()
        smtp.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])

        sent_count = 0
        for target in data['targets']:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = data['subject']
                msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
                msg['To'] = target['email']

                # Add tracking pixel
                html_content = data['template'].replace(
                    '<!-- TRACKING_PIXEL -->', 
                    create_tracking_pixel(campaign.id, target['id'])
                )

                msg.attach(MIMEText(html_content, 'html'))
                smtp.send_message(msg)
                sent_count += 1

                # Log email sent event
                event = Event(
                    event_type='email_sent',
                    ip_address=socket.gethostbyname(socket.gethostname()),
                    campaign_id=campaign.id,
                    target_id=target['id']
                )
                db.session.add(event)

            except Exception as e:
                current_app.logger.error(f"Failed to send to {target['email']}: {str(e)}")
                continue

        db.session.commit()
        smtp.quit()
        return jsonify({
            'success': True,
            'sent': sent_count,
            'failed': len(data['targets']) - sent_count
        })

    except Exception as e:
        current_app.logger.error(f"Email campaign failed: {str(e)}")
        return jsonify({'error': str(e)}), 500