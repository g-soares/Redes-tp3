from flask import Flask, Response, json
import os
import sys	

app = Flask(__name__)

netFile = None
ixFile = None
netIxLanFile = None

@app.route('/api/ix')
def endPoint1():
	data = {'data': json.load(open(ixFile,'r'))['data']}

	return  Response(response=json.dumps(data), status=200, mimetype='application/json')

@app.route('/api/ixnets/<ixId>')
def endPoint2(ixId):
	redes = json.load(open(netIxLanFile,'r'))['data']
	identificadores = []

	for rede in redes:
		if rede['ix_id'] == int(ixId):
			identificadores.append(rede)

	data  = {'data': identificadores}

	return Response(response=json.dumps(data), status=200, mimetype='application/json')

@app.route('/api/netname/<netId>')
def endPoint3(netId):
	redes = json.load(open(netFile,'r'))['data']
	nome = None
	
	for rede in redes:
		if rede['id'] == int(netId):
			nome = rede['name']

	data = {'data': nome}

	return Response(response=json.dumps(data), status=200, mimetype='application/json')

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print('Inicialização incorreta')
		sys.exit()

	PORT = int(sys.argv[1])
	netFile = sys.argv[2]
	ixFile = sys.argv[3]
	netIxLanFile = sys.argv[4]

	port = int(os.environ.get("PORT", PORT))
	app.run( host='0.0.0.0', port=port)