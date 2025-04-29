import asyncio

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers.json import JSONOutputParser
from decouple import config
from langchain_google_genai import ChatGoogleGenerativeAI

from .schemas import QuizSchema 


async def generate_associations(vocabulary, number_of_options):
    generated_associations_output_parser = JSONOutputParser(pydantic_object=QuizSchema)
    generated_associations_format_instructions = generated_associations_output_parser.get_format_instructions()
    generate_associations_template = """

        This is an association game. The game is for the user to associate similar words. The main vocabulary must associate the correct options. The game is based on a vocabulary. There are different options. 
        Some of the options are correct while the others are incorrect. Generate {number_of_options} options. 
        The options should be based on the vocabulary. The correct option should be in UPPERCASE. The correct options should be synonyms of the vocabulary.     
        The remaining options should be in lowercases. The remaining options should be words that are not synonyms of the vocabulary.   
                    
        The vocabulary is {vocabulary} 
        The number_of_options is: {number_of_options}  

        Format instructions: {format_instructions}
        """
    generate_associations_prompt = PromptTemplate(
        template=generate_associations_template,
        input_variables=["vocabulary", "number_of_options"],
        partial_variables={"format_instructions": generated_associations_format_instructions})

    llm = ChatGoogleGenerativeAI(google_api_key=config("GEMINI_API_KEY"), temperature=0.0, model='gemini-1.5-flash')

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