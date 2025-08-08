from typing import Any, Dict, Union

import yaml


def load_yaml(yaml_path: Union[str]) -> Dict[str, Any]:
    with open(yaml_path, "r") as f:
        raw = yaml.safe_load(f)
    return raw


def load_environment_graph(raw_data: Dict):
    environment_graph = {}

    for state_str, value in raw_data.items():
        state = int(state_str)  # convert key to int

        # If the value is a list (e.g., [7, 8])
        if isinstance(value, list):
            environment_graph[state] = value

        # If the value is a dict
        elif isinstance(value, dict):
            processed = {}
            for k, v in value.items():
                if isinstance(v, dict) and "next" in v and "prob" in v:
                    # convert to (list, prob) tuple
                    processed[int(k)] = (v["next"], v["prob"])
                else:
                    # keep other keys like "skip"
                    processed[k] = v
            environment_graph[state] = processed

        else:
            raise ValueError(f"Unsupported value format for key {state}: {value}")

    return environment_graph


def load_task_from_yaml(
    yaml_path: Union[str],
) -> Any:
    raw = load_yaml(yaml_path=yaml_path)

    graph = load_environment_graph(raw["graph"])
    meta = {"meta": raw["meta"]}

    return meta, graph
