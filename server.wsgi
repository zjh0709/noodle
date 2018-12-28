import sys
sys.path.insert(0,'/home/ubuntu/noodle')
from noodle.server.hello import app as application

application.run(host="0.0.0.0", debug=True)