from flask import Flask, render_template, redirect, request, jsonify, Blueprint

user = Blueprint('user', __name__)

@user.route('/login', methods=["GET"])
def login():
    return render_template('login.html')

@user.route('/register', methods=["GET"])
def register():
    return render_template('register.html')