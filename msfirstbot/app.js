var builder = require('botbuilder');

var connector = new builder.ConsoleConnector().listen();
var bot = new builder.UniversalBot(connector);
var model = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/0461769f-c4f5-4ed2-9136-c10d96b45fee?subscription-key=96d95462721b41629fed437056c857c6&verbose=true&q=';
var recognizer = new builder.LuisRecognizer(model);
var intents = new builder.IntentDialog({recognizers : [recognizer]})
  .matches("getWeather", [
    function(session, args, next){
      var where = builder.EntityRecognizer.findEntity(args.entities, "where");
      if(!where){
        session.send("Where abouts?");
      }
      session.send(`The user wants to know the weather in ${where.entity}`);
      console.log(args);
  }])
  .matches("None", [
    function(session, args, next){
      session.send("Hello");
    }])
    .onDefault((session) => {
      session.send('Sorry I did not understand \'%s\'.', session.message.text);
    });
bot.dialog('/', intents);
