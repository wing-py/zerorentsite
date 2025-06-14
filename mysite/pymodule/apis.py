from .models import db,User,Order
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app,send_from_directory
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_cors import CORS

apis_bp = Blueprint('apis', __name__)
CORS(apis_bp)
# apis
@apis_bp.route('/apis/getOrders')
def getOrders():
    page = request.args.get('page',0,type=int)
    per_page=100
    total=Order.query.count()
    # print(page)
    # orders = User.query.offset(page).limit(per_page).all()
    orders = Order.query.paginate(page=page,per_page=per_page,error_out=False)
    serialized = [user.to_dict() for user in orders.items]

    print(orders)
    return jsonify({
        'page':page,
        'limit':per_page,
        'total':total,
        'data':serialized,
    })

@apis_bp.route('/apis/postOrder',methods=['POST'])
def postOrder():
    try:
      data = request.get_json()
      print(f"data: {data}")
      required_fields=['name','description','price','publisher_id']
      if not all(field in data for field in required_fields):
        print('error, 缺少必填字段')
        return jsonify({'error':'缺少必填字段'}),400

      # 检查用户是否存在
      if not User.query.filter_by(id=data['publisher_id']).first():
          flash('用户不存在')
          return jsonify({'error':'用户不存在'}),400

      new_order = Order(
          id=str(uuid.uuid4()),
          name=data['name'],
          description = data['description'],
          price = data['price'],
          stat = 'undo',
          publisher_id = data['publisher_id'],
          worker_id = None,
          date=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
      )
      db.session.add(new_order)
      db.session.commit()
      return jsonify({
          'status': 'success',
          'message': '表单提交成功',
          'received_data': data
      }), 200

    except Exception as e:
      print({'error': str(e)})
      return jsonify({'error': str(e)}), 500

@apis_bp.route('/apis/getDevelopers')
def getDevelopers():
    page = request.args.get('page',0,type=int)
    per_page = 10
    total = User.query.count()
    users = User.query.paginate(page=page,per_page=per_page,error_out=False)
    serialized = [user.to_dict() for user in users.items]

    print(users)
    return jsonify({
        'page':page,
        'limit':per_page,
        'total':total,
        'data':serialized,
    })

@apis_bp.route('/apis/register', methods=['POST'])
def register():
    try:
      data = request.get_json()
      print(f"data: {data}")
      required_fields=['name','password','email','phone']
      if not all(field in data for field in required_fields):
        print('error, 缺少必填字段')
        return jsonify({'error':'缺少必填字段'}),400
                # 检查用户名是否已存在
      if User.query.filter_by(username=data['name']).first():
          flash('用户名已存在')
          return jsonify({'error':'用户名已存在'}),400

      # 创建新用户
      new_user = User(
          id=str(uuid.uuid4()),
          username=data['name'],
          password=generate_password_hash(data['password']),
          email=data['email'],
          phone=data['phone'],
      )
      db.session.add(new_user)
      db.session.commit()
      return jsonify({
          'status': 'success',
          'message': '表单提交成功',
          'received_data': data
      }), 200

    except Exception as e:
      print('error, flask wrong')
      return jsonify({'error': str(e)}), 500


@apis_bp.route('/apis/login', methods=['POST'])
def login():
    try:
      data = request.get_json()
      print(f"data: {data}")
      required_fields=['username','password']
      if not all(field in data for field in required_fields):
        print('error, 缺少必填字段')
        return jsonify({'error':'缺少必填字段'}),400
                # 检查用户名是否已存在
      user = User.query.filter_by(username=data['username']).first()
      print(f"data: {data}")
      if not user:
          print('error, 用户不存在')
          return jsonify({'error':'用户不存在'}),400

      if not check_password_hash(user.password, data['password']):
          print('error, 密码错误')
          return jsonify({'error':'密码错误'}),400
      # serialized = [user.to_dict()['id']]
      serialized = {'id':user.id,'username':user.username}

      return jsonify({
          'data': serialized,
          'status': 'success',
          'message': '表单提交成功',
          'received_data': data
      }), 200

    except Exception as e:
        # 5. 错误处理
      print('error, flask wrong')
      return jsonify({'error': str(e)}), 500
