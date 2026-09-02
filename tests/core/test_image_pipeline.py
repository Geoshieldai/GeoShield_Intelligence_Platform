from core.image_processing.processing_pipeline import ProcessingPipeline


def test_pipeline_creation():

    pipeline = ProcessingPipeline()

    assert pipeline is not None