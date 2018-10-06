from flask import Flask, render_template, redirect, url_for, request, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Regexp, DataRequired
from flask import jsonify
from random import uniform as rr
from random import randint as ri
from sklearn.cluster import DBSCAN
from math import *
import numpy as np
import json
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '1dbc1cfb04729cb8a714c2122d5b3edb'


class LoginForm(FlaskForm):
	username = StringField('Phone Number: ', validators=[Length(min=10, max=10),
											Regexp('[789][\d]{9}', message='Wrong')
											],
										 render_kw={"placeholder": "Phone number..."})
	submit = SubmitField('Enter')


class AdminLoginForm(FlaskForm):
	latitude = StringField('Enter Latitude: ', validators=[DataRequired()],
										 render_kw={"placeholder": "Longitude..."})

	longitude = StringField('Enter Longitude: ', validators=[DataRequired()],
										 render_kw={"placeholder": "Longitude..."})
	submit = SubmitField('Enter')


def dist(x1, y1, x2, y2):
	return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
	form = LoginForm()

	if form.validate_on_submit():
		return redirect('map')

	return render_template('index.html', form=form)


@app.route('/map', methods=['GET', 'POST'])
def map():
	if request.method=='GET':
		return render_template('map.html')
	else:
		lat = request.form.get('latitude')
		lon = request.form.get('longitude')
		X = request.form.get('points')
		# print(request.form)
		dat = json.loads(X)
		print (type(dat))
		L = np.array(dat)
		L = L * 10000
		clustering = DBSCAN(eps=20, min_samples=5).fit(L)
		core_samples = clustering.core_sample_indices_
		labels = clustering.labels_
		n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
		clusters = [L[labels == i] for i in range(n_clusters_)]
		print(clusters)
		S = []
		for i in clusters:
			S.append(i.shape[0])
		m = max(S)
		geofence = clusters[S.index(m)].tolist()
		max_dist = 0
		mx = 0
		my = 0
		for i in range(len(geofence)):
			curr = geofence[i]
			for j in range(i + 1,len(geofence)):
				pt = geofence[j]
				d = dist(curr[0],curr[1],pt[0],pt[1])
				if d > max_dist:
					max_dist = d
					mx = float(curr[0] + pt[0]) / 2
					my = float(curr[1] + pt[1]) / 2

		max_dist = 0
		px = 0
		py = 0
		for i in range(len(geofence)):
			curr = geofence[i]
			d = dist(curr[0],curr[1],mx,my)
			if d > max_dist:
				max_dist = d
				px = curr[0]
				py = curr[1]
		radius = dist(px, py, mx, my)
		print(radius, " ", mx, " ", my)
		return jsonify({"mx":mx / 10000, "my":my/10000,"radius":radius})
		

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	form = AdminLoginForm()
	with open('../dataCSV.csv', 'a', newline='') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow([form.latitude.data, form.longitude.data])

	return render_template('admin.html', form=form)


if __name__ == '__main__':
	app.run(debug=True)
