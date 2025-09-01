from fastapi import APIRouter, HTTPException, Request

from schemas.graphql_schema import GraphQLRequest
from services.graphql_service import GraphQLService

def get_graphql_router(graphql_service: GraphQLService) -> APIRouter:
    router = APIRouter(prefix="/graphql", tags=["graphql"])

    @router.post("/")
    async def graphql_endpoint(request: GraphQLRequest):
        try:
            return graphql_service.execute_query(request.query, request.variables)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Failed to process GraphQL request: {ex}")

    return router