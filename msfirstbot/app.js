var builder = require('botbuilder');

var connector = new builder.ConsoleConnector().listen();
var bot = new builder.UniversalBot(connector);
var model = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/0461769f-c4f5-4ed2-9136-c10d96b45fee?subscription-key=96d95462721b41629fed437056c857c6&verbose=true&q=';
var recognizer = new builder.LuisRecognizer(model);
var intents = new builder.IntentDialog({recognizers : [recognizer]});
bot.dialog('/', intents);

intents.matches("getWeather", [
    function(session, args, next){
      var where = builder.EntityRecognizer.findEntity(args.entities, "where");
			var when = builder.EntityRecognizer.findEntity(args.entities, "when");
      if(!where){
        session.send("Where abouts?");
      }else if (!when){
				session.send("I'll find the weather for now, soon and tomorrow. If your interested in a particular date or time this week let me know!");
			}else if(where && when){
        session.send(`The user wants to know the weather in ${where.entity} for ${when.entity}. `);
      }else if(where){
        session.send(`The user wants to know the weather in ${where.entity}.`);
      }else if (when){
        session.send(`The user wants to know the weather for ${when.entity}.`);
      }else{

      }
  }])

intents.matches("None", [
    function(session, args, next){
      session.send("Hello");
    }])
    .onDefault((session) => {
      session.send('Sorry I did not understand \'%s\'.', session.message.text);
    });
