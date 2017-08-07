var express = require('express');
var app = express();
var fb = require("facebook-chat-api");
var bodyParser = require("body-parser");
var multer = require("multer");

app.use(express.static('static'));
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

app.get('/', function (req, res) {
   res.sendFile( __dirname + "/" + "index.html" );
})

function compare(a,b) {
  return a.messageCount - b.messageCount;
}

app.post('/login',function (req, res) {
   // Prepare output in JSON format
   response = {
      username:req.body.username,
      password:req.body.password
   };

   console.log(response);
   fb({email: response.username, password: response.password}, (err, api) => {
       if(err) return console.error(err);
       // Here you can use the api
       api.getThreadList(0,300, "inbox", (err, arr) => {
         if(err) return console.error(err);
         arr.sort(compare);
       });
       api.logout()
   });

   res.end("Logged In - logging out now!");
})

var server = app.listen(8081, 'localhost', function () {
   var host = server.address().address
   var port = server.address().port
   console.log(server.address().address)
   console.log("Example app listening at http://%s:%s", host, port)
})
