__pragma__ ('alias', 'S', '$')


class Forest:
    async def __init__(self, callback=None, page=1):

        # self.trees = localStorage.getItem('trees')
        # if self.trees is None

        self.total = 'loading...'
        self.callback = callback
        self.page = page
        self.total_pages = 1

        await self.update()

    async def update(self):
        response = await window.requests.js_get('trees',
                                                {'params': {
                                                 'results_per_page': 12,
                                                 'page': self.page}}
                                                )

        self.trees = response.data.objects
        self.total = response.data.num_results
        self.total_pages = response.data.total_pages

        self.response = response
        if self.callback:
            self.callback()

    def prevPage(self):
        if self.page > 1:
            self.page = int(self.page) - 1
            self.update()

    def nextPage(self):
        if self.page < self.total_pages:
            self.page = int(self.page) + 1
            self.update()


module.exports = Forest
