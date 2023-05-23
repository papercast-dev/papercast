from fastapi import FastAPI, Body
from typing import Dict, Any
from papercast.pipelines import Pipeline
from fastapi import HTTPException, APIRouter
import uvicorn
import asyncio

class Server:
    def __init__(self, pipelines: Dict[str, Pipeline]):
        self._pipelines = pipelines
        self._pipeline_tasks = []

        self.router = APIRouter()
        self.router.add_api_route("/", self._root)
        self.router.add_api_route("/add", self._add, methods=["POST"])
        self.router.add_api_route("/pipelines", self.serialize_pipelines)

        self.app = FastAPI()
        self.app.include_router(self.router)
        self.app.add_event_handler("startup", self.run_pipelines)
        self.app.add_event_handler("shutdown", self._cancel_pipeline_tasks)

    def _root(self):
        return {"message": "Papercast Server"}

    def _get_pipeline(self, pipeline: str):
        if pipeline not in self._pipelines.keys():
            raise HTTPException(status_code=404, detail="Pipeline not found")
        return self._pipelines[pipeline]

    def _add(
        self,
        data: Dict[Any, Any] = Body(...),
    ):

        if "pipeline" in data:
            pipeline = self._get_pipeline(data["pipeline"])  # type: Pipeline
        elif "default" in self._pipelines.keys():
            pipeline = self._get_pipeline("default")
        else:
            return {"message": "Pipeline not specified and no default pipeline found"}
        pipeline.run(**data)

        return {"message": f"Document(s) added to pipeline {pipeline.name}"}

    def serialize_pipelines(self):
        def serialize_pipeline(pipeline: Pipeline):
            return {
                "subscribers": [extractor.asdict() for extractor in pipeline.subscribers],
                "processors": [narrator.asdict() for narrator in pipeline.processors],
            }

        return {
            "pipelines": {
                k: serialize_pipeline(p) for k, p in self._pipelines.items()
            }
        }

    async def _cancel_pipeline_tasks(self):
        for task in self._pipeline_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def run_pipelines(self):
        print("Running pipelines")
        for pipeline in self._pipelines.values():
            task = asyncio.create_task(pipeline._run_in_server())
            self._pipeline_tasks.append(task)
    
    def run(self, host: str = "", port: int = 8000):
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="debug",
            lifespan="on",
        )
        