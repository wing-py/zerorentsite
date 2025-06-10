from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from .models import db, Order, User, Comment

user_bp = Blueprint('user', __name__)

# 寻找开发者
@user_bp.route('/list_worker')
def list_worker():
    users = User.query.all()
    return render_template('list_worker.html', users=users)