from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import connect

session = connect('sqlite:///restaurantMenu.db')


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>" \
                          "<h2>What would you like me to say?</h2>" \
                          "<input name='message' type='text' >" \
                          "<input type='submit' value='Submit'> </form>"
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
                    output += "<a href='/restaurants/%s/edit'>Edit</a>&nbsp;" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</li>"

                output += "</ul>"
                output += "<a href='/restaurants/new'>Create a new restaurant</a>"
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

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h2>"
                    output += myRestaurantQuery.name
                    output += "</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name='updateRestaurantName' type='text' placeholder='New Restaurant Name'	>"
                    output += "<input type='submit' value='Submit'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h2>Do you really want to delete "
                    output += myRestaurantQuery.name
                    output += "?</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type='submit' value='Delete'>"
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

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updateRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if myRestaurantQuery:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if myRestaurantQuery:
                        session.delete(myRestaurantQuery)
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
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
