from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from connect import *

session = connect('sqlite:///restaurantMenu.db')

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output += "</body></html>"
				self.wfile.write(output)
				return
				
				
			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()			
				
				output = ""
				output += "<html><body>"
				output += "<ul>"
				for restaurant in restaurants:
					output += "<li>"
					output += restaurant.name
					output += "&nbsp;&nbsp;"
					output += "<a href='#'>Edit</a>"
					output += "<a href='#'>Delete</a>"
					output += "</li>"
					
				output += "</ul>"
				output += "</body></html>"
				self.wfile.write(output)
				return
				
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output += "<html><body>"
				output += "Create a new restaurant!"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
				output += "<h2>What is the restaurant's name?</h2>"
				output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'	>"
				output += "<input type='submit' value='Submit'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				return
				
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(301)
				self.end_headers()
				
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')
					
				output = ""
				output += "<html><body>"
				output += "<h2>Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]
				
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
				output += "</body></html>"
				
				self.wfile.write(output)
				
			if self.path.endswith("/restaurants/new"):			
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
					
					newRestaurant = Restaurant(messagecontent[0])
					session.add(newRestaurant)
					session.commit()
					
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
					
				
			
			
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webserverHandler)
		print ("Web server running on port %s" % port)
		server.serve_forever()
		
		
	except KeyboardInterrupt:
		print ("^C entered, stopping web server...")
		server.socket.close()

if __name__ == '__main__':
	main()
	