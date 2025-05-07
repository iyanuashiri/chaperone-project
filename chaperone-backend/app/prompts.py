import asyncio

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.json import JsonOutputParser
from decouple import config
from langchain_google_genai import ChatGoogleGenerativeAI

from .schemas import AssociationSchema 


async def generate_associations(vocabulary, number_of_options):
    generated_associations_output_parser = JsonOutputParser(pydantic_object=AssociationSchema)
    generated_associations_format_instructions = generated_associations_output_parser.get_format_instructions()
    generate_associations_template = """

        This is an association game. Generate a dictionary where each key is an option word and its value is the meaning of that word.
        The game is for the user to associate similar words with the given vocabulary. The main vocabulary must have correct associations.
        Generate {number_of_options} options based on the vocabulary.
        
        For the correct option:
        - The key (word) should be in UPPERCASE
        - The value should be its meaning/definition
        - It should be a synonym of the vocabulary
        
        For the incorrect options:
        - The keys (words) should be in lowercase
        - The values should be their meanings/definitions
        - They should NOT be synonyms of the vocabulary
                    
        The vocabulary is {vocabulary} 
        The number_of_options is: {number_of_options}  

        Format instructions: {format_instructions}
        """
    generate_associations_prompt = PromptTemplate(
        template=generate_associations_template,
        input_variables=["vocabulary", "number_of_options"],
        partial_variables={"format_instructions": generated_associations_format_instructions})

    llm = ChatGoogleGenerativeAI(google_api_key=config("GEMINI_API_KEY"), temperature=0.0, model='gemini-2.5-flash-preview-04-17')

    generated_associations = generate_associations_prompt | llm | generated_associations_output_parser

    tasks = [
        generated_associations.ainvoke({"vocabulary": vocabulary,
                                     "number_of_options": number_of_options,
                                     })
    ]
    list_of_tasks = await asyncio.gather(*tasks)

    # result = generated_questions.invoke({"number_of_questions": number_of_questions,
    #                                      "number_of_options": number_of_options,
    #                                      'text': text})
    
    return list_of_tasks