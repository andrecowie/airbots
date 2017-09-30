from flask import Flask, render_template
from flask_graphql import GraphQLView

from schema import schema

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run()
