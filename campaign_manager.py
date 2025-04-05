from flask import Blueprint, request, jsonify, current_app
from database.models import Campaign, Target, Event, Response
from database import db
from datetime import datetime
from sqlalchemy import func

campaign_bp = Blueprint('campaign', __name__, url_prefix='/campaign')

@campaign_bp.route('/', methods=['GET'])
def list_campaigns():
    try:
        campaigns = Campaign.query.all()
        return jsonify({
            'success': True,
            'campaigns': [{
                'id': c.id,
                'name': c.name,
                'vector_type': c.vector_type,
                'status': c.status,
                'created_at': c.created_at.isoformat(),
                'target_count': len(c.targets),
                'event_count': len(c.events)
            } for c in campaigns]
        })
    except Exception as e:
        current_app.logger.error(f"Failed to list campaigns: {str(e)}")
        return jsonify({'error': str(e)}), 500

@campaign_bp.route('/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        
        # Get campaign metrics
        metrics = {
            'emails_sent': db.session.query(func.count(Event.id))
                .filter(Event.campaign_id == campaign_id)
                .filter(Event.event_type == 'email_sent')
                .scalar(),
            'emails_opened': db.session.query(func.count(Event.id))
                .filter(Event.campaign_id == campaign_id)
                .filter(Event.event_type == 'email_opened')
                .scalar(),
            'links_clicked': db.session.query(func.count(Event.id))
                .filter(Event.campaign_id == campaign_id)
                .filter(Event.event_type == 'link_clicked')
                .scalar(),
            'credentials_captured': db.session.query(func.count(Response.id))
                .join(Target)
                .filter(Target.campaign_id == campaign_id)
                .scalar()
        }
        
        return jsonify({
            'success': True,
            'campaign': {
                'id': campaign.id,
                'name': campaign.name,
                'vector_type': campaign.vector_type,
                'status': campaign.status,
                'created_at': campaign.created_at.isoformat(),
                'sandbox_mode': campaign.sandbox_mode,
                'metrics': metrics
            }
        })
    except Exception as e:
        current_app.logger.error(f"Failed to get campaign: {str(e)}")
        return jsonify({'error': str(e)}), 500

@campaign_bp.route('/<int:campaign_id>/status', methods=['PUT'])
def update_status(campaign_id):
    try:
        data = request.json
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
            
        campaign = Campaign.query.get_or_404(campaign_id)
        campaign.status = data['status']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f"Campaign status updated to {data['status']}"
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to update campaign status: {str(e)}")
        return jsonify({'error': str(e)}), 500