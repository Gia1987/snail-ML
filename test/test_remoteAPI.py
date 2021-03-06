import path_helper_test_main
from remoteAPI import *


def test_index_route_initializes_photo_loop_and_asks_for_photo_path(mocker):
    tester = app.test_client()
    mocker.patch.object(controller, 'create_temp_photo')
    mocker.patch.object(controller, 'get_photoname')
    response = tester.get('/', content_type='html/text')
    assert (response.status_code) == 200
    assert (controller.create_temp_photo.called)
    assert (controller.get_photoname.called)

def test_FEATURE_index_route_captures_and_renders_photo(mocker):
    tester = app.test_client()
    response = tester.get('/', content_type='html/text')
    assert (response.status_code) == 200
    assert('<img src=' in response.data.decode("utf8"))

def test_forward_route_calls_up_function_and_redirects_to_index(mocker):
    tester = app.test_client()
    mocker.patch.object(controller, 'up')
    mocker.patch.object(controller, 'create_temp_photo')
    mocker.patch.object(controller, 'get_photoname')
    response = tester.get('/forward', content_type='html/text', follow_redirects=True)
    assert (response.status_code) == 200
    assert (controller.up.called)
    assert (controller.create_temp_photo.called)
    assert (controller.get_photoname.called)

def test_pivot_left_route_calls_pivot_left_function_and_redirects_to_index(mocker):
    tester = app.test_client()
    mocker.patch.object(controller, 'piv_left')
    mocker.patch.object(controller, 'create_temp_photo')
    mocker.patch.object(controller, 'get_photoname')
    response = tester.get('/piv_left', content_type='html/text', follow_redirects=True)
    assert (response.status_code) == 200
    assert (controller.piv_left.called)
    assert (controller.create_temp_photo.called)
    assert (controller.get_photoname.called)

def test_pivot_right_route_calls_pivot_right_function_and_redirects_to_index(mocker):
    tester = app.test_client()
    mocker.patch.object(controller, 'piv_right')
    mocker.patch.object(controller, 'create_temp_photo')
    mocker.patch.object(controller, 'get_photoname')
    response = tester.get('/piv_right', content_type='html/text', follow_redirects=True)
    assert (response.status_code) == 200
    assert (controller.piv_right.called)
    assert (controller.create_temp_photo.called)
    assert (controller.get_photoname.called)

def test_ai_move_calls_get_image_path(mocker):
    tester = app.test_client()
    mocker.patch.object(controller, 'get_img_path')
    mocker.patch.object(controller, 'get_server_move')
    response = tester.get('/ai_move?host_url=test', content_type='html/text')
    assert (controller.get_img_path.called)

def test_ai_move_calls_get_server_move_with_passed_in_url_and_image_path(mocker, monkeypatch):
    tester = app.test_client()
    monkeypatch.setattr(controller,'get_img_path', lambda: 'img_path_test')
    mocker.patch.object(controller, 'get_server_move')
    response = tester.get('/ai_move?host_url=test', content_type='html/text')
    controller.get_server_move.assert_called_with('img_path_test','test')

def test_ai_move_applies_forward_move(mocker, monkeypatch):
    tester = app.test_client()
    mocker.patch.object(controller, 'get_img_path')
    monkeypatch.setattr(controller,'get_server_move', lambda x, y: 'forward')
    mocker.patch.object(controller, 'up')
    response = tester.get('/ai_move?host_url=test', content_type='html/text')
    assert (controller.up.called)

def test_ai_move_applies_pivot_left_move(mocker, monkeypatch):
    tester = app.test_client()
    mocker.patch.object(controller, 'create_temp_photo')
    mocker.patch.object(controller, 'get_img_path')
    monkeypatch.setattr(controller,'get_server_move', lambda x, y: 'pivot left')
    mocker.patch.object(controller, 'piv_left')
    response = tester.get('/ai_move?host_url=test', content_type='html/text')
    assert (controller.piv_left.called)

def test_ai_move_applies_pivot_right_move(mocker, monkeypatch):
    tester = app.test_client()
    mocker.patch.object(controller, 'get_img_path')
    monkeypatch.setattr(controller,'get_server_move', lambda x, y: 'pivot right')
    mocker.patch.object(controller, 'piv_right')
    response = tester.get('/ai_move?host_url=test', content_type='html/text')
    assert (controller.piv_right.called)
