from workers import WorkerEntrypoint, Response
from urllib.parse import urlparse


class Default(WorkerEntrypoint):

    async def fetch(self, request):
        url = urlparse(request.url)

        # Test backend
        if url.path == "/api/test":
            return Response.json(
                {"status": True, "message": "Cloudflare Python Worker is working!"}
            )

        # Submit report endpoint
        if url.path == "/submit-report" and request.method == "POST":
            return Response.json(
                {"status": True, "message": "Report received successfully!"}
            )

        # Serve index.html and other static assets
        return await self.env.ASSETS.fetch(request)
