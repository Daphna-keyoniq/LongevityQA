from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os

## internal imports
from medai_flow.tools.consts.ontology import (
    KeyoniqQoreBiomarkers,
    Rels,
)
from medai_flow.tools.fuzzy_matching.ontology_names import convert_to_graph_name
from medai_flow.utils.kg import KnowledgeGraphRepository
from medai_flow.config import Config

config = Config().load_configuration()


class GetRelatedRisksInput(BaseModel):
    """Input schema for GetRelatedRisks."""

    biomarker_name: str = Field(
        ...,
        description="the biomarker name",
    )
    biomarker_value: str = Field(
        ...,
        description="whether the biomarker is high or low. please specify either 'high' 'low', 'normal' or 'unknown'",
    )


class GetRelatedRisks(BaseTool):
    name: str = "Get the risks related to this marker value"
    description: str = "You can use this tool when you want to find the risks related to a certain marker value"

    args_schema: type[GetRelatedRisksInput] = GetRelatedRisksInput

    file_path: str = os.path.join(
        config.paths.full_knowledge_dir,
        "knowledge_graph/diagnosis_kg.csv",
    )
    graph_repo: type[KnowledgeGraphRepository] = KnowledgeGraphRepository(file_path)

    def _run(
        self,
        biomarker_name: str,
        biomarker_value: str,
    ) -> list:
        biomarker = convert_to_graph_name(biomarker_name, biomarker_value)
        biomarker = KeyoniqQoreBiomarkers.map_graph_name(biomarker)
        df = self.graph_repo.get_graph()
        pos_associated_risks = df[
            [
                self.graph_repo.obj_col,
                self.graph_repo.strength_col,
                self.graph_repo.origin_col,
            ]
        ][
            (df[self.graph_repo.subj_col] == biomarker)
            & (df[self.graph_repo.rel_col] == Rels.PositivelyCorrelate)
            | (df[self.graph_repo.subj_col] == biomarker)
            & (df[self.graph_repo.rel_col] == Rels.Predict)
            | (df[self.graph_repo.subj_col] == biomarker)
            & (df[self.graph_repo.rel_col] == Rels.Cause)
        ]
        pos_associated_risks = pos_associated_risks.rename(
            columns={self.graph_repo.obj_col: "disease_risk"}
        )

        grouped_pos_associated_risks = pos_associated_risks.groupby(
            "disease_risk", as_index=False
        ).agg(
            {
                self.graph_repo.strength_col: lambda x: sum(x),
                self.graph_repo.origin_col: lambda x: ",".join(x),
            },
        )

        return grouped_pos_associated_risks.to_json(orient="records")
