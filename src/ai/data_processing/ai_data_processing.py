from sklearn.preprocessing import MinMaxScaler, StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import math
from src.modules.data_handlers.ai_models_handle import save_ai, load_latest_ai
from src.modules.data_handlers.ai_data_handle import read_data_from_file, write_other_data_to_file
from src.modules.data_handlers.parameters import *


def normalize_data_min_max(data):
    """
    Normalizes the data using the MinMaxScaler, between 0 and 1
    """
    scaler = MinMaxScaler()
    return scaler.fit_transform(data)


def normalize_data_z_score(data):
    """
    Normalizes the data using the StandardScaler, transforming to mean=0 and std=1
    """
    scaler = StandardScaler()
    return scaler.fit_transform(data)


def preprocess_data(data_type: CollectedDataType) -> (list[list], list):
    """
    Returns an array with sensor data + other metadata and a tensor with only sensor data

    :param data_type: the type of data to be processed
    :return: a list with all the data and a tensor with only the sensor data
    """

    json_data = read_data_from_file(data_type)
    all_sensor_data = [[item[DATA_SENSORS_FIELD], item[DATA_PARAMS_FIELD]["i"], item[DATA_PARAMS_FIELD]["j"]] for item
                       in json_data]

    sensor_data = [item[DATA_SENSORS_FIELD] for item in json_data]
    sensor_data = normalize_data_min_max(np.array(sensor_data))
    sensor_data = torch.tensor(sensor_data, dtype=torch.float32)
    return all_sensor_data, sensor_data


def process_adjacency_properties(all_sensor_data, indices_properties):
    """

    """
    # if indexes are adjacent in the matrix, they are paired
    for i in range(len(all_sensor_data)):
        for j in range(i + 1, len(all_sensor_data)):
            i_x, i_y = all_sensor_data[i][1], all_sensor_data[i][2]
            j_x, j_y = all_sensor_data[j][1], all_sensor_data[j][2]
            indices_properties.append((i, j, abs(i_x - j_x) + abs(i_y - j_y)))

    return indices_properties
