from models import ChatGPT as Model

agent = Model()
while True:
  user_input = input("User:")
  if not user_input:
    break
  completion = agent.get_completion(user_input)
  print(f"Assistant:{completion}")