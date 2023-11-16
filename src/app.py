# We are going to fit a linear model to data on ipfs

# Input arguments:
    # - CID where the csv is saved

# Output
    # - model summary
    # - model parameters
    # - model predictions

# Journey:
#  User uploads a csv file to ipfs, saving its cid
# User runs a lilypad job, passing the cid as an argument
# Lilypad downloads the file from ipfs
# Lilypad runs the linear model on the data
# Lilypad writes the results to files

import logging
import argparse
import os
import json
import pickle

from requests import request
import pandas as pd
from sklearn.linear_model import LinearRegression #pip install scikit-learn

output_dir = "/outputs"
input_dir = "/inputs"

def write_buffer_to_file(data, path_to_file):
    with open(path_to_file, "wb") as f:
        f.write(data)


# NO NEED OF DOWNLOADING DATA, CUZ DATA WILL BE PREDOWNLOADED

# def download_data_cid(cid):
#     url = f"https://3.23.201.90/ipfs/{cid}"
#     payload = {}
#     headers = {}
#     response = request("GET", url, headers=headers, data=payload)
#     return response.content

def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(f'{output_dir}/test.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger

if __name__ == '__main__':
    logger = get_logger()
    logger.info('test')
    # we list all the files in the /inputs directory
    print("Files in the input directory:")
    logger.info("Files in the input directory:")
    print("AAAAAAAAAA")
    try:
        for file in os.listdir(input_dir):
            print(file)
            logger.info(file)
    except:
        with open(input_dir, 'w+') as f:
            print(f)
            logger.info(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('--file-name', type=str, required=True) # downloading from ipfs.chainsafe is the cid name 
    parser.add_argument('--target-column', type=str, required=True)
    parser.add_argument('--ignore-columns', nargs='+', type=str, required=False)

    args = parser.parse_args()

    print(f"Target column: {args.target_column}")
    logger.info(f"Target column: {args.target_column}")
    if args.ignore_columns:
        print(f"Ignoring columns: {args.ignore_columns}")
        logger.info(f"Ignoring columns: {args.ignore_columns}")
    else:
        print("No columns ignored")
        logger.info("No columns ignored")

    # NO NEED OF DOWNLOADING DATA, CUZ DATA WILL BE PREDOWNLOADED

    # # We download the file from ipfs
    # data = download_data_cid(args.url_source)

    # # We write the data to a csv file
    # write_buffer_to_file(data, input_dir+'/data.csv')

    # We read the data into a pandas dataframe
    df = pd.read_csv(f'{input_dir}/{args.file_name}')

    target = df[args.target_column]
    features = df.drop(columns=[args.target_column])
    if args.ignore_columns:
        features = features.drop(columns=args.ignore_columns)
    
    # We log the feature names
    print("Features identified")
    logger.info("Features: {}".format(features.columns))

    # We fit the model
    model = LinearRegression()
    model.fit(features, target)

    # # We log the model summary
    # print("Model summary")
    # print(model.summary())
    # logger.info("Model summary: {}".format(model.summary()))
    print("Coefficient of determination: {}".format(model.score(features, target)))


    target_hat = model.predict(features)

    # We save the model parameters, the predictions and the model itself to files

    # We save the model parameters to a json file
    model_params = model.get_params()
    with open(output_dir+'/model_params.json', 'w+') as f:
        f.write(json.dumps(model_params))

    # We save the predictions to a csv file
    df["predictions"] = target_hat
    df.to_csv(output_dir+'/predictions.csv')

    # We save the model to a pickle file
    model_name = "linear_model.pkl"
    with open(output_dir+'/'+model_name, 'wb') as f:
        pickle.dump(model, f)     