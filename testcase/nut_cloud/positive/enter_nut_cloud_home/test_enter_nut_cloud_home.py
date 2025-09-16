import logging

logger = logging.getLogger(__name__)


class TestEnterNutCloudHome:
    
    def test_get_document_name(self, enter_nut_cloud_home):
        document_all_name = enter_nut_cloud_home.get_all_search_document_names()
