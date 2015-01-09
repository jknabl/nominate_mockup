import sys, os, config
INTERP = os.path.join(os.environ['HOME'], config.HOST['domain'], 
  'bin', 'python')

if sys.executable != INTERP:
  os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

sys.path.append(config.HOST['domain'])
from ccnomination.app import app as application
