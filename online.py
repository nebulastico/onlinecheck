import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import argparse
import eventlet
from colorama import Fore, Style, init

eventlet.monkey_patch()
init(autoreset=True)

fichero=str()
dominio=str()
argnum=int()
SSL= str()
http=str()
of=str()
sdf=str()
arch=str()
correctos=list()
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.1 Safari/537.36'}

parser = argparse.ArgumentParser(description='Online subdomains tester by N3bula')

parser.add_argument("-i", type=str, dest="inputfile", help="Input file (format list file)")
parser.add_argument("-d", type=str, dest="domain", help="Domain")
parser.add_argument("-sdf", type=str, dest="sdf", help="Subdomains list")
parser.add_argument("-o",type=str, dest="of", help="Output file with online webpage subdomains")
parser.add_argument("-ssl", action="store_true", help="If have ssl cypher")
parser.add_argument("-t", type=int, dest="timeout",help="Timeout (sec)", default=10)
parser.add_argument("-v", action="store_true",help="Verbose mode")

args = parser.parse_args()

if args.ssl:
	http="https://"
else:
	http="http://"

def saveOutputFile(fn,lista):
	with open(fn, 'w') as f:
		for item in lista:
			item=item+"\n"
			f.write(item)

def fileToList(fpath):
	lista=list()
	fi=open(fpath,"r")
	for linea in fi:
		linea=linea.rstrip()
		linea=linea.lstrip()
		if not "http://" or "https://" in linea:
			linea=http+linea
		lista.append(linea)
	return lista


def subdomainComposer(fpath):
	lista=list()
	fi=open(fpath,"r")
	for linea in fi:
		linea=linea.rstrip()
		linea=linea.lstrip()
		if not ("http://" or "https://") in linea:
			linea=http+linea+"."+args.domain
		lista.append(linea)
	return lista

s = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504, 508, 511])

s.mount(http, HTTPAdapter(max_retries=retries))

print("[~] Searching...")

if args.inputfile:	inputf=fileToList(args.inputfile)
if args.sdf:	inputf=subdomainComposer(args.sdf)

for linea in inputf:
	if args.v:	print("Testing:",linea)
	try:
		with eventlet.Timeout(args.timeout):
			respuesta=s.get(linea,headers=header, verify=False, timeout=(3.05, args.timeout))
		if respuesta.status_code==200:
			correctos.append(linea)
			if args.v: print(Fore.GREEN+Style.BRIGHT+"[+] Founded!:\t"+linea)
		else:
			if args.v: print(Fore.RED+"[-] Bad req.!:\t",Fore.RED+linea)
		#s.session().close()
	except requests.exceptions.RequestException:
		if args.v: print(Fore.RED+"[-] Bad req.!:\t"+linea)
	except eventlet.timeout.Timeout:
		if args.v: print(Fore.RED+"[-] Timeout!:\t"+linea)
if args.of:	saveOutputFile(args.of,correctos)

print("\n############### Founded! ##############\n")
for item in correctos:
	print("[+]",item)


