import json

from hcaptcha_challenger.models import ImageAreaSelectChallenge, ImageDragDropChallenge

from extensions.llm_adapter import (
    _coerce_payload_for_schema,
    _extract_json_payload,
    _normalize_glm_payload,
)


def test_area_select_box_answer_is_converted_to_click_points():
    text = '{"answer":[[781,525,889,624],[1031,525,1139,624]]}'

    payload = _coerce_payload_for_schema(
        _normalize_glm_payload(_extract_json_payload(text)), ImageAreaSelectChallenge, text
    )
    challenge = ImageAreaSelectChallenge(**payload)

    assert challenge.points[0].model_dump() == {"x": 835, "y": 574}
    assert challenge.points[1].model_dump() == {"x": 1085, "y": 574}


def test_area_select_dict_boxes_are_converted_to_click_points():
    payload = {
        "answer": [
            {"x_min": 10, "y_min": 20, "x_max": 30, "y_max": 60},
            {"x_min": 101, "y_min": 201, "x_max": 200, "y_max": 300},
        ]
    }
    text = json.dumps(payload)

    coerced = _coerce_payload_for_schema(
        _normalize_glm_payload(payload), ImageAreaSelectChallenge, text
    )
    challenge = ImageAreaSelectChallenge(**coerced)

    assert [point.model_dump() for point in challenge.points] == [
        {"x": 20, "y": 40},
        {"x": 150, "y": 250},
    ]


def test_drag_answer_source_target_strings_are_converted_to_paths():
    payload = {"answer": [{"source": "(1139, 559)", "target": "(960, 559)"}]}
    text = json.dumps(payload)

    coerced = _coerce_payload_for_schema(
        _normalize_glm_payload(payload), ImageDragDropChallenge, text
    )
    challenge = ImageDragDropChallenge(**coerced)

    assert challenge.paths[0].start_point.model_dump() == {"x": 1139, "y": 559}
    assert challenge.paths[0].end_point.model_dump() == {"x": 960, "y": 559}


def test_drag_moves_flat_coordinates_are_converted_to_paths():
    payload = {"moves": [{"start_x": 1156, "start_y": 575, "end_x": 1013, "end_y": 670}]}
    text = json.dumps(payload)

    coerced = _coerce_payload_for_schema(
        _normalize_glm_payload(payload), ImageDragDropChallenge, text
    )
    challenge = ImageDragDropChallenge(**coerced)

    assert challenge.paths[0].start_point.model_dump() == {"x": 1156, "y": 575}
    assert challenge.paths[0].end_point.model_dump() == {"x": 1013, "y": 670}
