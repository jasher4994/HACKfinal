import os
from flask import Flask, render_template, request
import vertexai
from vertexai.language_models import TextGenerationModel 
from vertexai.language_models import CodeGenerationModel

#must replace hashtags with project names
#To run >>>>>
# flask --app CodeReviewer run --debug -p 8080

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    # a simple page that says hello
    @app.route('/', methods=['POST', 'GET'])
    def hello():
        if request.method == 'POST':
            print('hello')
            user_input = request.form['user_input']
            prompt1 = "write me a function that: " + user_input + ". Include type hinting, and a google style docstring with '🔥🔥🔥created to LBG standards🔥🔥🔥' at the end of the docstring. Use the most efficient coding method based on minimum processing time."


            vertexai.init(project="###########", location="us-central1")
            parameters = {
                "max_output_tokens": 1024,
                "temperature": 0.9
            }
            model = CodeGenerationModel.from_pretrained("code-bison-32k@002")
            model = model.get_tuned_model("#############")
            response = model.predict(
                prompt1,
                **parameters
            )
            response = response.text
            response_new = response[10:-3]

            prompt2 = 'Explain this code to someone who does not use python, suggesting further reading on any packages or functions used and describing why these were used. In big O notation what is the code complexity of this function:' + response_new
            analysis = model.predict(
                prompt2,
                **parameters
            )
            analysis = analysis.text
            
            prompt3 = 'Write a unit test using pytest for this function. Ensure edge cases and boundaries are tested. Include tests using pytest.raises. Put all tests into one function with a note describing each test and a google standards docstring. Make sure "🔥🔥🔥Created to LBG standards🔥🔥🔥" is at the end of the docstring.' + response
            unit_test = model.predict(
                prompt3,
                **parameters
            )
            unit_test = unit_test.text[10:-3]



            return render_template('demo.html', response = response_new, analysis = analysis, unit_test = unit_test, post_success=True)
        else:
            return render_template('demo.html')

    return app
