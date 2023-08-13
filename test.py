# from LLM import hf_ops
# print(hf_ops.get_answer("What is container?")) # TODO: REMOVE THIS 

from Other import error_resolution

a = error_resolution.common_errors_resolution("I am getting API Rate Limit Exceeded")
print(a)