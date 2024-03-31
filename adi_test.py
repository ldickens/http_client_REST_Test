import adi_core_networking, json
from typing import Callable

class TestMedia():
    test_json: dict | None = None
    with open('json_get_media_test.json') as f:
        test_json = json.load(f)

    def test_show_media_names(self, capsys: Callable):
        assert self.test_json != None
        adi_core_networking.show_media_names(self.test_json['entries'])
        captured = (capsys.readouterr().out).strip().split('\n')
        last_output = captured[-1]
        print(f'last_output: {captured}')
        required_out = 'BW_Mask' 
        assert last_output == required_out

    def test_search_by_name_success_single(self,capsys: Callable):
        search = 'Yamaha Adecia'
        result = adi_core_networking.search_by_name(search, self.test_json['entries'])
        assert type(result) == list
        assert len(result) == 1
        assert result[0]['name'] == 'Yamaha Adecia'
        captured = capsys.readouterr()
        assert captured.out.strip() == 'Found 1 file(s) called: Yamaha Adecia'

    def test_search_by_name_success_multiple(self,capsys: Callable):
        search = 'BW_Mask'
        result = adi_core_networking.search_by_name(search, self.test_json['entries'])
        assert type(result) == list
        assert len(result) == 2
        assert result[0]['name'] == 'BW_Mask'
        captured = capsys.readouterr()
        assert captured.out.strip() == 'Found 2 file(s) called: BW_Mask'
    
    def test_search_by_name_fail(self, capsys: Callable):
        search = 'FAILURE'
        assert adi_core_networking.search_by_name(search, self.test_json['entries']) == None 
        captured = capsys.readouterr()  
        assert captured.out.strip() == 'File not found: FAILURE'

    def test_search_by_id_success(self):
        search = "668b2427-edde-494f-9c78-c7f9fb477cce:3E49D8FA732A94E27ABEEA5724316721"
        result = adi_core_networking.search_by_id(search, self.test_json['entries'])
        assert result['name'] == "9600x1920_Demo_Content_LEFT"

    def test_search_by_id_failure(self):
        search = "sdaojfhasi-edde-494f-9c78-c7f9fb477cce:3E49D8FA732A94E27ABEEA5724316721"
        result = adi_core_networking.search_by_id(search, self.test_json['entries'])
        assert result == None
