import sys
import json
import os
import socket

def request(dest, pedido):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(dest)
	request = 'GET {0} HTTP/1.1\nHost: {1}:{2}\n\n'.format(pedido, dest[0], dest[1]).encode()
	sock.send(request)
	data = b''
	
	while True:
		resposta = sock.recv(1024)
		if not resposta:
			break
		data += resposta
	
	sock.close()

	return data.decode().split('\r\n\r\n')[1]

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Inicialização incorreta')
		sys.exit()

	ip, port = sys.argv[1].split(':')
	opt = int(sys.argv[2])
	dest = (ip, int(port))

	redes = json.loads(request((ip, int(port)), '/api/ix'))['data']
	saida = []

	if opt == 0:
		dicionario = {}
		for rede in redes:
			respostas = json.loads(request(dest, '/api/ixnets/{0}'.format(rede['id'])))['data']
			
			for resposta in respostas:
				if not resposta['net_id'] in dicionario:
					nome = json.loads(request(dest, '/api/netname/{0}'.format(resposta['net_id'])))['data']
					dicionario[resposta['net_id']] = [resposta['net_id'],nome]
				
				dicionario[resposta['net_id']].append(resposta['ix_id'])
		
		for rede in dicionario.values():
			saida.append([str(rede[0]), rede[1], str(len(set(rede[2:])))])
	elif opt == 1:
		for rede in redes:
			respostas = json.loads(request(dest, '/api/ixnets/{0}'.format(rede['id'])))['data']
			ids = [no['net_id'] for no in respostas]
			saida.append([str(rede['id']),rede['name'],str(len(set(ids)))])

	for linha in saida:
		print('\t'.join(linha))