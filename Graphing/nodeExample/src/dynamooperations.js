import {
    config,
    DynamoDB
} from 'aws-sdk';

config.update({
    region: 'ap-southeast-2'
});


const questionsTable = {
    TableName: 'wtf-questions',
    KeySchema: [
        {
            AttributeName: 'trueid',
            KeyType: 'HASH',
        },
        {
            AttributeName: 'id',
            KeyType: 'RANGE'
        }
    ],
    AttributeDefinitions: [
        {
            AttributeName: 'trueid',
            AttributeType: 'S',
        },
        {
            AttributeName: 'id',
            AttributeType: 'N',
        },
    ],
    ProvisionedThroughput: {
        ReadCapacityUnits: 1,
        WriteCapacityUnits: 1,
    },
}

const usersTable = {
    TableName: 'wtf-users',
    KeySchema: [
        {
            AttributeName: 'trueid',
            KeyType: 'HASH',
        },
        {
            AttributeName: 'id',
            KeyType: 'RANGE'
        }
    ],
    AttributeDefinitions: [
        {
            AttributeName: 'trueid',
            AttributeType: 'S',
        },
        {
            AttributeName: 'id',
            AttributeType: 'N',
        },
    ],
    ProvisionedThroughput: {
        ReadCapacityUnits: 1,
        WriteCapacityUnits: 1,
    },
}
const answersTable = {
    TableName: 'wtf-answers',
    KeySchema: [
        {
            AttributeName: 'trueid',
            KeyType: 'HASH',
        },
        {
            AttributeName: 'id',
            KeyType: 'RANGE'
        }
    ],
    AttributeDefinitions: [
        {
            AttributeName: 'trueid',
            AttributeType: 'S',
        },
        {
            AttributeName: 'id',
            AttributeType: 'N',
        },
    ],
    ProvisionedThroughput: {
        ReadCapacityUnits: 1,
        WriteCapacityUnits: 1,
    },
}


const dynamodb = new DynamoDB();

var checkTablesExist = () => {
    dynamodb.describeTable({TableName: 'wtf-questions',} , function(err, data){
        if (err){
            dynamodb.createTable(questionsTable, function(err, data){
                if (err) console.log(err);
                else console.log(data);
            });
        }
    });
    dynamodb.describeTable({TableName: 'wtf-users',}, function(err, data){
        if(err){
            dynamodb.createTable(usersTable, function(err, data){
                if (err) console.log(err);
                else console.log(data);
            });
        }
    });
    dynamodb.describeTable({TableName: 'wtf-answers',}, function(err, data){
        if(err){
            dynamodb.createTable(answersTable, function(err, data){
                if (err) console.log(err);
                else console.log(data);
            });
        }
    });
};

var newAnswer = (questionid, userid, text) => {

}
var newQuestion = () => {

}
var newUser = () => {

}

export { checkTablesExist };
