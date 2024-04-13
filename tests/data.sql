INSERT INTO user (username, password)
VALUES
    ('test', 'test'),
    ('tonto', 'scrypt:32768:8:1$RRGc8bsAHWatCxJE$15f157e6ba4a8d184a6674f6eb730b802dcc381cc7b84adc11799692e505944439a10' ||
              '9a0253b073ef5a373c7fb312b53387ddbe3e1debf65fe6d55e6a380aab7');


INSERT INTO ChatResponses (user_id, input_prompt, response_text, model_used, temperature, max_tokens)
VALUES
    ('1', 'What is a good variable name for my gpa?', 'GPA dummy!', 'gpt-3.5-turbo', 0.3, 1000),
    ('2', 'What is the main advantages to using a set over a tuple?', 'You are going to have to look that one up champ!',
     'gpt-4.0-turbo', 0.001, 1500);


