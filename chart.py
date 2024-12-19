import os
os.environ["OPENAI_API_KEY"] = "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"

from codeinterpreterapi import CodeInterpreterSession
async def safe_generate_response(session, prompt):
    try:
        response = await session.generate_response(prompt)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
async def main():
# create a session
    session = CodeInterpreterSession(model="gpt-3.5-turbo")
    await session.astart()

# generate a response based on user input
    response = await session.generate_response(
    "scivi una breve poesia alla mamma")

# output the response (text + image)
    print("AI: ", response.content)
    #for file in response.files:
     #file.show_image()

# terminate the session
    await session.astop()

if __name__ == "__main__":
    import asyncio
# run the async function
    asyncio.run(main())