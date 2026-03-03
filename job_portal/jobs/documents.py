from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Job


@registry.register_document
class JobDocument(Document):
    """
    Elasticsearch document for Job model.
    This defines how Job is indexed inside Elasticsearch.
    """

    company = fields.ObjectField(properties={
        "name": fields.TextField(),
    })

    class Index:
        name = "jobs"  # index name in Elasticsearch
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "skills",
            "location",
            "salary_min",
            "salary_max",
            "job_type",
            "created_at",
        ]