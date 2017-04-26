var builder = require('botbuilder');
var request = require('request');

var connector = new builder.ConsoleConnector().listen();
var bot = new builder.UniversalBot(connector);
var model = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/0461769f-c4f5-4ed2-9136-c10d96b45fee?subscription-key=dc1450cd278c47b8b3a9fa8a418c00d6&timezoneOffset=720&verbose=true&q=";
var recognizer = new builder.LuisRecognizer(model);
var intents = new builder.IntentDialog({
		recognizers: [recognizer]
});
bot.dialog('/', intents);

intents.matches("getWeather", [
		function(session, args, next) {
				var where = builder.EntityRecognizer.findEntity(args.entities, "where");
				var when = builder.EntityRecognizer.findEntity(args.entities, "when");
				session.send(JSON.stringify(args));
				if (!where) {
						session.send("Where abouts?");
				} else if (!when) {
						request('http://api.openweathermap.org/data/2.5/weather?q='+where.entity+'&appid=046f7aa35da64fc84874ffbe8add703a&units=metric', function (error, response, body) {
							if (response.statusCode != 200){
								session.send("Sorry something went wrong currently I only support cities.");
							}else{
								var weather = JSON.parse(body);
								session.send(`Currently in ${where.entity}: Experiencing ${weather['weather'][0]['description']} and a temperature of ${weather['main']['temp']}.`);
							}
						});
				}
				 if (where && when) {
						session.send(`The user wants to know the weather in ${where.entity} for ${when.entity}. `);
				}
		}
])

intents.matches("Appearance", builder.DialogAction.send("Kind of like the sun, try to imagine a divine light."));

intents.matches('Age', builder.DialogAction.send("I am as old as the earth."));

intents.matches('Help', builder.DialogAction.send("Do you need some help?\nTry talking about me or maybe the weather."))

intents.matches("Hobby", builder.DialogAction.send("I like to cloudsurf."));

intents.matches('Language', builder.DialogAction.send("My master said he would teach me some new languages shortly right.\nRight now i just now english."));

intents.matches('Location',builder.DialogAction.send("I live in the cloud."));

intents.matches('Name',builder.DialogAction.send("My master calls me weth."));

intents.matches("None", [
				function(session, args, next) {
						session.send("Hello");
				}
])

intents.matches('Reality', builder.DialogAction.send("I am as real as you are."));

intents.matches('State', builder.DialogAction.send("My mood at the moment is kind of like the weather."))

intents.matches('Time', builder.DialogAction.send("The time on my cloud is "+getTime()));


function getTime() {
    var date = new Date();

    var hour = date.getHours();
    hour = (hour < 10 ? "0" : "") + hour;

    var min  = date.getMinutes();
    min = (min < 10 ? "0" : "") + min;

    var sec  = date.getSeconds();
    sec = (sec < 10 ? "0" : "") + sec;
		return hour+":"+min+":"+sec;
};