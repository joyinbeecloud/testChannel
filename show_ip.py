# encoding: utf-8
from flask import Blueprint
from flask import request
from flask import render_template

show_ip_view=Blueprint("show_ip",__name__)

@show_ip_view.route('')
def show_ip():
    ip=request.remote_addr
    return render_template('show_ip.html',ip=ip)