from flask import Blueprint, render_template, current_app
from database.models import Campaign, Event, Response
from database import db
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def generate_engagement_chart(campaign_id):
    """Generate engagement timeline chart as base64 image"""
    try:
        # Get events from last 7 days
        time_threshold = datetime.utcnow() - timedelta(days=7)
        events = Event.query.filter(
            Event.campaign_id == campaign_id,
            Event.timestamp >= time_threshold
        ).order_by(Event.timestamp).all()

        # Prepare data
        event_counts = {}
        for event in events:
            date_str = event.timestamp.strftime('%Y-%m-%d')
            if date_str not in event_counts:
                event_counts[date_str] = {'email_opened': 0, 'link_clicked': 0, 'form_submitted': 0}
            event_counts[date_str][event.event_type] += 1

        # Create DataFrame
        df = pd.DataFrame.from_dict(event_counts, orient='index')
        df = df.reindex(sorted(df.index), axis=0)

        # Plot
        plt.figure(figsize=(10, 5))
        df.plot(kind='bar', stacked=True, ax=plt.gca())
        plt.title('Engagement Timeline')
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    except Exception as e:
        current_app.logger.error(f"Failed to generate chart: {str(e)}")
        return None

@dashboard_bp.route('/<int:campaign_id>')
def view_dashboard(campaign_id):
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        
        # Get basic stats
        stats = {
            'targets': len(campaign.targets),
            'emails_sent': Event.query.filter_by(
                campaign_id=campaign_id,
                event_type='email_sent'
            ).count(),
            'emails_opened': Event.query.filter_by(
                campaign_id=campaign_id,
                event_type='email_opened'
            ).count(),
            'credentials_captured': Response.query.join(
                Target
            ).filter(
                Target.campaign_id == campaign_id
            ).count()
        }

        # Generate chart
        chart_img = generate_engagement_chart(campaign_id)

        return render_template(
            'dashboard/view.html',
            campaign=campaign,
            stats=stats,
            engagement_chart=chart_img
        )

    except Exception as e:
        current_app.logger.error(f"Failed to load dashboard: {str(e)}")
        return render_template('error.html', error=str(e)), 500