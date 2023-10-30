import os
import replicate
import re
import streamlit as st



def grammar_errors(summary):

  os.environ["REPLICATE_API_TOKEN"] = "r8_KjNJz1w5dROUo3FRE1s6FJakHD3bNJS2kZ9nu"
  pre_prompt1 = "List the grammatical errors in the following paragraph:"

  prompt_input = summary
  # Generate LLM response
  output1 = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                          input={"prompt": f"{pre_prompt1}\n{prompt_input}\nAssistant:",
                                "temperature": 0.1, "top_p": 0.8, "max_length": 1000, "repetition_penalty": 1})

  full_response = ""

  for item in output1:
    full_response += item


  # Define a regular expression pattern to match lines containing errors
  pattern = r'"([^"]+)" should be "([^"]+)"'

  # Use re.findall to extract the error lines
  error_lines = re.findall(pattern, full_response)

  # Create an array to store the extracted errors
  errors = []
  for error in error_lines:
      errors.append(f'"{error[0]}" should be "{error[1]}"')

  st.info(f"There are {len(errors)} grammatical errors in your summary.")
  # Print the list of errors with line numbers
  # for i, error in enumerate(errors):
  #     print(f"{i + 1}. {error}")

  with st.expander("See the grammatical errors"):
     for i, error in enumerate(errors):
        st.write(f"{i + 1}. {error}")


# st.info(f"There are {5} grammatical errors in your summary.")

# error = "Hi"
# with st.expander("See explanation"):
#     for i in range(5):
#         st.write(f"{i + 1}. {error}")


def ideal_summary(prompt,text):
  
  os.environ["REPLICATE_API_TOKEN"] = "r8_KjNJz1w5dROUo3FRE1s6FJakHD3bNJS2kZ9nu"
  summary_prompt = prompt

  text_to_summarize = text
  
  # Generate LLM response
  output1 = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                          input={"prompt": f"{summary_prompt}\n{text_to_summarize}\n",
                                "temperature": 0.1, "top_p": 0.8, "max_length": 25000, "repetition_penalty": 1})

  full_response = ""

  for item in output1:
    full_response += item

  with st.expander("An example summary for reference"):
    st.write(full_response)