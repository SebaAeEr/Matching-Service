# Matching Service

## The Matching server ##
* If you want to use ML algorithms, you need an openai-key. You can copy the key at file chatgpt.py into the variable `chat_gpt_key` or use environment variables `CHAT_GPT_KEY`.
* Start the Matching server with the command inside the project directory: `uvicorn main_matcher:matcher --host 0.0.0.0 --port 27182`

## The Correlator ##
* This service works with every Correlator this is just an example Correlator with minimal functionality.
* This Correlator connects to RocketChat. So you need a RocketChat account!
* Put in your credentials in listener.py at line 21 and 22 for the variables `usr_name` and `password`. Or use environment variables `RC_NAME` and `RC_PASSWORD`.
* If you are not on the 'chat.tum.de' server you also have to change the `server_url` variable.
* Start the Correlator server with the command inside the project directory: `uvicorn main:correlator --host 0.0.0.0 --port 8000`
* You can now add rules with the online documentation: http://localhost:8000/ad_doc#/default/add_rule_add_rule_post

## Cpee Instance ##
* create a new Cpee instance and load the testset bpmn.xml.
* If you use your own Correlator you have to modify the endpoints `messages`, `rules` and `add_matching`. You can look into the example Correlator in main.py how those endpoints are implemented.
* If the Correlator is already running you can start running the Cpee Instance.
