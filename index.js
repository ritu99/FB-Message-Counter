var express = require('express');
var app = express();
var fb = require("facebook-chat-api");
var bodyParser = require("body-parser");
var multer = require("multer");

app.use(express.static('views'));

app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

app.set('view engine', 'ejs');

app.get('/', function (req, res) {
   res.render( __dirname + "/views/" + "login.ejs", {data: 'nothing'} );
})

app.post('/',function (req, res) {
   // Prepare output in JSON format
   response = {
      username:req.body.username,
      password:req.body.password
   };

   function compare(a,b) {
     return b.messageCount - a.messageCount;
   }

   var threadCount = 1000;
   fb({email: response.username, password: response.password}, (err, api) => {
       if(err) {
         switch(err.error){
           case 'Wrong username/password.':
              res.render( __dirname + "/views/" + "login.ejs", {data: "error"});
              break;
           case 'login-approval':
              res.render( __dirname + "/views/" + "login.ejs", {data: "login-approval"});
              break;
         }

         return console.error(err);
       }
       // Here you can use the api
       api.getThreadList(0, threadCount, "inbox", (err, arr) => {
         if(err) {
           return console.error(err);
         }
         arr.sort(compare);
         var count = 0;
        //  console.log(arr);

         var result = arr.map(a => a.threadID);
         api.getUserInfo(result, (err, ret) => {
             if(err) return console.error(err);
             for(var i = 0; i < arr.length; i++){
               if(arr[i]["participants"].length > 2) continue;
               if(typeof ret[arr[i]["threadID"]] !== "undefined"){
                 arr[i]["name"] = ret[arr[i]["threadID"]]["name"];
                 arr[i]["imageSrc"] = ret[arr[i]["threadID"]]["thumbSrc"];
               }

             }
             res.render( __dirname + "/views/data.ejs", {data: arr});
             api.logout();
          });

       });

   });

})

var server = app.listen(8081, 'localhost', function () {
   var host = server.address().address
   var port = server.address().port
   console.log(server.address().address)
   console.log("Example app listening at http://%s:%s", host, port)
})
