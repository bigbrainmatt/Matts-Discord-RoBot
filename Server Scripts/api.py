from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import asyncio

from bot import bot

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

@app.route('/user_join', methods=['POST'])
@limiter.limit("5 per minute")
def user_join():
    username = request.args.get("username")
    userID = request.args.get("userID")
    displayName = request.args.get("displayName")
    accountAge = request.args.get("accountAge")
    membershipStatus = request.args.get("membershipStatus")
    joinTimestamp = request.args.get("joinTimestamp")
    serverId = request.args.get("serverId")

    async def log_to_discord():
        cog = bot.get_cog("onUserJoinGame")
        if cog:
            userInfo = [
                username,
                userID,
                displayName,
                accountAge,
                membershipStatus,
                joinTimestamp,
                serverId
            ]

            await cog.log_to_discord(userInfo)

    bot.loop.create_task(log_to_discord())
    return jsonify({"message": "User join registered successfully"}), 200

def run_api(debug=False, port=5000):
    app.run(debug=debug, port=port, use_reloader=False)