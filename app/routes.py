from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.models import Ticket
from app.schemas import TicketSchema
from app.db import db

ticket_routes = Blueprint('ticket_routes', __name__)

ticket_schema = TicketSchema()
ticket_schemas = TicketSchema(many=True)

@ticket_routes.route('/tickets', methods=['POST'])
def create_ticket():
    try:
        data = request.get_json()
        ticket_data = ticket_schema.load(data)
        new_ticket = Ticket(
            eventName=ticket_data['eventName'],
            location=ticket_data['location'],
            time=ticket_data['time']
        )

        db.session.add(new_ticket)
        db.session.commit()

        return jsonify(ticket_schema.dump(new_ticket)), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@ticket_routes.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket_by_id(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify(ticket_schema.dump(ticket)), 200

@ticket_routes.route('/tickets/<int:ticket_id>', methods=['PATCH'])
def use_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)

    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    if ticket.isUsed:
        return jsonify({"message": "Ticket is already used"}), 400

    ticket.isUsed = True
    db.session.commit()

    return jsonify({"message": "Ticket marked as used", "ticket": ticket_schema.dump(ticket)}), 200

@ticket_routes.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f"Ticket {ticket_id} deleted"}), 200



@ticket_routes.route('/tickets/all', methods=['GET'])
def get_all_tickets():
    tickets = Ticket.query.all()
    result = ticket_schema.dump(tickets, many=True)
    return jsonify(result), 200
