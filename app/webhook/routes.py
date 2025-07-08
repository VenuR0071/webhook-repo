# webhook-repo/app/webhook/routes.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from ..extensions import get_events_collection # Import the function to get the collection

# Define the blueprint with a URL prefix
webhook_bp = Blueprint('webhook_bp', __name__, url_prefix='/webhook')

@webhook_bp.route('/receiver', methods=['POST'])
def receiver():
    events_collection = get_events_collection() # Get the collection

    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    if not payload:
        print("Received empty payload.")
        return jsonify({"message": "Empty payload"}), 400

    print(f"Received GitHub event: {event}")

    event_data = {
        "author": None,
        "action": None,
        "from_branch": None,
        "to_branch": None,
        "timestamp": datetime.utcnow().isoformat() + "Z", # UTC ISO format
        "request_id": None
    }

    try:
        if event == 'push':
            event_data["action"] = "PUSH"
            event_data["author"] = payload['pusher']['name']
            event_data["to_branch"] = payload['ref'].split('/')[-1]
            event_data["request_id"] = payload['after'] # Commit hash

        elif event == 'pull_request':
            pr_info = payload['pull_request']
            event_data["author"] = pr_info['user']['login']
            event_data["from_branch"] = pr_info['head']['ref']
            event_data["to_branch"] = pr_info['base']['ref']
            event_data["request_id"] = str(pr_info['id']) # PR ID

            if payload['action'] == 'closed' and pr_info['merged']:
                event_data["action"] = "MERGE" # Brownie points!
            else:
                event_data["action"] = "PULL_REQUEST"

        else:
            print(f"Unhandled GitHub event type: {event}")
            return jsonify({"message": f"Event type '{event}' not handled"}), 200

        # Store the data in MongoDB
        if event_data["action"]: # Only store if a valid action was identified
            events_collection.insert_one(event_data)
            print(f"Stored {event_data['action']} event: {event_data}")
            return jsonify({"message": f"{event_data['action']} event received and stored"}), 200
        else:
            return jsonify({"message": "No valid action identified from payload"}), 200

    except KeyError as e:
        print(f"KeyError: Missing key in payload - {e}. Payload: {payload}")
        return jsonify({"message": f"Error processing payload: Missing key {e}"}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Payload: {payload}")
        return jsonify({"message": f"Internal server error: {e}"}), 500

# UI Data Endpoint (this endpoint is part of the /webhook blueprint now)
# So the full path will be /webhook/events_api
@webhook_bp.route('/events_api', methods=['GET'])
def get_events_api():
    events_collection = get_events_collection() # Get the collection
    try:
        # Fetch latest 20 events, sorted by timestamp (newest first)
        events_cursor = events_collection.find().sort("timestamp", -1).limit(20)
        events = []
        for event in events_cursor:
            # Convert ObjectId to string for JSON serialization
            event['_id'] = str(event['_id'])
            events.append(event)
        return jsonify(events), 200
    except Exception as e:
        print(f"Error fetching events from MongoDB: {e}")
        return jsonify({"message": f"Error fetching events: {e}"}), 500