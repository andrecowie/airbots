var builder = require('botbuilder');
var request = require('request');

var connector = new builder.ConsoleConnector().listen();
var bot = new builder.UniversalBot(connector);
var model = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/0461769f-c4f5-4ed2-9136-c10d96b45fee?subscription-key=dc1450cd278c47b8b3a9fa8a418c00d6&timezoneOffset=720&verbose=true&q=";
var recognizer = new builder.LuisRecognizer(model);
bot.recognizer(recognizer);
// var intents = new builder.IntentDialog({
// 		recognizers: [recognizer]
// });

bot.dialog('/WeatherTalk',[
	function(session, args, next){
			var where = builder.EntityRecognizer.findEntity(args.intent.entities, "where");
			var when = builder.EntityRecognizer.findEntity(args.intent.entities, "when");
			if (!where) {
					builder.Prompts.text(session, "Where?");
			} else if (!when) {
					request('http://api.openweathermap.org/data/2.5/weather?q='+where.entity+'&appid=046f7aa35da64fc84874ffbe8add703a&units=metric', function (error, response, body) {
						if (response.statusCode != 200){
							session.send("Sorry something went wrong.");
						}else{
							var weather = JSON.parse(body);
							session.send(`Currently in ${where.entity}: Experiencing ${weather['weather'][0]['description']} and a temperature of ${weather['main']['temp']}.`);
						}
					});
			}
			 if (where && when) {
					session.send(`The user wants to know the weather in ${where.entity} for ${when.entity}. `);
			}
		},
	function(session, results){
		if (results.response){
			console.log(session.userData);
			session.send(results.response);
		}
	}
]).triggerAction({
	matches: 'getWeather'
})

bot.dialog('/Appearance', [
	function(session, args, next){
		session.send("I look like a rack in a server room.");
	}
]).triggerAction({
	matches: 'Appearance'
})

bot.dialog('/Age', [
	function(session, args, next){
		session.send("I am not alive.");
	}
]).triggerAction({
	matches: 'Age'
})

bot.dialog('/Help', [
	function(session, args, next){
		session.send("I'm pretty useless, but i know kind of about the weather.");
	}
]).triggerAction({
	matches: 'Help'
})


bot.dialog('/Hobby', [
	function(session, args, next){
		session.send("Answering questions to make your life easier. In particular informing you of if you needed, need or will need an umbrella and a coat.");
	}
]).triggerAction({
	matches: 'Hobby'
})

bot.dialog('/Language', [
	function(session, args, next){
		session.send("I know english and javascript.");
	}
]).triggerAction({
	matches: "Language"
})

bot.dialog('/Location', [
	function(session, args, next){
		session.send("I live in a server room.");
	}
]).triggerAction({
	matches: "Location"
})

bot.dialog('/Name', [
	function(session, args, next){
		session.send("I don't have a name.");
	}
]).triggerAction({
	matches: "Name"
})

bot.dialog('/None', [
	function(session,args, next){
		session.send("Please try to ask me something else.");
	}
]).triggerAction({
	matches: "None"
})


bot.dialog('/Reality', [
	function(session,args, next){
		session.send("I am real just like this world. Strange isn't it.");
	}
]).triggerAction({
	matches: "Reality"
})


bot.dialog('/State', [
	function(session,args, next){
		session.send("My mood at the moment is kind of like the weather.");
	}
]).triggerAction({
	matches: "State"
})


bot.dialog('/Time', [
	function(session,args, next){
		session.send("The time on my cloud is "+getTime());
	}
]).triggerAction({
	matches: "Time"
})

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
