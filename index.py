import modules.objectLib as ol
from classes.Priority import Priority
from classes.EditType import EditType
from web.webHost import app
import asyncio


async def runApp():
    app.run()
    
if __name__ == "__main__":
    asyncio.run(runApp())