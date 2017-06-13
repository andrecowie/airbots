import {
  makeExecutableSchema,
  addResolveFunctionsToSchema,
} from 'graphql-tools';

const typeDefs = `
# A question and its answers.
type Question{
  id: Int!
  # The text the user was shown which is the main question.
  text: String!
  # All or a particular Answer for a Question if the Id Of the answer isn't for the particular question null will be returned.
  answers(id: Int): [Answer] 
}

# A user with their answers.
type User{
  id: Int!
  # The users name.
  name: String
  # The users answers to questions.
  answers(id: Int): [Answer]
}

# A user's answer to a question.
type Answer{
  id: Int!
  text: String!
  users(id: Int): User!
  question(id: Int): Question!
}


# The root queries i would recommend only using one parameter.
type Query{
  users(id: Int, ids:[Int], name: String): [User]
  questions(id: Int, ids: [Int], text: String): [Question]
  answers(id: Int, ids:[Int], text: String): [Answer]
}
`;

var question = [{'id': 0,'text': "What is your name?"},{'id': 1, 'text': "What do you do?"}];
var user = [{'id': 0, 'name': "Joe"},{'id': 1, 'name': undefined}, {'id': 2, 'name': 'Sam'}];
var answer = [{'id':0, 'text':"Joe"},{'id': 1, 'text': 'I study'}, {'id': 2, 'text': 'Sam'}, {'id': 3, 'text': 'I work'}];
var whoansweredwhat = [{'userid':0, 'questionid': 0}, {'userid': 1, 'questionid': 1}, {'userid': 2, 'questionid': 0}, {'userid': 2,'questionid': 1}]

const resolverMap = {
  Query: {
    users(obj, { id, ids, name }, context){
        if(ids){
            var theusers = [];
            ids.forEach(function(x){
                theusers.push(user[x]);
            });
            return theusers;
        }else if(id){
            return [user[ids]];
        }else if(name){
        
        }
        return user;
    },
    questions(obj, { id, ids, text },context){
        if(ids){
            var thequestions =[];
            ids.forEach(function(x){
                thequestions.push(question[x]);
            });
            return thequestion;
        }else if(id){
            return question[id];
        }else if(text{
        }
        return question;
    },
    answers(obj, { id, ids, text }, context){
        if(ids){
            var theanswers = [];
            ids.forEach(function(x){
                theanswers.push(answer[x])
            });
            return theanswers;
        }else if(id){
            return answer[id];
        }else if(text){

        }
        return answer;
    },
  },
  User: {
    answers(obj, { id }, context){
        var useranswer = [];
        whoansweredwhat.forEach(function(x, index){
            if (x['userid'] == obj.id){
                useranswer.push(answer[index]);
            }
        });
        return useranswer;
    },
  },
  Answer: {
    users(obj, { id }, context){
        return user[whoansweredwhat[obj.id]['userid']];
    },
    question(obj, { ids }, context){
        return question[whoansweredwhat[obj.id]['questionid']];
    },
  },
  Question: {
      answers(obj, { id }, context){
          questionsanswers = [];
          whoansweredwhat.forEach(function(x, index){
            if (x['questionid'] == obj.id){
                questionanswers.push(answer[index]);
            }
          });
          return questionanswers;
      }
  }
};


const schema = makeExecutableSchema({ typeDefs });
addResolveFunctionsToSchema(schema, resolverMap);
export { schema };
