from fastapi import FastAPI, Body
from typing import Optional, Dict, Any
from papercast.pipelines import Pipeline
from fastapi import HTTPException, APIRouter
import uvicorn


class Server:
    def __init__(self, pipelines: Dict[str, Pipeline]):
        self._pipelines: Dict[str, Pipeline] = pipelines
        self._init_app()

    def _init_app(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self._root)
        self.router.add_api_route("/add", self._add, methods=["POST"])
        self.router.add_api_route("/pipelines", self.__pipelines)
        self.app = FastAPI()
        self.app.include_router(self.router)

    def _root(self):
        return {"message": "Papercast Server"}

    def _add(
        self,
        data: Dict[Any, Any] = Body(...),
    ):
        pipeline = self.get_pipeline(data["pipeline"])  # type: Pipeline
        pipeline.run(**data)

        return {"message": f"Documents added to pipeline {pipeline.name}"}

    def get_pipeline(self, pipeline: str):
        if pipeline not in self._pipelines.keys():
            raise HTTPException(status_code=404, detail="Pipeline not found")
        return self._pipelines[pipeline]

    def __pipelines(self):
        return {
            "pipelines": {
                k: self.serialize_pipeline(p) for k, p in self._pipelines.items()
            }
        }

    def serialize_pipeline(self, pipeline: Pipeline):
        return {
            "collectors": [collector.asdict() for collector in pipeline.collectors],
            "narrators": [narrator.asdict() for narrator in pipeline.narrators],
            "extractors": [extractor.asdict() for extractor in pipeline.extractors],
            "filters": [filter.asdict() for filter in pipeline.filters],
            "publishers": [publisher.asdict() for publisher in pipeline.publishers],
        }

    def run(
        self,
        host: str = "",
        port: int = 8000,
    ):
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="debug",
        )
