1) All lambda functions must be called as: "worker-lambda, request-lambda, bonus-lambda"
2) All buttons must have action_id as: "worker_create_something, request_edit_2, bonus_start_menu" (name of lambda not plural, but single)
3) After clicking a button, it returns data like this:
    {
        "response_url": body['response_url'],
        "trigger_id": body['trigger_id'],
        "user": body['user'],
        "action_id": action_id #  important, not action, but action_id already
    }
   
4) After submitting a modal it returns data like this:
    {
        "body": body, #  there are all input fields there, we will take data from it in business logic lambda
        "action_id": callback_id #  important, not action_id, but callback_id with key action_id, it is necessary for catching this result in lambda with business logic
    }
   
5) In file slack_block_kits.py there are names for action_id of buttons, which appear at start, You can rename it as You want, but I think it will be better, when we have the same structure of these action_id
6) To return to the start_menu with three buttons: workers, requests, bonuses, the action_id of your button have to start with "start"
7) Now there is my lambda ARN there, later there will be ARN from our main lambda functions
