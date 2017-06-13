var express = require('express');
var graphqlHTTP = require('express-graphql');
var { buildSchema } = require('graphql');

// Construct a schema, using GraphQL schema language
var schema = buildSchema(`

type Question{
  id: Int!
  text: String!
  answer: [Answer]
}

type User{
  id: Int!
  name: String
  answers: [Answer]
}

type Answer{
  id: Int!
  text: String!
  question: Question!
  user: User!
}

type Query{
  hello(name: String): String
  getUser(id: Int!): User
  getQuestion(id: Int!): Question
  getAnswer(id: Int!): Answer
}
`);
// The root provides a resolver function for each API endpoint

var question = [[0, "What is your name?", [0]]];
var user = [[0, "Joe", [0]],[1]]
var answer = [[0,"Joe",0, 0]]

var myUsers;
var myQuestions;
var myAnswers;
myUsers = function(args){
    return {
      "id": user[args.id][0],
      "name": user[args.id][1],

    }
}
myQuestions = function(args){ 
  return {
    "id": question[args.id][0],
    "text": question[args.id][1]
  }
}
myAnswers = function(args){
  return{
    "id": answer[args.id][0],
    "text": answer[args.id][1],
    "question": myQuestions({"id":answer[args.id][2]}),
    "user": myUsers({"id": answer[args.id][3]})
  }
}

var root = {
  hello: (args) => {
    return 'Hello '+args.name;
  },
  getUser: (args) => {
    return myUsers(args)
  },
  getQuestion:(args) =>{
    return myQuestions(args)
  },
  getAnswer: (args) =>{
    return myAnswers(args)
  },
};

var app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true,
}));
app.listen(4000);
console.log('Running a GraphQL API server at localhost:4000/graphql');
