from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from database.models import Campaign, Target
from database import db
from datetime import datetime
import csv
import io

scenario_bp = Blueprint('scenario', __name__, url_prefix='/scenario')

@scenario_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_campaign():
    if request.method == 'POST':
        # Validate form data
        campaign_name = request.form.get('name')
        vector_type = request.form.get('vector_type')
        targets_file = request.files.get('targets')
        
        if not all([campaign_name, vector_type, targets_file]):
            flash('All fields are required', 'error')
            return redirect(request.url)
        
        # Create new campaign
        new_campaign = Campaign(
            name=campaign_name,
            vector_type=vector_type,
            status='draft'
        )
        db.session.add(new_campaign)
        
        # Process targets file
        try:
            stream = io.StringIO(targets_file.stream.read().decode("UTF8"))
            csv_reader = csv.DictReader(stream)
            for row in csv_reader:
                target = Target(
                    email=row.get('email'),
                    name=row.get('name', ''),
                    position=row.get('position', ''),
                    campaign_id=new_campaign.id
                )
                db.session.add(target)
            
            db.session.commit()
            flash('Campaign created successfully', 'success')
            return redirect(url_for('campaign.view', campaign_id=new_campaign.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error processing targets file: {str(e)}', 'error')
    
    return render_template('scenario/new.html', 
                         vector_types=['email', 'web', 'usb', 'document'])