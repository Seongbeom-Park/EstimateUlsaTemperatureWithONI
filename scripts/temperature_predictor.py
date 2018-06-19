import tensorflow as tf

import time, datetime
import os.path
import pandas as pd
import numpy as np

FROM_YEAR = 1990 # min: 1981
CUT_YEAR = 2010
LAST_YEAR = 2015 # max: 2017

TRAIN_SIZE = 0
TEST_SIZE = 0

BATCH_SIZE = 1

def load_data(asos_file, oni_file, from_year, cut_year, last_year):
    print "load_data"

    # TIME,TEMPERATURE [degC],PRECIPITATION [mm/6hr],WIND SPEED [m/s],WIND DIRECTION,HUMIDITY [%],SEA-LEVEL PRESSURE [hPa]
    asos = pd.read_csv(asos_file)
    asos['Year']    = asos['TIME']//1000000%10000
    asos['Month']   = asos['TIME']//10000%100
    asos['Day']     = asos['TIME']//100%100
    asos['Time']    = asos['TIME']//1%100

    # Year,ppastMonth,pastMonth,currMonth,ONI
    oni = pd.read_csv(oni_file)

    column_name = ['Year', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'ppM.Temp.', 'pM.Temp.', 'cM.Temp.', 'ONI']

    ppmt = None
    pmt = None
    cmt = None
    dataset_temp = []
    for y in range(from_year-1, last_year+1):
        for m in range(1, 13):
            month = [0 for i in range(1,13)]
            month[m-1] = 1
            ppmt = pmt
            pmt = cmt
            cmt = asos[(asos['Year'] == y) & (asos['Month'] == m)]['TEMPERATURE [degC]'].mean()
            oni_val = oni[(oni['Year'] == y) & (oni['currMonth'] == m)]['ONI'].values[0]
            if (y >= from_year):
                dataset_temp.append(pd.DataFrame([[y, month[0], month[1], month[2], month[3], month[4], month[5], month[6], month[7], month[8], month[9], month[10], month[11], ppmt, pmt, cmt, oni_val]], columns=column_name))
    #dataset = pd.concat(dataset_temp, ignore_index=True)
    dataset = pd.concat(dataset_temp, ignore_index=True).drop(columns=['ONI'])

    train_x = dataset[(dataset['Year'] >= from_year) & (dataset['Year'] < cut_year)]
    test_x = dataset[(dataset['Year'] >= cut_year) & (dataset['Year'] < last_year)]
    
    dataset['nM.Temp.'] = dataset['cM.Temp.'].drop(dataset.index[0]).reset_index(drop=True)
    
    train_y = dataset[(dataset['Year'] >= from_year) & (dataset['Year'] < cut_year)]['nM.Temp.']
    test_y = dataset[(dataset['Year'] >= cut_year) & (dataset['Year'] < last_year)]['nM.Temp.']
   
    return (train_x, train_y, len(train_x), test_x, test_y, len(test_x))

def make_feature_columns(train_x):
    print "make_feature_columns"

    feature_columns = []

    for key in train_x.keys():
        feature_columns.append(tf.feature_column.numeric_column(key=key))

    return feature_columns

def train_input_fn(features, labels, batch_size):
    print "train_input_fn"

    inputs = (dict(features), labels)

    dataset = tf.data.Dataset.from_tensor_slices(inputs).batch(batch_size).make_one_shot_iterator()
    
    return dataset.get_next()

def eval_input_fn(features, labels, batch_size):
    print "eval_input_fn"
    if labels is None:
        inputs = features
    else:
        inputs = (dict(features), labels)

    dataset = tf.data.Dataset.from_tensor_slices(inputs).batch(batch_size).make_one_shot_iterator()
    
    return dataset.get_next()

def main(argv): # ASOS, ONI
    ASOS_file_path = argv[1]
    ONI_file_path = argv[2]
    model_dir = argv[3]
    print "Application start: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "ASOS file path: " + ASOS_file_path
    if not os.path.exists(ASOS_file_path):
        print "ASOS file does not exist"
        exit(0)
    print "ONI file path: " + ONI_file_path
    if not os.path.exists(ONI_file_path):
        print "ONI file does not exist"
        exit(0)
    
    print "load start: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    load_start = time.time()
    (train_x, train_y, TRAIN_SIZE, test_x, test_y, TEST_SIZE) = load_data(ASOS_file_path, ONI_file_path, FROM_YEAR, CUT_YEAR, LAST_YEAR)
    feature_columns = make_feature_columns(train_x)
    HIDDEN_UNITS = [100 for i in range(20)]
    regressor = tf.estimator.DNNRegressor(
            hidden_units = HIDDEN_UNITS,
            feature_columns = feature_columns,
            model_dir = model_dir,
            label_dimension = 1,
            weight_column = None,
            optimizer = 'Adagrad',
            activation_fn = tf.nn.relu,
            dropout = None,
            input_layer_partitioner = None,
            config = None
            )
    load_end = time.time()

    print "train start: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    train_start = time.time()
    regressor.train(
            input_fn = lambda:train_input_fn(train_x, train_y, BATCH_SIZE),
            hooks = None,
            steps = None,
            max_steps = None,
            saving_listeners = None
            )
    train_end = time.time()

    print "test start: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_start = time.time()
    eval_result = regressor.evaluate(
            input_fn = lambda:eval_input_fn(test_x, test_y, BATCH_SIZE),
            steps = TEST_SIZE//BATCH_SIZE,
            hooks = None,
            checkpoint_path = None,
            name = None
            )
    test_end = time.time()

    load_time = load_end - load_start
    train_time = train_end - train_start
    test_time = test_end - test_start
    print ",".join(["load_time", "train_time", "test_time"])
    print ",".join([str(load_time), str(train_time), str(test_time)])
    print eval_result


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
