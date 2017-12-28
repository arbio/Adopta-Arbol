
class Forest:
    async def __init__(self):
        await self.update()

    async def update(self):
        response = await window.requests.js_get('trees')
        self.trees = response.data.objects


def iLikePython():
    window.forest = Forest()


module.exports = iLikePython
