from flask import Flask,render_template,request
import sqlite3
import plotly.graph_objs as go
app = Flask(__name__)

@app.route('/')
@app.template_filter()
def index():
	conn = sqlite3.connect('crime.db')
	cursor = conn.cursor()
	query = "SELECT SUM(Vandalism),SUM(Assault),SUM(Burglary),SUM(Robbery),SUM(Theft),SUM(Other),SUM(Arrest),SUM(Shooting) FROM DailyStats"
	rows = cursor.execute(query).fetchall()
	labels = ['Vandalism','Assault','Burglary','Robbery','Theft','Other','Arrest','Shooting']
	values = [x for x in rows[0]]

	fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
	div = fig.to_html(full_html=False)

	return render_template('index.html',plot_div=div)

@app.route('/handle_form',methods=["POST"])
def handle_the_form():
	start = request.form['start']
	end = request.form['end']
	chart = request.form['chart']
	conn = sqlite3.connect('crime.db')
	cursor = conn.cursor()
	query = "SELECT COUNT(Id),Month FROM (SELECT * FROM Crimes WHERE date(Day) BETWEEN '{}' AND '{}') T GROUP BY MONTH".format(start,end)
	rows = cursor.execute(query).fetchall()
	xvals,yvals = [x[1] for x in rows],[x[0] for x in rows]
	data = []
	line,bar = False,False
	if chart=='line':
		data = go.Scatter(x=xvals,y=yvals)
		line = True
	if chart== 'bar':
		data = go.Bar(x=xvals,y=yvals)
		bar = True
	basic_layout = go.Layout(title="Cumulative data from {} to {}".format(start,end))
	fig = go.Figure(data=data,layout=basic_layout)
	div = fig.to_html(full_html=False)
	return render_template('graph.html',plot_div=div,start=start,end=end,line=line,bar=bar)


@app.route('/details',methods=["GET",'POST'])
def detail():
	start = request.form['start']
	end = request.form['end']
	chart = request.form['chart']
	conn = sqlite3.connect('crime.db')
	cursor = conn.cursor()
	labels = ['Vandalism','Assault','Burglary','Robbery','Theft','Other','Arrest','Shooting']
	data = []
	for l in labels:
		if request.form.get(l):
			query = "SELECT SUM({}),Month FROM DailyStats D INNER JOIN (SELECT * FROM Crimes C WHERE date(Day) BETWEEN '{}' AND '{}') T ON D.Dates=T.Dates GROUP BY Month".format(l,start,end)
			rows = cursor.execute(query).fetchall()
			xvals,yvals = [x[1] for x in rows],[x[0] for x in rows]
			if chart == 'bar':
				data.append(go.Bar(name=l,x=xvals,y=yvals))
			if chart == 'line':
				data.append(go.Scatter(name=l,x=xvals,y=yvals))
	fig = go.Figure(data=data)
	div = fig.to_html(full_html=False)
	return render_template('detail.html',plot_div=div)

if __name__=='__main__':
	print("starting Flask app",app.name)
	app.run(debug=True)